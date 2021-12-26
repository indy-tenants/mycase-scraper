from unittest import TestCase

from settings import Settings
from sheets import Sheets


class TestSheets(TestCase):

    def test_init(self):
        sheets = Sheets(Settings)
        self.assertTrue(sheets.spreadsheet.get_sheets())

    def test_get_upcoming_sheet(self):
        self.fail()

    def test_get_decided_sheet(self):
        self.fail()
