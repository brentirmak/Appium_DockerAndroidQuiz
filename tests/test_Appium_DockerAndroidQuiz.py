# tests/test_answer_question.py
import random
import time
import os
import sys
import pytest
import Appium_DockerAndroidQuiz_WriteResult
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.android.nativekey import AndroidKey

class TestAnswerQuestion:

    def test_answer_question(self, driver):
        start = time.time()

        # Detect run type
        run_type = "jenkins" if "var/lib/jenkins/workspace" in os.getcwd() else "manual"
        results_log_path = (
            os.getcwd() + '/Appium_DockerAndroidQuiz.txt' if run_type == "jenkins"
            else '/home/brent-ubuntu-26-04/AppiumProjects/Appium_DockerAndroidQuiz/Appium_DockerAndroidQuiz.txt'
        )

        time.sleep(5)
        elements = driver.find_elements("xpath", "//*")
        print(f"Found {len(elements)} UI elements")

        correct_answer = False

        while not correct_answer:
            random_number = random.randint(0, 2)
            xpath_value = f"//android.widget.RadioButton[@resource-id=\"com.bitbar.testdroid:id/radio{random_number}\"]"

            driver.find_element(by=AppiumBy.XPATH, value=xpath_value).click()

            text_field = driver.find_element(by=AppiumBy.XPATH, value="//android.widget.EditText[@resource-id=\"com.bitbar.testdroid:id/editText1\"]")
            text_field.clear()
            text_field.send_keys("Brent")
            driver.press_keycode(AndroidKey.ENTER)

            driver.find_element(by=AppiumBy.XPATH, value="//android.widget.Button[@resource-id=\"com.bitbar.testdroid:id/button1\"]").click()

            result = driver.find_element(by=AppiumBy.XPATH, value="//android.widget.TextView[@resource-id=\"com.bitbar.testdroid:id/textView1\"]").text

            if result == "You are right!":
                correct_answer = True
            else:
                driver.back()
                time.sleep(5)

        duration = time.time() - start

        with open(results_log_path, 'w') as results_log:
            Appium_DockerAndroidQuiz_WriteResult.init(results_log, "Answer_Question", "Pass", str(duration), run_type)

        assert correct_answer, "Never found the correct answer"