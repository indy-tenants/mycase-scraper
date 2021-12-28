from argparse import ArgumentParser, Namespace

from loguru import logger

from mycase_scraper.utils.driver import CaseDetails, Driver, SearchItem
from mycase_scraper.utils.utils import get_current_month_as_str, get_current_year_as_str


class Scraper:

    @staticmethod
    def run_for_county(args: Namespace):
        pass

    @staticmethod
    def run_for_single_case_number(args: Namespace):
        result: SearchItem = Driver.instance().get_search_result(args.number)
        details: CaseDetails = Driver.instance().get_detailed_case_info(result)


def get_parser():
    logger.debug('Setting up argument parsing')
    parser = ArgumentParser()

    # Scope of what to scrape
    parser.add_argument('-n', '--number', help='Case Number of single case to scrape')
    parser.add_argument('-c', '--county', help='Name of county to scrape, (Use quotes if there\'s a space)')

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
