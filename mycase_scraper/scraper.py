from argparse import ArgumentParser, Namespace

from loguru import logger
from selenium.common.exceptions import TimeoutException

from mycase_scraper.db.persistence_builder import PersistenceBuilder, PersistenceStrategy
from mycase_scraper.settings import Settings
from mycase_scraper.utils.case import CaseDetails, SearchItem, SearchResults
from mycase_scraper.utils.courts import courts_for_county
from mycase_scraper.utils.driver import Driver
from mycase_scraper.utils.utils import format_year_month, get_current_month_as_str, get_current_year_as_str


class Scraper:

    @staticmethod
    def run_for_county(args: Namespace):

        for court in courts_for_county(args.county):
            Scraper.run_for_court(args, court)

    @staticmethod
    def run_for_court(args, court) -> [CaseDetails]:
        try:
            Driver.instance().get_search_results_list(court, format_year_month(args.year, args.month))
            search_results: SearchResults = Driver.instance().get_search_results_from_network_requests()

            detailed_cases: [CaseDetails] = []
            for case in search_results.values():

                try:
                    if case:
                        detailed_cases.append(
                            Driver.instance().get_detailed_case_info(case)
                        )
                except TimeoutException as tx:
                    logger.exception(
                        f'Exception while trying to get details for case {case}: {tx}')
                except Exception as ex:
                    logger.exception(
                        f'Exception while trying to get details for case {case}: {ex}')

            return detailed_cases
        except Exception as ex:
            logger.exception(f'Exception while getting docket for {court} with args {args}: {ex}')

    @staticmethod
    def run_for_single_case_number(args: Namespace) -> CaseDetails:
        logger.debug(f'Searching for case number: \'{args.number}\'')
        search_item: SearchItem = Driver.instance().get_search_result(args.number)
        logger.debug(f'Getting case_details for case number \'{args.number}\'')
        case_details: CaseDetails = Driver.instance().get_detailed_case_info(search_item)
        logger.debug(f'Found case case_details \'{case_details.get_data() if case_details is not None else None}\'')
        return case_details


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
        if args.court:
            case_list: list = Scraper.run_for_court(args, args.court)
            return PersistenceBuilder.get_context(
                PersistenceStrategy(
                    Settings.PERSISTENCE_STRATEGY.value.upper()
                )
            ).save_cases(case_list)
        elif args.county:
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
