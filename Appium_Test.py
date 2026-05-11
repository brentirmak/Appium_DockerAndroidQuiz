import random

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.android.nativekey import AndroidKey
from appium import webdriver
from appium.options.android import UiAutomator2Options
import time
import os

options = UiAutomator2Options()

options.platform_name = "Android"
options.device_name = "Android Emulator"
options.automation_name = "UiAutomator2"

# APK path INSIDE container
#options.app = "/root/tmp/bitbar-sample-app.apk"
options.app = "/home/androidusr/bitbar-sample-app.apk"

run_type = "manual"

if "var/lib/jenkins/workspace" in os.getcwd():
    print("We are running script from Jenkins server - path needs to be changed")
    run_type = "jenkins"
    print("Path for results file has been set, type set to jenkins")
else:
    print("We are running script from development VM")

driver = webdriver.Remote(
    #To run from Windows (host)
    #command_executor="http://localhost:4723",
    #To run from VM inside of Windows (host)
    command_executor="http://192.168.150.1:4723",
    options=options
)

time.sleep(5)

print("App launched successfully")

# Example interaction
elements = driver.find_elements("xpath", "//*")
print(f"Found {len(elements)} UI elements")

correct_answer = False

while not correct_answer:
    random_number = random.randint(0, 2)
    print("The following random number was chosen: ", random_number)

    xpath_value = "//android.widget.RadioButton[@resource-id=\"com.bitbar.testdroid:id/radio" + str(random_number) + "\"]"

    print("Will now answer the question")
    driver.find_element(by=AppiumBy.XPATH, value=xpath_value).click()
    print("Clicked on the radio button")

    print("Will now click on the 'Please type your name to proceed' field.")
    text_field = driver.find_element(by=AppiumBy.XPATH, value="//android.widget.EditText[@resource-id=\"com.bitbar.testdroid:id/editText1\"]")
    text_field.clear()

    print("Entering 'Brent'")
    text_field.send_keys("Brent")
    print("Will hit <ENTER>")
    driver.press_keycode(AndroidKey.ENTER)
    print("Clicking on the Answer button")
    driver.find_element(by=AppiumBy.XPATH, value="//android.widget.Button[@resource-id=\"com.bitbar.testdroid:id/button1\"]").click()
    print("Capturing the result")
    result = driver.find_element(by=AppiumBy.XPATH, value="//android.widget.TextView[@resource-id=\"com.bitbar.testdroid:id/textView1\"]").text

    if result == "You are right!":
        print("Correct Answer!")
        correct_answer = True
    else:
        print("Wrong Answer! Try again")
        driver.back()
        time.sleep(5)

time.sleep(5)

driver.quit()
