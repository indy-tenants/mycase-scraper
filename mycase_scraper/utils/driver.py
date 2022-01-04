from enum import Enum
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

from mycase_scraper.settings import Settings
from mycase_scraper.utils.builders.selector import CSSSelectorBuilder
from mycase_scraper.utils.uri import URI

logger.debug('starting webdriver')

ONE_SECOND = 1
DEFAULT_SLEEP_INTERVAL = 3
DEFAULT_WAIT_TIME = 3
MAX_TIMEOUT = 30


class CaseStatus(Enum):
    DECIDED = 'Decided'

    def __str__(self):
        return self.value


def get_options() -> Options:
    options = Options()
    options.headless = Settings.CHROME_HEADLESS
    logger.debug(f'Getting options {options}')
    return options


class SearchItem:
    _data: dict = {}

    def __init__(self, data):
        self._data = data

    def get_id(self) -> int:
        logger.debug(f'Getting CaseID {self._data.get("CaseID")}')
        return self._data.get('CaseID')

    def get_case_number(self) -> str:
        logger.debug(f'Getting CaseNumber {self._data.get("CaseNumber")}')
        return self._data.get('CaseNumber')

    def get_case_token(self) -> str:
        logger.debug(f'Getting CaseToken {self._data.get("CaseToken")}')
        return self._data.get('CaseToken')

    def get_case_status(self) -> CaseStatus:
        logger.debug(f'Getting CaseStatus {self._data.get("CaseStatus")}')
        return CaseStatus(self._data.get('CaseStatus'))

    def get_is_active(self) -> bool:
        logger.debug(f'Getting IsActive {self._data.get("IsActive")}')
        return self._data.get('IsActive')

    def get_data(self) -> dict:
        logger.debug(f'Getting data from SearchItem of case {self.get_case_number()}')
        return self._data


class CaseDetails(SearchItem):
    _details: dict = {
        'InvalidToken': None,
        'CaseKey': None,
        'CaseCategoryKey': None,
        'CaseCategoryGroup': None,
        'CaseNumber': None,
        'Court': None,
        'CourtCode': None,
        'CountyCode': None,
        'IsAppellateCourt': None,
        'FileDate': None,
        'CaseStatus': None,
        'CaseStatusDate': None,
        'CaseType': None,
        'CaseTypeCode': None,
        'CaseSubType': None,
        'Style': None,
        'IsActive': None,
        'IsPublic': None,
        'AppearByDate': None,
        'Bonds': None,
        'Charges': None,
        'Events': None,
        'Parties': None,
        'CrossRefs': None,
        'Related': None,
        'CommCourtFlag': None
    }

    def __init__(self, data, details=None):
        super(CaseDetails, self).__init__(data)
        self.add_details(details or {})

    @classmethod
    def from_search_item(cls, item: SearchItem):
        return cls(item.get_data())

    def add_details(self, details: dict):
        if 'InvalidToken' in details and details.get('InvalidToken') is False:
            self._details.update(details)
        return self

    def get_case_key(self) -> dict:
        logger.debug(f'Getting data from CaseDetails of case {self._details.get("CaseKey")}')
        return self._data.get('CaseKey')

    def get_details(self):
        logger.debug(f'Getting details for case {self._details.get("CaseNumber")}')
        return self._details

    def get_raw_data(self) -> dict:
        logger.debug(f'Getting raw data for case {self._details.get("CaseNumber")}')
        return {**self.get_data(), **self.get_details()}


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

    def find_by_case_number(self, case_num: str):
        if case_num in self._results.keys():
            logger.debug(f'Found SearchItem for case number {case_num}')
            return self._results.get(case_num)
        else:
            logger.debug(f'Could not find SearchItem for case number {case_num}')
            return None


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

    @classmethod
    def tidy_up(cls):
        del cls._driver
        del cls._instance

    def __del__(self):
        logger.debug('shutting down webdriver')
        self.get_driver().close()
        self.get_driver().quit()

    def get_driver(self):
        return self._driver

    def go(self, uri):
        logger.info(f'Navigating to url {uri}')
        self.get_driver().get(uri)
        return self

    def go_home(self):
        logger.debug(f'go to {URI.SEARCH}')
        self.get_driver().get(URI.SEARCH)
        return self

    def get_search_cases_response(self) -> list:
        requests = filter(lambda r: r.url == URI.SEARCH_CASES, self.get_driver().requests)
        return [r.response for r in requests]

    def get_search_result(self, case_num: str) -> SearchItem:
        logger.debug(f'Searching for single case with case number {case_num}')
        self.instance().go(URI.get_case_url_for_case_number(case_num))
        return self.get_search_results_from_network_requests().find_by_case_number(case_num)

    def get_detailed_case_info(self, case_item: SearchItem) -> CaseDetails:
        logger.debug(f'Getting details for case number {case_item.get_case_number()}')
        self.instance().go(URI.get_case_url(case_item.get_case_token()))
        return self.get_details_from_network_requests(case_item)

    def get_search_results_list(self, court_code: str, year_month: str) -> SearchResults:
        self.instance().go(URI.get_search_url_with_court_and_date(court_code, year_month))
        try:
            def check():
                running_total_selector = '#OD_BODY > div:nth-child(4) > table > tbody > tr > td.pad-all-0.va-bottom.text-right.width-30p.hidden-xs > div > div:nth-child(1) > span'
                running_total_regex = r'(?P<lower_current>\d*) to (?P<upper_current>\d*) of (?P<total>\d*)'

                running_total = WebDriverWait(self.get_driver(), DEFAULT_WAIT_TIME).until(
                    presence_of_element_located((By.CSS_SELECTOR, running_total_selector))
                )

                running_total_match = match(running_total_regex, running_total.text)

                if running_total_match is None:
                    logger.error('Cant find totals on screen, bailing out')
                    return True

                return running_total_match.groupdict()['upper_current'] == running_total_match.groupdict()['total']

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
            logger.exception(f'Timed out waiting on next button, assume we have all the cases and move on {ex}')
        except Exception as ex:
            logger.exception(f'{ex}')
        finally:
            return self.get_search_results_from_network_requests()

    def get_search_results_from_network_requests(self) -> SearchResults:
        filtered_requests = (
            filter(
                lambda r: r.response.status_code == 200 and match(URI.SEARCH_CASES_RE, r.url),
                self.instance().get_driver().requests
            )
        )
        results = SearchResults()
        for req in filtered_requests:
            json_body = loads(req.response.body)
            search_result_items = [SearchItem(d) for d in json_body.get('Results')]
            results.add_list(search_result_items)
            if json_body.get('TotalResults') == results.get_total():
                logger.info(f'Total number of {results.get_total()} cases collected')
        return results

    def get_details_from_network_requests(self, search_item: SearchItem) -> CaseDetails:
        try:
            req = self.instance().get_driver().wait_for_request(URI.CASE_SUMMARY_RE, MAX_TIMEOUT)
            details = loads(req.response.body)
            return CaseDetails(search_item, details)
        except TimeoutException as te:
            logger.exception(f'Timed out waiting for details for case {search_item.get_case_number()}: {te}')
        except Exception as ex:
            logger.exception(f'Failed to get details for case {search_item.get_case_number()}: {ex}')
