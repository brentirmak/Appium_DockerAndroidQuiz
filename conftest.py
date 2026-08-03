```python
import os

import pytest
from dotenv import load_dotenv
from appium import webdriver
from appium.options.android import UiAutomator2Options


@pytest.fixture(scope="function")
def driver():

    load_dotenv()

    webdriver_remote_url = os.getenv(
        "WEBDRIVER_REMOTE_URL",
        "http://127.0.0.1:4723"
    )

    # Keep the Docker container APK path.
    # This path exists inside the Docker container,
    # NOT on the Jenkins server or Windows host.
    apk_path = os.getenv(
        "APK_PATH",
        "/home/androidusr/bitbar-sample-app.apk"
    )

    print("\n==========================================")
    print("Appium Driver Configuration")
    print("==========================================")
    print("Current directory:", os.getcwd())
    print("WEBDRIVER_REMOTE_URL =", webdriver_remote_url)
    print("APK_PATH =", apk_path)
    print("==========================================")

    options = UiAutomator2Options()

    options.platform_name = "Android"
    options.device_name = "Android Emulator"
    options.automation_name = "UiAutomator2"

    # APK path is interpreted by Appium.
    # Because Appium is running inside Docker,
    # this path must exist inside the Docker container.
    options.app = apk_path

    drv = webdriver.Remote(
        command_executor=webdriver_remote_url,
        options=options
    )

    yield drv

    try:
        drv.quit()
    except Exception:
        pass
```
s