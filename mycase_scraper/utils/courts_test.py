from unittest import TestCase

from mycase_scraper.utils.courts import courts_for_county


class TestCourts(TestCase):

    def test_courts_for_county(self):
        adam_county_courts = courts_for_county('01')
        self.assertEqual(
            ['01C01', '01D01'],
            adam_county_courts
        )

        bartholomew_county_courts = courts_for_county('03')
        self.assertEqual(
            ['03C01', '03D01', '03D02'],
            bartholomew_county_courts
        )

        porter_county_courts = courts_for_county('64')
        self.assertEqual(
            ['64C01', '64D01', '64D02', '64D03', '64D04', '64D05', '64D06', '64E01', '64I01'],
            porter_county_courts
        )
