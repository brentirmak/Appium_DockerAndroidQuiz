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
    # Determine Appium server
    # ============================================================
    #
    # Jenkins:
    #   WEBDRIVER_REMOTE_URL is supplied by Jenkins.
    #
    # Local:
    #   Falls back to localhost.
    #
    webdriver_remote_url = os.getenv(
        "WEBDRIVER_REMOTE_URL",
        "http://127.0.0.1:4723"
    )

    # ============================================================
    # Determine APK path
    # ============================================================
    #
    # Jenkins:
    #   Jenkins exports:
    #
    #   APK_PATH=/home/androidusr/bitbar-sample-app.apk
    #
    # Local:
    #   Falls back to the same path, which works with the
    #   locally running Docker/Appium environment.
    #
    apk_path = os.getenv(
        "APK_PATH",
        "/home/androidusr/bitbar-sample-app.apk"
    )

    # ============================================================
    # Display configuration
    # ============================================================

    print("\n==========================================")
    print("Appium Driver Configuration")
    print("==========================================")
    print("Current directory:", os.getcwd())
    print("WEBDRIVER_REMOTE_URL =", webdriver_remote_url)
    print("APK_PATH =", apk_path)
    print("==========================================")

    # ============================================================
    # Configure Android
    # ============================================================

    options = UiAutomator2Options()

    options.platform_name = "Android"
    options.device_name = "Android Emulator"
    options.automation_name = "UiAutomator2"

    # APK path is interpreted by the Appium server.
    #
    # Appium is running inside Docker, therefore this path
    # must exist INSIDE the Docker container.
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
