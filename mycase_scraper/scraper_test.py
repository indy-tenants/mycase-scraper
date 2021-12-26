from unittest import TestCase, main
from scraper import get_parser
from utils.infractions import Codes
from utils.utils import get_current_year_as_str, get_current_month_as_str


class TestScraper(TestCase):

    def test_parser(self):
        single_county_run_args = ['-c', 'marion']
        single_county_run = get_parser().parse_args(single_county_run_args)
        self.assertEqual(Codes.EV                  , single_county_run.type          )
        self.assertEqual('marion'                  , single_county_run.county.lower())
        self.assertEqual(get_current_year_as_str() , single_county_run.year          )
        self.assertEqual(get_current_month_as_str(), single_county_run.month         )
        self.assertEqual(False                     , single_county_run.daemon        )


if __name__ == '__main__':
    main()
