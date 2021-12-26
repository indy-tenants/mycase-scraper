from loguru import logger
from sheetfu.client import SpreadsheetApp


class Sheets:

    def __init__(self, settings):
        self.SETTINGS = settings

        logger.debug(
            f'Initializing sheets client with credentials from {self.SETTINGS.GOOGLE_SERVICE_ACCOUNT_PATH}'
            f' for sheet {self.SETTINGS.GOOGLE_SPREADSHEETS_ID}'
        )
        self.spreadsheet = SpreadsheetApp(self.SETTINGS.GOOGLE_SERVICE_ACCOUNT_PATH)\
            .open_by_id(self.SETTINGS.GOOGLE_SPREADSHEETS_ID)

        logger.debug('Checking that required sheets exist')
        sheet_names = [i.name for i in self.spreadsheet.get_sheets()]
        if self.SETTINGS.PRIMARY_SHEET_NAME not in sheet_names:
            logger.info(f'Creating new primary sheet called: {self.SETTINGS.PRIMARY_SHEET_NAME}')
            self.spreadsheet.create_sheets(self.SETTINGS.PRIMARY_SHEET_NAME)
        if self.SETTINGS.ARCHIVE_SHEET_NAME not in sheet_names:
            logger.info(f'Creating new archive sheet called: {self.SETTINGS.ARCHIVE_SHEET_NAME}')
            self.spreadsheet.create_sheets(self.SETTINGS.ARCHIVE_SHEET_NAME)
