import random

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.android.nativekey import AndroidKey
from appium import webdriver
from appium.options.android import UiAutomator2Options
import Appium_Test_WriteResult
import time
import os
import sys
from dotenv import load_dotenv

try:
    options = UiAutomator2Options()

    options.platform_name = "Android"
    options.device_name = "Android Emulator"
    options.automation_name = "UiAutomator2"

    # APK path INSIDE container
    options.app = "/home/androidusr/bitbar-sample-app.apk"

    run_type = "manual"

    # 1. Load the environment variables from the .env file
    load_dotenv()

    # 2. Retrieve the secrets using os.getenv()
    webdriver_remote_url = os.getenv("WEBDRIVER_REMOTE_URL")

    if "var/lib/jenkins/workspace" in os.getcwd():
        print("We are running script from Jenkins server - path needs to be changed")
        run_type = "jenkins"
        results_log_path = os.getcwd() + '/Appium_Test.txt'
        print("Results Log Path (per script): ", results_log_path)
        print("Path for results file has been set, type set to jenkins")
    else:
        print("We are running script from development VM")
        results_log_path = '/home/brent-ubuntu-26-04/SeleniumProjects/Appium_Test/Appium_Test.txt'
        print("Results Log Path (per script): ", results_log_path)
        print("Path for results file has been set, type set to manual")

    with open(results_log_path, 'w') as results_log:
        print("*************** START: Answer Question Transaction ***************")
        answer_question_transaction_start = time.time()

        driver = webdriver.Remote(
            #To run from Windows (host)
            #command_executor="http://localhost:4723",
            #To run from VM inside of Windows (host)
            command_executor=webdriver_remote_url,
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

        answer_question_transaction_end = time.time()
        print("*************** END: Answer Question Transaction ***************")

        answer_question_transaction = answer_question_transaction_end - answer_question_transaction_start
        print("\nAnswer Question Transaction Duration: ", str(answer_question_transaction))

        Appium_Test_WriteResult.init(results_log, "Answer_Question", "Pass", str(answer_question_transaction), run_type)

        time.sleep(5)

        driver.quit()

except Exception as err:
    print("Exception: ", err)

    Appium_Test_WriteResult.init(results_log, "Answer_Question", "Fail", "NULL", run_type)

    driver.quit()

    try:
        sys.exit(1)
    except SystemExit:
        print("SystemExit Exception terminated the program!")
        quit()

