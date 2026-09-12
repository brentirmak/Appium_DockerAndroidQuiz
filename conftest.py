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
        "http://127.0.0.1:4725"
    )

    # ============================================================
    # Determine APK path (inside Docker container)
    # ============================================================
    apk_path = os.getenv(
        "APK_PATH",
        "/home/brent-ubuntu-26-04/AppiumProjects/Appium_DockerAndroidQuiz/bitbar-sample-app.apk"
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

    # 🔥 FIX: override UiAutomator2Options default automationName
    options.set_capability("automationName", "UiAutomator2")
    options.set_capability("appium:automationName", "UiAutomator2")

    if os.getenv("JENKINS_URL") or os.getenv("BUILD_NUMBER"):
        print("We are running on Jenkins - setting device_udid accordingly")
        device_udid = "192.168.150.1:5555"
    else:
        print("We are performing a manual run - setting device_udid accordingly")
        device_udid = "192.168.150.1:5555"

    options.set_capability("appium:udid", device_udid)
    options.set_capability("appium:deviceName", "Docker-Android")

    # APK path must exist inside Docker container
    options.app = apk_path

    # ============================================================
    # Capability logging
    # ============================================================
    print("=== CAPABILITIES SENT TO APPIUM ===")
    print(options.capabilities)
    print("===================================")

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
