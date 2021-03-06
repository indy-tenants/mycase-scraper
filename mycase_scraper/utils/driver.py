import re
from json import loads
from re import match
from time import sleep

from loguru import logger
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire.webdriver import Chrome

from settings import Settings
from utils.builders.selector import CSSSelectorBuilder
from utils.case import CaseDetails, SearchItem, SearchResults
from utils.uri import URI

logger.debug('starting webdriver')

SECONDS = 1
MINUTES = 1
SHORT_TIMEOUT = 3 * SECONDS
DEFAULT_TIMEOUT = 10 * SECONDS
MAX_TIMEOUT = 30 * SECONDS
USER_INPUT_TIMEOUT = 5 * MINUTES


def get_options() -> Options:
    options = Options()
    options.headless = Settings.CHROME_HEADLESS
    logger.debug(f'Getting options {options}')
    return options


class Driver:
    """
        This class might break over time. I've done my best to make it easy to fix as things break
    """

    _instance = None
    _driver: Chrome = None

    @classmethod
    def _init_driver(cls, options=get_options()):
        return Chrome(options=options)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = Driver()
            cls._instance._driver = cls._init_driver()
            cls._instance._driver.scopes = [URI.SEARCH_CASES_RE, URI.CASE_SUMMARY_RE]
        return cls._instance

    @classmethod
    def tidy_up(cls):
        try:
            if hasattr(cls, '_instance'):
                del cls._instance
            if hasattr(cls, '_driver'):
                del cls._driver
        except AttributeError as ae:
            logger.exception(f'Could not tidy up {ae}')

    def __del__(self):
        logger.debug('shutting down webdriver')
        self.get_driver().close()
        self.get_driver().quit()

    def get_driver(self) -> Chrome:
        return self._driver

    def go(self, uri):
        logger.info(f'Navigating to url {uri}')
        self.get_driver().get(uri)
        self.check_for_captcha()
        return self

    def go_home(self):
        logger.debug(f'go to {URI.SEARCH}')
        self.get_driver().get(URI.SEARCH)
        return self

    # Waiters

    def wait_for_element_selector(self, selector, timeout=MAX_TIMEOUT):
        logger.debug(f'Waiting for selector \'{selector}\' to load')
        try:
            return WebDriverWait(
                self.get_driver(),
                timeout
            ).until(
                presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        selector
                    )
                )
            )
        except TimeoutException:
            logger.exception(f'Timed out waiting for selector \'{selector}\'')

    def wait_for_search_results(self):
        self.wait_for_element_selector(
            CSSSelectorBuilder().tag('tr').withClazz('result-row').build()
        )

    def check_for_captcha(self):
        try:
            return self.wait_for_element_selector(
                CSSSelectorBuilder().id('CaptchaModal').build(),
                timeout=SHORT_TIMEOUT
            )
        except TimeoutException:
            return None

    def wait_while_captcha_modal_on_screen(self):
        while self.check_for_captcha():
            logger.info('Captcha modal detected on screen, waiting')
            sleep(MAX_TIMEOUT)

    # data getters

    # def get_search_cases_response(self) -> list:
    #     requests = filter(lambda r: r.url == URI.SEARCH_CASES, self.get_driver().requests)
    #     return [r.response for r in requests]

    def get_detailed_case_info(self, case_item: SearchItem) -> CaseDetails:
        logger.debug(f'Getting details for case number {case_item.get_case_number()}')
        self.instance().go(URI.get_case_url(case_item.get_case_token()))
        self.wait_for_element_selector(
            CSSSelectorBuilder().tag('h4').withClazz('text-primary').withAttribute('data-bind',
                                                                                   'html: Style').build()
        )
        return self.get_details_from_network_requests(case_item)

    def navigate_through_set_of_search_results(self):
        try:
            def check():
                sleep(3 * SECONDS)  # TODO: Get rid of this maybe?

                running_total_regex = r'(?P<lower_current>\d*) to (?P<upper_current>\d*) of (?P<total>\d*)'

                running_total_match = re.search(
                    running_total_regex,
                    self.get_driver().page_source
                )

                if running_total_match is None:
                    logger.error('Cant find totals on screen, bailing out')
                    return True

                running_total_match_dict = running_total_match.groupdict()
                return running_total_match_dict['upper_current'] == running_total_match_dict['total']

            while not check():
                sleep(SECONDS)
                next_button = WebDriverWait(self.get_driver(), DEFAULT_TIMEOUT).until(
                    presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            CSSSelectorBuilder().tag('button').withAttribute('title', 'Go to next result page').build()
                        )
                    )
                )
                next_button.click()
                WebDriverWait(self.get_driver(), DEFAULT_TIMEOUT).until(
                    presence_of_element_located((By.CLASS_NAME, 'results'))
                )
        except TimeoutException:
            logger.exception(f'Timed out waiting on next button, assume we have all the cases and move on')
        except Exception as ex:
            logger.exception(f'{ex}')

    # Collect network requests

    def get_search_result(self, case_num: str) -> SearchItem:
        logger.debug(f'Searching for single case with case number {case_num}')
        self.instance().go(URI.get_case_url_for_case_number(case_num))
        self.wait_for_search_results()
        return self.get_search_results_from_network_requests().find_by_case_number(case_num)

    def get_search_results_list(self, search_term: str) -> SearchResults:
        logger.debug(f'Searching for list of cases for search term {search_term}')
        self.instance().go(URI.get_case_url_for_case_number(search_term))
        self.navigate_through_set_of_search_results()
        return self.get_search_results_from_network_requests()

    # Get network requests

    def get_search_results_from_network_requests(self) -> SearchResults:
        filtered_requests = list(
            filter(
                lambda r: r.response is not None and r.response.status_code == 200 and match(URI.SEARCH_CASES_RE, r.url),
                self.instance().get_driver().requests
            )
        )
        results: SearchResults = SearchResults()
        for req in filtered_requests:
            json_body = loads(req.response.body)
            json_results = json_body.get('Results')
            results.add_list(
                [SearchItem(d) for d in json_results] if json_results is not None else []
            )
            if json_body.get('TotalResults') == results.get_total():
                logger.info(f'Total number of {results.get_total()} cases collected')
        return results

    def get_details_from_network_requests(self, search_item: SearchItem) -> CaseDetails:

        logger.debug(f'Trying to get details from network requests')
        try:
            filtered_requests: list = list(
                filter(
                    lambda r: r.response is not None and r.response.status_code == 200 and match(URI.CASE_SUMMARY_RE, r.url),
                    self.instance().get_driver().requests
                )
            )
            req = filtered_requests.pop()
            details = loads(req.response.body)
            return CaseDetails(search_item, details)
        except TimeoutException as te:
            logger.exception(f'Timed out waiting for details for case {search_item.get_case_number()}: {te}')
        except Exception as ex:
            logger.exception(f'Failed to get details for case {search_item.get_case_number()}: {ex}')
