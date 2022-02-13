from argparse import ArgumentParser, Namespace

from loguru import logger
from mysql.connector.errors import IntegrityError
from selenium.common.exceptions import TimeoutException

from db.persistence_builder import PersistenceBuilder, PersistenceStrategy
from settings import Settings
from utils.case import CaseDetails, SearchResults
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
    def collect_search_results(search_term: str) -> [SearchResults]:
        return Driver.instance().get_search_results_list(search_term)

    # get details

    @staticmethod
    def persist_details_for_search_results(search_results: SearchResults):
        for case in search_results.values():
            details = Scraper.get_detailed_case_for_search_item(case)
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

    # Persist

    @staticmethod
    def persist_case(case_details: CaseDetails):
        case_details is not None and get_persistence().save_case(case_details)

    @staticmethod
    def scrape(args):
        search_items: SearchResults = Scraper.collect_search_results(args.number)
        for search_item in search_items.values():
            try:
                case: CaseDetails = get_persistence().get_case(search_item.get_case_number())
                if case:
                    if case.get_is_active():
                        details = Scraper.get_detailed_case_for_search_item(search_item)
                        details is not None and get_persistence().update_case(details)
                else:
                    details = Scraper.get_detailed_case_for_search_item(search_item)
                    details is not None and get_persistence().save_case(details)
            except IntegrityError as ie:
                logger.exception(f'Case already exists, skipping {ie}')


def get_parser():
    logger.debug('Setting up argument parsing')
    parser = ArgumentParser()

    # Scope of what to scrape
    parser.add_argument('-n', '--number', help='Case Number of single case to scrape')
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
        if args.number:
            if '*' not in args.number:
                case: CaseDetails = get_persistence().get_case(args.number)
                if case and case.get_is_active():
                    return Scraper.scrape(args)
            else:
                return Scraper.scrape(args)
    finally:
        Driver.tidy_up()


if __name__ == '__main__':
    main(get_parser().parse_args())
