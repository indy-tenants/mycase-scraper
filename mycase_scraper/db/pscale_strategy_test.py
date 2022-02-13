from os.path import join
from unittest import TestCase

from db.pscale_strategy import PScaleStrategy
from settings import Settings
from utils.case import CaseDetails, SearchItem
from utils.utils import read_json_from_file


class TestPScaleStrategy(TestCase):

    def test_save_case(self):
        example_case = CaseDetails(SearchItem(read_json_from_file(join(
             Settings.APP_HOME_DIRECTORY.value, 'db/example_data/49K01-2201-EV-ABCDEF.json'
        ))))
        PScaleStrategy().save_case(example_case)
        blob = PScaleStrategy().get_case_by_ucn('49K01-2201-EV-ABCDEF')
        self.assertIsNotNone(blob)

    def test_update_case(self):
        example_case = CaseDetails(SearchItem(read_json_from_file(join(
            Settings.APP_HOME_DIRECTORY.value, 'db/example_data/49K01-2201-EV-ABCDEF.updated.json'
        ))))
        PScaleStrategy().update_case(example_case)
        blob = PScaleStrategy().get_case_by_ucn('49K01-2201-EV-ABCDEF')
        self.assertIsNotNone(blob)

    def test_get_case(self):
        cd = CaseDetails(
            SearchItem(
                PScaleStrategy().get_case_by_ucn('49K01-2201-EV-ABCDEF').pop()
            )
        )
        self.assertIsNotNone(cd)
