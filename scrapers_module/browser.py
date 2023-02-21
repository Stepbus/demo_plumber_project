import random
from time import sleep

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from scrapers_module.exceptions import NoSuchElementError


class Browser:
    element_waiting_timeout_sec = 15

    def __init__(self):
        options = webdriver.ChromeOptions()
        self.__set_up_chrome_options(options)
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(
            service=service,
            options=options,
        )

    @staticmethod
    def __set_up_chrome_options(options):
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        options.add_argument('--headless')

    def go_to_url(self, url):
        self.driver.get(url)

    def move_to_element(self, element: WebElement):
        action = webdriver.ActionChains(self.driver)
        action.move_to_element(element).perform()

    def scroll_to_element(self, element: WebElement):
        action = webdriver.ActionChains(self.driver)
        action.scroll_to_element(element).perform()

    def get_element_by_xpath(self, driver_, xpath: str, raise_error=True):
        try:
            element = WebDriverWait(driver_, self.element_waiting_timeout_sec).until(
                ec.visibility_of_element_located((By.XPATH, f'{xpath}'))
            )
            if element:
                return element
        except TimeoutException:
            if raise_error:
                raise NoSuchElementError(f'No element was found by XPATH: {xpath}')

    def get_elements_by_xpath(self, driver_, xpath: str, raise_error=True):
        try:
            element = WebDriverWait(driver_, self.element_waiting_timeout_sec).until(
                ec.visibility_of_all_elements_located((By.XPATH, f'{xpath}'))
            )
            if element:
                return element
        except TimeoutException:
            if raise_error:
                raise NoSuchElementError(f'No element was found by XPATH: {xpath}')
            else:
                return []

    @staticmethod
    def click_on_element(element: WebElement):
        element.click()

    @staticmethod
    def paste_text_into_field(input_field: WebElement, text: str):
        for char in text:
            sleep(random.choice((0.05, 0.1, 0.15, 0.2)))
            input_field.send_keys(char)

    def refresh(self):
        self.driver.refresh()

    def quit_browser(self):
        self.driver.quit()
