from loguru import logger
from sheetfu.client import SpreadsheetApp
from sheetfu.model import Range
from sheetfu.modules.table import Table

from utils.case import CaseDetails, SearchItem


class Sheets:

    def __init__(self, settings):
        self.SETTINGS = settings

        logger.debug(
            f'Initializing sheets client with credentials from {self.SETTINGS.GOOGLE_SERVICE_ACCOUNT_PATH.value}'
            f' for sheet {self.SETTINGS.GOOGLE_SPREADSHEETS_ID.value}'
        )
        self.spreadsheet = SpreadsheetApp(self.SETTINGS.GOOGLE_SERVICE_ACCOUNT_PATH.value) \
            .open_by_id(self.SETTINGS.GOOGLE_SPREADSHEETS_ID.value)

        logger.debug('Checking that required sheets exist')
        sheet_names = [i.name for i in self.spreadsheet.get_sheets()]
        if self.SETTINGS.PRIMARY_SHEET_NAME.value not in sheet_names:
            logger.info(f'Creating new primary sheet called: {self.SETTINGS.PRIMARY_SHEET_NAME.value}')
            self.spreadsheet.create_sheets(self.SETTINGS.PRIMARY_SHEET_NAME.value)
            detailed_item: CaseDetails = CaseDetails(SearchItem({}))
            header_range: Range = self.spreadsheet.get_sheet_by_name(
                self.SETTINGS.PRIMARY_SHEET_NAME.value).get_range_from_a1(
                f'A1:{chr(64 + len(detailed_item.get_data().keys()))}1'
            )
            header_range.set_values(
                [
                    [value for value in detailed_item.get_data().keys()]
                ]
            )
        if self.SETTINGS.ARCHIVE_SHEET_NAME.value not in sheet_names:
            logger.info(f'Creating new archive sheet called: {self.SETTINGS.ARCHIVE_SHEET_NAME.value}')
            self.spreadsheet.create_sheets(self.SETTINGS.ARCHIVE_SHEET_NAME.value)
            detailed_item: CaseDetails = CaseDetails(SearchItem({}))
            header_range: Range = self.spreadsheet.get_sheet_by_name(
                self.SETTINGS.ARCHIVE_SHEET_NAME.value).get_range_from_a1(
                f'A1:{chr(64 + len(detailed_item.get_data().keys()))}1'
            )
            header_range.set_values(
                [
                    [value for value in detailed_item.get_data().keys()]
                ]
            )

    def add_raw_data_for_case(self, data: CaseDetails):
        table = Table.get_table_from_sheet(
            spreadsheet=self.spreadsheet,
            sheet_name=self.SETTINGS.ARCHIVE_SHEET_NAME.value
        )
        table.add_one(data.get_data())
        table.commit()
