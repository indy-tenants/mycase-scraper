from unittest import TestCase

from mycase_scraper.utils.case import CaseStatus, SearchItem
from mycase_scraper.utils.driver import Driver


class TestMyCaseDriver(TestCase):

    def tearDown(self) -> None:
        Driver.tidy_up()

    def test_go_home(self):
        Driver.instance().go_home()
        Driver.instance().get_driver().save_screenshot('./image.png')

    def test_get_network_traffic(self):
        Driver.instance().go_home()
        for request in Driver.instance().get_driver().requests:
            if request.response:
                print(
                    request.url,
                    request.response.status_code,
                    request.response.headers['Content-Type']
                )

    def test_get_cases_for_49K01_jan_2021(self):
        results = Driver.instance().get_search_results_list('49K01', 2101)
        self.assertEqual(301, results.get_total())
        self.assertTrue('49K01-2101-EV-000399' in results.keys())

    def test_get_search_result(self):
        result: SearchItem = Driver.instance().get_search_result('49K01-2101-EV-000399')
        self.assertEqual(40229763, result.get_int_field_from_data('CaseID'))
        self.assertIs(CaseStatus.DECIDED.value, result.get_str_field_from_data('CaseStatus'))
        self.assertEqual(False, result.get_is_active())

    def test_get_detailed_case_results(self):
        result: SearchItem = Driver.instance().get_search_result('49K01-2101-EV-000399')
        details = Driver.instance().get_detailed_case_info(result)
        self.assertEqual(result.get_int_field_from_data('CaseID'), details.get_case_key())
