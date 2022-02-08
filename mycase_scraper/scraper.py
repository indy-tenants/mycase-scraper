from argparse import ArgumentParser, Namespace

from loguru import logger
from selenium.common.exceptions import TimeoutException

from db.persistence_builder import PersistenceBuilder, PersistenceStrategy
from settings import Settings
from utils.case import CaseDetails, SearchItem, SearchResults
from utils.courts import courts_for_county
from utils.driver import Driver
from utils.utils import format_year_month, get_current_month_as_str, get_current_year_as_str


class Scraper:

    search_results: SearchResults = SearchResults()

    def run_for_county(self, args: Namespace, court_type_filter) -> list[CaseDetails]:
        try:
            for court in courts_for_county(args.county, court_type_filter=court_type_filter):
                self.get_search_results_from_court(court, format_year_month(args.year, args.month))

            logger.info(f'Getting details for \'{self.search_results.get_total()}\' search results')
            return self.get_details_for_search_results(
                self.search_results
            )
        except Exception as ex:
            logger.exception(f'Exception while getting cases for county \'{args.county}\' with args {args}: {ex}')

    def get_search_results_from_court(self, court_code: str, ymonth: str):
        try:
            Driver.instance().navigate_search_results_for_court(court_code, ymonth)
            self.search_results.add_list(
                Driver.instance().get_search_results_from_network_requests().values()
            )
        except Exception as Ex:
            logger.exception(f'Something went wrong {Ex}')
        finally:
            pass

    def run_for_court(self, args: Namespace) -> list[CaseDetails]:
        try:
            self.search_results.add_list(
                Driver.instance().get_search_results_list(
                    args.court,
                    format_year_month(args.year, args.month)
                ).values()
            )

            logger.info(f'Getting details for \'{self.search_results.get_total()}\' search results')
            return self.get_details_for_search_results(
                self.search_results
            )

        except Exception as ex:
            logger.exception(f'Exception while getting docket for {args.court} with args {args}: {ex}')

    @staticmethod
    def get_details_for_search_results(search_results: SearchResults) -> list[CaseDetails]:
        detailed_cases: [CaseDetails] = list()
        for case in search_results.values():
            try:
                if case:
                    detailed_cases.append(
                        Driver.instance().get_detailed_case_info(case)
                    )
            except TimeoutException as tx:
                logger.exception(
                    f'Exception while trying to get details for case \'{case}\' : \'{tx}\'')
            except Exception as ex:
                logger.exception(
                    f'Exception while trying to get details for case \'{case}\' : \'{ex}\'')
        return detailed_cases

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
    parser.add_argument('-F', '--court-filter', dest='filter', help='Filter by court type', default='')

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
            case_list: list[CaseDetails] = Scraper().run_for_court(args)
            return PersistenceBuilder.get_context(
                PersistenceStrategy(
                    Settings.PERSISTENCE_STRATEGY.value.upper()
                )
            ).save_cases(case_list)
        elif args.county:
            case_list: list[CaseDetails] = Scraper().run_for_county(
                args,
                court_type_filter=lambda c: args.filter.lower() in c.lower()
            )
            return PersistenceBuilder.get_context(
                PersistenceStrategy(
                    Settings.PERSISTENCE_STRATEGY.value.upper()
                )
            ).save_cases(case_list)
        elif args.number:
            details: CaseDetails = Scraper.run_for_single_case_number(args)
            return PersistenceBuilder.get_context(
                PersistenceStrategy(
                    Settings.PERSISTENCE_STRATEGY.value.upper()
                )
            ).save_case(details)
    finally:
        Driver.tidy_up()


if __name__ == '__main__':
    main(get_parser().parse_args())
