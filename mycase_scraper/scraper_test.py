from unittest import TestCase, main

from mycase_scraper.scraper import get_parser, main as app_main
from mycase_scraper.utils.infractions import Codes
from mycase_scraper.utils.utils import get_current_month_as_str, get_current_year_as_str


class TestScraper(TestCase):

    def test_parser(self):
        single_county_run_args = ['-c', 'Marion']
        single_county_run = get_parser().parse_args(single_county_run_args)
        self.assertEqual(Codes.EV, single_county_run.type)
        self.assertEqual('marion', single_county_run.county.lower())
        self.assertEqual(get_current_year_as_str(), single_county_run.year)
        self.assertEqual(get_current_month_as_str(), single_county_run.month)
        self.assertEqual(False, single_county_run.daemon)

    def test_run_for_county(self):
        single_county_run_args = ['-c', 'marion', '-y', '21', '-m', '1']
        output = app_main(get_parser().parse_args(single_county_run_args))
        self.assertIsNotNone(output)

    def test_run_for_single_case_number(self):
        single_case_number_args = ['-n', '49K01-2101-EV-000399']
        output = app_main(get_parser().parse_args(single_case_number_args))
        self.assertIsNotNone(output)


if __name__ == '__main__':
    main()
