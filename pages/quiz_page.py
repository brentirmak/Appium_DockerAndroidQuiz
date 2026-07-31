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
        self.tap(self.radio_locator(index))

    def enter_name(self, name: str):
        self.type_text(self.NAME_FIELD, name)
        self.driver.press_keycode(AndroidKey.ENTER)

    def submit(self):
        self.tap(self.SUBMIT_BUTTON)

    def get_result_text(self) -> str:
        return self.get_text(self.RESULT_TEXT)

    def is_correct(self) -> bool:
        return self.get_result_text() == self.CORRECT_RESULT_TEXT

    def go_back_to_question(self):
        self.driver.back()

    def answer_with_random_choice(self, name: str = "Brent") -> bool:
        """One full attempt: pick a random radio, enter name, submit, check result."""
        import random
        random_index = random.randint(0, 2)
        self.select_radio(random_index)
        self.enter_name(name)
        self.submit()
        return self.is_correct()