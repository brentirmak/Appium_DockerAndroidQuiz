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

    # Docker emulator UDID (never Windows)
    options.set_capability("appium:udid", "emulator-5556")

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
