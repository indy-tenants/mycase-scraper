from argparse import ArgumentParser
from loguru import logger
from utils.infractions import Codes
from utils.utils import get_current_month_as_str, get_current_year_as_str


class Scraper:

    _instance = None
    _data = {}

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = Scraper()
        return cls._instance

    def scrape(self, args):
        pass

    def collect_ids_for_date_range(self):
        pass

    def run_as_daemon(self, args):
        pass


def get_parser():
    logger.debug("Setting up argument parsing")
    parser = ArgumentParser()
    parser.add_argument("-c", "--county", help="Scrape docket for county")
    parser.add_argument("-m", "--month", help="Month to focus on", default=get_current_month_as_str())
    parser.add_argument("-y", "--year", help="year to focus on", default=get_current_year_as_str())
    parser.add_argument("-t", "--type", help="Type of cases to scrape", type=lambda c: Codes[c], choices=list(Codes),
                        default=Codes["EV"])
    parser.add_argument("-d", "--daemon", help="Run as daemon", action="store_true", default=False)
    return parser


def main(args):
    logger.debug(f'Running with args: {args}')
    if args.daemon:
        Scraper.instance().run_as_daemon(args)
    else:
        Scraper.instance().scrape(args)


if __name__ == '__main__':
    main(get_parser().parse_args())
