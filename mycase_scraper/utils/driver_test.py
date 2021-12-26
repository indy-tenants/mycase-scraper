from unittest import TestCase
from mycase_scraper.utils.driver import Driver


class TestMyCaseDriver(TestCase):

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
        results = Driver.instance().get_results_list('49K01', 2101)
        self.assertEqual(301, results.get_total())
        self.assertTrue('49K01-2101-EV-000399' in results.keys())

    def test_get_detailed_case_results(self):
        details = Driver.instance().get_detailed_case_results(
            '49K01-2101-EV-000399'
        )
        self.assertEqual('', details)
