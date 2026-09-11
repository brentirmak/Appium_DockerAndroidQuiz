import os
import pytest
from dotenv import load_dotenv
from appium import webdriver
from appium.options.android import UiAutomator2Options
@pytest.fixture(scope="function")
def driver():
    # ============================================================
    # Load .env for local execution
    # ============================================================
    load_dotenv()
    # ============================================================
    # Determine Appium server (Docker Appium)
    # ============================================================
    webdriver_remote_url = os.getenv(
        "WEBDRIVER_REMOTE_URL",
        "http://127.0.0.1:4725"   # Docker Appium runs on its own port
    )
    # ============================================================
    # Determine APK path (inside Docker container)
    # ============================================================
    apk_path = os.getenv(
        "APK_PATH",
        "/home/androidusr/bitbar-sample-app.apk"
    )
    # ============================================================
    # Display configuration
    # ============================================================
    print("\n==========================================")
    print("Docker Appium Driver Configuration")
    print("==========================================")
    print("Current directory:", os.getcwd())
    print("WEBDRIVER_REMOTE_URL =", webdriver_remote_url)
    print("APK_PATH =", apk_path)
    print("==========================================")
    # ============================================================
    # Configure Android (Docker Emulator)
    # ============================================================
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"

    if os.getenv("JENKINS_URL") or os.getenv("BUILD_NUMBER"):
        # Running under Jenkins - your pipeline already sets DEVICE_UDID,
        # so reaching here means something upstream changed; keep old default as a safety net
        print("We are running on Jenkins - setting device_udid accordingly")
        #device_udid = "192.168.150.1:5560"
        device_udid = "192.168.150.1:5555"
    else:
        # Manual/local run - the container's internal Appium sees the emulator by its own serial
        print("We are performing a manual run - setting device_udid accordingly")
        device_udid = "emulator-5554"

    options.set_capability("appium:udid", device_udid)

    # Clear device name to avoid Windows confusion
    options.set_capability("appium:deviceName", "Docker-Android")
    # APK path must exist inside Docker container
    options.app = apk_path
    # ============================================================
    # Create Appium session
    # ============================================================
    drv = webdriver.Remote(
        command_executor=webdriver_remote_url,
        options=options
    )
    # ============================================================
    # Return driver to pytest
    # ============================================================
    yield drv
    # ============================================================
    # Cleanup
    # ============================================================
    try:
        drv.quit()
    except Exception:
        pass