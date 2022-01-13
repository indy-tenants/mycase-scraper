from argparse import ArgumentParser, Namespace

from loguru import logger
from selenium.common.exceptions import TimeoutException

from db.persistence import PersistenceBuilder, PersistenceStrategy
from mycase_scraper.db.sheets import Sheets
from mycase_scraper.settings import Settings
from mycase_scraper.utils.courts import courts_for_county
from mycase_scraper.utils.driver import Driver
from mycase_scraper.utils.utils import format_year_month, get_current_month_as_str, get_current_year_as_str
from utils.case import CaseDetails, SearchItem, SearchResults


class Scraper:

    @staticmethod
    def run_for_county(args: Namespace):

        detailed_cases: [CaseDetails] = []

        for court in courts_for_county(args.county):

            try:

                Driver.instance().get_search_results_list(court, format_year_month(args.year, args.month))

            except Exception as ex:

                logger.exception(f'Exception while getting docket for {court} with args {args}: {ex}')

        search_results: SearchResults = Driver.instance().get_search_results_from_network_requests()

        for case in search_results.values():

            try:
                detailed_cases.append(
                    Driver.instance().get_detailed_case_info(case.get_data())
                )
            except TimeoutException as tx:
                logger.exception(
                    f'Exception while trying to get details for case {case}: {tx}')
            except Exception as ex:
                logger.exception(
                    f'Exception while trying to get details for case {case}: {ex}')

        sheets = Sheets(Settings)
        for details in detailed_cases:
            try:
                sheets.add_raw_data_for_case(details)
            except Exception as ex:
                logger.exception(
                    f'Could not add data for case {details.get_case_number()} to sheet {details.get_raw_data()} :{ex}')

    @staticmethod
    def run_for_single_case_number(args: Namespace):
        logger.debug(f'Searching for case number: \'{args.number}\'')
        result: SearchItem = Driver.instance().get_search_result(args.number)
        logger.debug(f'Getting details for case number \'{args.number}\'')
        details: CaseDetails = Driver.instance().get_detailed_case_info(result)
        logger.debug(f'Found case details \'{details.get_raw_data() or None}\'')
        return details


def get_parser():
    logger.debug('Setting up argument parsing')
    parser = ArgumentParser()

    # Scope of what to scrape
    parser.add_argument('-n', '--number', help='Case Number of single case to scrape')
    parser.add_argument('-c', '--county',
                        help='Two digit code of county to scrape, (counties found here: https://www.in.gov/courts/rules/admin/index.html#_Toc77764569)')
    parser.add_argument('-C', '--court', help='Five alpha numeric character code identifying the court to scrape from')

    # Time range
    parser.add_argument('-m', '--month', help='Month to focus on', default=get_current_month_as_str())
    parser.add_argument('-y', '--year', help='year to focus on', default=get_current_year_as_str())

    # Type of case to scrape
    # parser.add_argument('-t', '--type', help='Type of cases to scrape', type=lambda c: Codes[c], choices=list(Codes),
    #                     default=Codes['EV'])
    return parser


def main(args: Namespace):
    logger.debug(f'Running with args: {args}')

    try:
        if args.county:
            return Scraper.run_for_county(args)
        elif args.number:
            details: CaseDetails = Scraper.run_for_single_case_number(args)
            PersistenceBuilder.get_context(
                PersistenceStrategy(
                    Settings.PERSISTENCE_STRATEGY.value.upper()
                )
            ).save_case(details)
            return details
    finally:
        Driver.tidy_up()


if __name__ == '__main__':
    main(get_parser().parse_args())
