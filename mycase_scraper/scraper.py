from argparse import ArgumentParser, Namespace

from loguru import logger
from mysql.connector.errors import IntegrityError
from selenium.common.exceptions import TimeoutException

from db.persistence_builder import PersistenceBuilder, PersistenceStrategy
from settings import Settings
from utils.case import CaseDetails, SearchItem, SearchResults
from utils.driver import Driver


def get_persistence():
    return PersistenceBuilder.get_context(
        PersistenceStrategy(
            Settings.PERSISTENCE_STRATEGY.value.upper()
        )
    )


class Scraper:

    search_results: SearchResults = SearchResults()

    # collect search results

    @staticmethod
    def collect_search_results(search_term: str) -> SearchResults:
        return Driver.instance().get_search_results_list(search_term)

    # get details

    @staticmethod
    def persist_details_for_search_item(search_item):
        details = Scraper.get_detailed_case_for_search_item(search_item)
        details is not None and get_persistence().save_case(details)

    @staticmethod
    def get_detailed_case_for_search_item(case) -> CaseDetails:
        try:
            if case:
                return Driver.instance().get_detailed_case_info(case)
        except TimeoutException as tx:
            logger.exception(
                f'Timed out while trying to get details for case \'{case}\' : \'{tx}\'')
        except Exception as ex:
            logger.exception(
                f'Exception while trying to get details for case \'{case}\' : \'{ex}\'')

    @staticmethod
    def scrape_and_update(search_term: str):
        search_items: SearchResults = Scraper.collect_search_results(search_term)
        for search_item in search_items.values():
            Scraper.try_to_scrape_and_persist_details_for_search_item(search_item, True)

    @staticmethod
    def scrape_and_save(search_term: str):
        search_items: SearchResults = Scraper.collect_search_results(search_term)
        for search_item in search_items.values():
            Scraper.try_to_scrape_and_persist_details_for_search_item(search_item)

    @staticmethod
    def try_to_scrape_and_persist_details_for_search_item(search_item: SearchItem, update: bool = False):
        try:
            if update:
                details = Scraper.get_detailed_case_for_search_item(search_item)
                return details is not None and get_persistence().update_case(details)
            Scraper.persist_details_for_search_item(search_item)
        except IntegrityError as ie:
            logger.exception(f'Case already exists, skipping {ie}')


def get_parser():
    logger.debug('Setting up argument parsing')
    parser = ArgumentParser()

    # Scope of what to scrape
    parser.add_argument('-n', '--number', help='Case Number of single case to scrape', default=Settings.APP_DEFAULT_SEARCH_TERM.value)
    parser.add_argument('-a', '--active', help='Pull active cases from previous months', action='store_true')
    # parser.add_argument('-C', '--court', help='Five alpha numeric character code identifying the court to scrape from')
    # parser.add_argument('-F', '--court-filter', dest='filter', help='Filter by court type', default='')

    # Time range
    # parser.add_argument('-m', '--month', help='Month to focus on', default=get_current_month_as_str())
    # parser.add_argument('-y', '--year', help='year to focus on', default=get_current_year_as_str())

    # Type of case to scrape
    # parser.add_argument('-t', '--type', help='Type of cases to scrape', type=lambda c: Codes[c], choices=list(Codes),
    #                     default=Codes['EV'])
    return parser


def main(args: Namespace):
    logger.debug(f'Running with args: {args}')

    try:
        if args.active:
            # Collect active records for previous months
            active_cases: [CaseDetails] = get_persistence().get_active_cases_before_this_month()
            # Get and persist
            for case in active_cases:
                if case is not None and case.get_case_number() is not None:
                    return Scraper.scrape_and_update(case.get_case_number())
        elif args.number:
            if '*' not in args.number:
                case: CaseDetails = get_persistence().get_case_by_ucn(args.number)
                if not case:
                    return Scraper.scrape_and_save(args.number)
                elif case and case.get_is_active():
                    return Scraper.scrape_and_update(args.number)
            else:
                return Scraper.scrape_and_save(args.number)
    finally:
        Driver.tidy_up()


if __name__ == '__main__':
    main(get_parser().parse_args())
