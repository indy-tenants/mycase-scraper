import re
from json import loads
from time import sleep
from loguru import logger
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from seleniumwire.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from settings import Settings
from builders.selector import CSSSelectorBuilder
from uri import URI

logger.debug('starting webdriver')

ONE_SECOND = 1
DEFAULT_SLEEP_INTERVAL = 3
DEFAULT_WAIT_TIME = 3
MAX_TIMEOUT = 30


def get_options():
    options = Options()
    options.headless = Settings.CHROME_HEADLESS
    logger.debug(f'Getting options {options}')
    return options


class SearchItem:

    data = {}

    def __init__(self, data):
        self.data = data

    def get_id(self):
        logger.debug(f'Getting CaseID {self.data.get("CaseID")}')
        return self.data.get('CaseID')

    def get_case_number(self):
        logger.debug(f'Getting CaseNumber {self.data.get("CaseNumber")}')
        return self.data.get('CaseNumber')

    def get_case_token(self):
        logger.debug(f'Getting CaseToken {self.data.get("CaseToken")}')
        return self.data.get('CaseToken')


class SearchResults:

    _results = {}

    def add(self, item: SearchItem):
        if item.get_case_number() not in self._results.keys():
            logger.debug(f'Adding item with case number {item.get_case_number()}')
            self._results.update({item.get_case_number(): item})
        else:
            logger.warning(f'Item with case number {item.get_case_number()} already exists in set')

    def add_list(self, items: [SearchItem]):
        logger.debug(f'Adding {len(items)} items to list of results')
        for i in items:
            self.add(i)

    def get_total(self):
        logger.debug(f'Getting total results, current: {len(self._results)}')
        return len(self._results.keys())

    def keys(self):
        logger.debug(f'Getting result keys {self._results.keys()}')
        return self._results.keys()

    def values(self):
        logger.debug(f'Getting result values {self._results.values()}')
        return self._results.values()


class Details:
    _details = {}

    def add(self, body):
        if 'Results' in body:
            self._details.update(body)


class Driver:
    """
        This class might break over time. I've done my best to make it easy to fix as things break
    """

    _instance = None
    _driver = None

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

    def __del__(self):
        logger.debug('shutting down webdriver')
        self.get_driver().close()
        self.get_driver().quit()

    def tidy_up(self):
        del self._driver

    class Go:

        @staticmethod
        def to(page):
            logger.debug(f'go to {page.SEARCH.value}')
            pass

    def get_driver(self):
        return self._driver

    def go(self, uri):
        logger.info(f'Navigating to url {uri}')
        self.get_driver().get(uri)

    def go_home(self):
        logger.debug(f'go to {URI.SEARCH}')
        self.get_driver().get(URI.SEARCH)
        return self

    def get_search_cases_response(self):
        requests = filter(lambda r: r.url == URI.SEARCH_CASES, self.get_driver().requests)
        return [r.response for r in requests]

    def get_results_list(self, court_code, year_month):
        self.instance().go(URI.get_search_url_with_court_and_date(court_code, year_month))
        results = SearchResults()
        try:
            def check():
                running_total_selector = '#OD_BODY > div:nth-child(4) > table > tbody > tr > td.pad-all-0.va-bottom.text-right.width-30p.hidden-xs > div > div:nth-child(1) > span'
                running_total_regex = r'(?P<lower_current>\d*) to (?P<upper_current>\d*) of (?P<total>\d*)'

                running_total = WebDriverWait(self.get_driver(), DEFAULT_WAIT_TIME).until(
                    presence_of_element_located((By.CSS_SELECTOR, running_total_selector))
                )

                match = re.match(running_total_regex, running_total.text)

                if match is None:
                    logger.error('Cant find totals on screen, bailing out')
                    return True

                return match.groupdict()['upper_current'] == match.groupdict()['total']

            while not check():
                next_button = WebDriverWait(self.get_driver(), DEFAULT_WAIT_TIME).until(
                    presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            CSSSelectorBuilder().tag('button').withAttribute('title', 'Go to next result page').build()
                        )
                    )
                )
                next_button.click()
                sleep(ONE_SECOND)
                WebDriverWait(self.get_driver(), DEFAULT_WAIT_TIME).until(
                    presence_of_element_located((By.CLASS_NAME, 'results')))
        except TimeoutException as ex:
            logger.exception(f'{ex}')
            logger.debug('Timed out waiting on next button, assume we have all the cases and move on')
        except Exception as ex:
            logger.exception(f'{ex}')
        finally:
            filtered_requests = list(
                filter(
                    lambda r: r.response.status_code == 200 and re.match(URI.SEARCH_CASES_RE, r.url),
                    self.instance().get_driver().requests
                )
            )
            for req in filtered_requests:
                json_body = loads(req.response.body)
                search_result_items = [SearchItem(d) for d in json_body.get('Results')]
                results.add_list(search_result_items)
                if json_body.get('TotalResults') == results.get_total():
                    logger.info(f'Total number of {results.get_total()} cases collected')
            return results

    def get_detailed_case_results(self, case_item: SearchItem):
        self.instance().go(URI.get_case_url(case_item.get_case_token()))


class BasePage:

    def get_title(self):
        pass

    def get_data(self):
        pass


class CaseSearchPage(BasePage):

    @staticmethod
    def search_button():
        return By.CSS_SELECTOR, CSSSelectorBuilder().tag('button').withAttribute('name', 'submit').build()

    @staticmethod
    def search_input():
        return By.CSS_SELECTOR, CSSSelectorBuilder().tag('input').withId('SearchCaseNumber').build()
