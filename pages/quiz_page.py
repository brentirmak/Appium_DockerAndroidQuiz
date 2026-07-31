from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.android.nativekey import AndroidKey
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class QuizPage(BasePage):
    PACKAGE = "com.bitbar.testdroid"

    RESULT_TEXT = (AppiumBy.XPATH, f'//android.widget.TextView[@resource-id="{PACKAGE}:id/textView1"]')
    NAME_FIELD = (AppiumBy.XPATH, f'//android.widget.EditText[@resource-id="{PACKAGE}:id/editText1"]')
    SUBMIT_BUTTON = (AppiumBy.XPATH, f'//android.widget.Button[@resource-id="{PACKAGE}:id/button1"]')

    CORRECT_RESULT_TEXT = "You are right!"

    def radio_locator(self, index: int) -> tuple:
        return (
            AppiumBy.XPATH,
            f'//android.widget.RadioButton[@resource-id="{self.PACKAGE}:id/radio{index}"]',
        )

    def wait_for_question_loaded(self, timeout: int = None):
        """Waits until at least one radio button is present, confirming the question screen is ready."""
        WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.presence_of_element_located(self.radio_locator(0))
        )

    def select_radio(self, index: int):
        print("Will tap radio button")
        self.tap(self.radio_locator(index))
        print("Tapped radio button")

    def enter_name(self, name: str):
        print("Will enter name")
        self.type_text(self.NAME_FIELD, name)
        print("Entered name. Will now hit <Enter>")
        self.driver.press_keycode(AndroidKey.ENTER)
        print("<Enter> key was pressed")

    def submit(self):
        print("Will click on the Submit button")
        self.tap(self.SUBMIT_BUTTON)
        print("Submit button was pressed")

    def get_result_text(self) -> str:
        print("Will get result text")
        return self.get_text(self.RESULT_TEXT)

    def is_correct(self) -> bool:
        print("Checking for the correct answer")
        return self.get_result_text() == self.CORRECT_RESULT_TEXT

    def go_back_to_question(self):
        print("Will go back to the previous question")
        self.driver.back()

    def answer_with_random_choice(self, name: str = "Brent") -> bool:
        """One full attempt: pick a random radio, enter name, submit, check result."""
        import random
        random_index = random.randint(0, 2)
        print("Will pick a random answer")
        self.select_radio(random_index)
        self.enter_name(name)
        self.submit()
        return self.is_correct()