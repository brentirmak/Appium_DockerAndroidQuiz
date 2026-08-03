import pytest
import os
from appium import webdriver
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv

@pytest.fixture(scope="function")
def driver():
    load_dotenv()
    webdriver_remote_url = os.getenv("WEBDRIVER_REMOTE_URL")
    print("\nCurrent directory:", os.getcwd())
    print("WEBDRIVER_REMOTE_URL =", os.getenv("WEBDRIVER_REMOTE_URL"))
    
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "Android Emulator"
    options.automation_name = "UiAutomator2"
    #options.app = "/home/androidusr/bitbar-sample-app.apk"

    apk_path = os.getenv(
        "APK_PATH",
        "/home/androidusr/bitbar-sample-app.apk"
    )

    print("APK_PATH =", apk_path)

    options.app = apk_path

    drv = webdriver.Remote(
        command_executor=webdriver_remote_url,
        options=options
    )

    yield drv  # driver is passed to each test

    drv.quit()  # teardown after each test