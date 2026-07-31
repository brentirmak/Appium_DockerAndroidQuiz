from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout

    def find(self, locator: tuple):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def find_clickable(self, locator: tuple):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def tap(self, locator: tuple):
        self.find_clickable(locator).click()

    def get_text(self, locator: tuple) -> str:
        return self.find(locator).text

    def type_text(self, locator: tuple, text: str, clear_first: bool = True):
        field = self.find(locator)
        if clear_first:
            field.clear()
        field.send_keys(text)