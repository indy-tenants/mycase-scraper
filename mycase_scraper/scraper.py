from argparse import ArgumentParser, Namespace

from loguru import logger
from selenium.common.exceptions import TimeoutException

from mycase_scraper.db.sheets import Sheets
from mycase_scraper.settings import Settings
from mycase_scraper.utils.courts import courts_for_county
from mycase_scraper.utils.driver import CaseDetails, Driver, SearchItem, SearchResults
from mycase_scraper.utils.utils import format_year_month, get_current_month_as_str, get_current_year_as_str


class Scraper:

    @staticmethod
    def run_for_county(args: Namespace):

        detailed_cases: [CaseDetails] = []
        for court in courts_for_county(args.county):
            try:
                search_results: SearchResults = Driver.instance().get_driver().get_search_results_list(
                    court,
                    format_year_month(args.year, args.month)
                )
                for case in search_results.values():
                    try:
                        detailed_cases.append(
                            Driver.instance().get_driver().get_detailed_case_info(case)
                        )
                    except TimeoutException as tx:
                        logger.exception(
                            f'Exception while trying to get details for case {case.get_case_number()}: {tx}')
                    except Exception as ex:
                        logger.exception(
                            f'Exception while trying to get details for case {case.get_case_number()}: {ex}')
            except Exception as ex:
                logger.exception(f'Exception while getting docket for {court} with args {args}: {ex}')

        sheets = Sheets(Settings)
        for details in detailed_cases:
            try:
                sheets.add_raw_data_for_case(details)
            except Exception as ex:
                logger.exception(
                    f'Could not add data for case {details.get_case_number()} to sheet {details.get_raw_data()} :{ex}')

    @staticmethod
    def run_for_single_case_number(args: Namespace):
        result: SearchItem = Driver.instance().get_search_result(args.number)
        details: CaseDetails = Driver.instance().get_detailed_case_info(result)


def get_parser():
    logger.debug('Setting up argument parsing')
    parser = ArgumentParser()

    # Scope of what to scrape
    parser.add_argument('-n', '--number', help='Case Number of single case to scrape')
    parser.add_argument('-c', '--county',
                        help='Two digit code of county to scrape, (counties found here: https://www.in.gov/courts/rules/admin/index.html#_Toc77764569)')

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
            return Scraper.run_for_single_case_number(args)
    finally:
        Driver.tidy_up()


if __name__ == '__main__':
    main(get_parser().parse_args())
