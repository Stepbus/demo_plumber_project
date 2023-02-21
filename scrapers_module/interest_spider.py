import os
import re
from time import sleep

from logger_module.logger_ import user_log_name, logger
from scrapers_module.exceptions import PageDoesNotOpen, NoSuchElementError
from scrapers_module.web_elements_service import XPathElementsLogin, XPathElementsAddInfo, XPathElementsApplyJobRequest

from scrapers_module.browser import Browser

from dotenv import load_dotenv

load_dotenv()


class InterestSpider:
    home_url = 'https://www./'

    def __init__(self):
        self.browser = Browser()

    def login(self):
        self.browser.go_to_url(self.home_url)
        logger.log(user_log_name, f"go to {self.home_url}")
        cookies = self.browser.get_element_by_xpath(self.browser.driver, XPathElementsLogin.cookies_element,
                                                    raise_error=False)
        if cookies:
            logger.log(user_log_name, f"Press cookies")
            self.browser.move_to_element(cookies)
            self.browser.click_on_element(cookies)
        logger.log(user_log_name, f"Looking for registration button")
        login_button = self.browser.get_element_by_xpath(
            self.browser.driver, XPathElementsLogin.login_button, raise_error=False)
        if not login_button:
            logger.log(user_log_name, f"Already logged!")
            return
        self.browser.click_on_element(login_button)
        email_element = self.browser.get_element_by_xpath(self.browser.driver, XPathElementsLogin.email_element)
        logger.log(user_log_name, f"Text email in login form")
        self.browser.paste_text_into_field(email_element, os.environ.get('MAIL'))
        psw_element = self.browser.get_element_by_xpath(self.browser.driver, XPathElementsLogin.psw_element)
        logger.log(user_log_name, f"Text password in login form")
        self.browser.paste_text_into_field(psw_element, os.environ.get('PASS'))
        submit_element = self.browser.get_element_by_xpath(self.browser.driver, XPathElementsLogin.submit_element)
        logger.log(user_log_name, f"Submit the form")
        self.browser.move_to_element(submit_element)
        self.browser.click_on_element(submit_element)
        for _ in range(1, 3):
            logger.log(user_log_name, f"Waiting for download element in the main page (attempt {_})")
            waiting_download_element = self.browser.get_element_by_xpath(
                self.browser.driver, XPathElementsLogin.waiting_download_element, raise_error=False)
            if waiting_download_element:
                self.browser.move_to_element(waiting_download_element)
                return
            self.browser.refresh()
        raise NoSuchElementError(f"No element was found by XPATH in function login")

    def get_additional_info(self, url_propositions):
        additional_info_list: list[dict] = []
        for url_proposition in url_propositions:
            try:
                self.browser.go_to_url(url_proposition)
                logger.log(user_log_name, f"Go to {url_proposition}")
            except Exception as ex:
                logger.log(user_log_name, f"For dev: exception in get(): {type(ex).__name__} {ex.args}")
                self.browser.refresh()
                sleep(3)
                self.browser.go_to_url(url_proposition)
                logger.log(user_log_name, f"Go to (second time) {url_proposition}")
            title_add_info = self.browser.get_elements_by_xpath(self.browser.driver,
                                                                XPathElementsAddInfo.title_add_info)
            value_add_info = self.browser.get_elements_by_xpath(self.browser.driver,
                                                                XPathElementsAddInfo.value_add_info)
            if not title_add_info and not value_add_info:
                raise PageDoesNotOpen
            logger.log(user_log_name, f"Received 'title_add_info' and 'value_add_info'")
            result: dict = self._parsing_elements_from_page(title_add_info, value_add_info)
            if self._show_interest():
                additional_info_list.append(result)
        return additional_info_list

    def _parsing_elements_from_page(self, titles_elements: list, values_elements: list):
        logger.log(user_log_name, f"Parsing data from page")
        _, client_id = os.path.split(self.browser.driver.current_url)
        type_klus = ''
        soort_probleem = ''
        aanvullende_informatie = ''

        pattern_type_klus = re.compile(r'Type\sklus.+')
        pattern_soort_probleem = re.compile(r'Soort\s.+')
        pattern_aanvullende_informatie = re.compile(r'Aanvullende\sinformatie')

        titles = [el.text for el in titles_elements]
        values = [el.text for el in values_elements]

        selected_data = list(zip(titles, values))
        for element in selected_data:
            if pattern_type_klus.search(element[0]):
                type_klus += f"{element[-1]}; "
            elif pattern_soort_probleem.search(element[0]):
                soort_probleem += f"{element[-1]}; "
            elif pattern_aanvullende_informatie.search(element[0]):
                aanvullende_informatie += f"{element[-1]}; "
        return dict(client_id=int(client_id), type_klus=type_klus.strip(), soort_probleem=soort_probleem.strip(),
                    aanvullende_informatie=aanvullende_informatie.strip())

    def _show_interest(self):
        button_interesse = self.browser.get_element_by_xpath(
            self.browser.driver, XPathElementsApplyJobRequest.button_interesse, raise_error=False)
        if button_interesse:
            logger.log(user_log_name, f"I pressed button interesse ...")
            self.browser.click_on_element(button_interesse)
            logger.log(user_log_name, f"I sent message to client")
            return True
        logger.log(user_log_name, f"Button interesse missing")
        return False

    def run(self, url_propositions):
        self.login()
        result = self.get_additional_info(url_propositions)
        return result
