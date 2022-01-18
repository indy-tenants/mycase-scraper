from unittest import TestCase, main

from mycase_scraper.scraper import get_parser, main as app_main
from mycase_scraper.utils.utils import get_current_month_as_str, get_current_year_as_str


class TestScraper(TestCase):

    def test_parser(self):
        single_county_run_args = ['-c', '49']
        single_county_run = get_parser().parse_args(single_county_run_args)
        self.assertEqual(49, int(single_county_run.county))
        self.assertEqual(get_current_year_as_str(), single_county_run.year)
        self.assertEqual(get_current_month_as_str(), single_county_run.month)

    def test_run_for_single_case_number(self):
        single_case_number_args = ['-n', '49K01-2101-EV-000399']
        output = app_main(get_parser().parse_args(single_case_number_args))
        self.assertIsNotNone(output)

    def test_run_for_court(self):
        single_county_run_args = ['-C', '49K07', '-y', '22', '-m', '1']
        output = app_main(get_parser().parse_args(single_county_run_args))
        self.assertIsNotNone(output)

    def test_run_for_county(self):
        single_county_run_args = ['-c', '49', '-y', '21', '-m', '1']
        output = app_main(get_parser().parse_args(single_county_run_args))
        self.assertIsNotNone(output)


if __name__ == '__main__':
    main()
