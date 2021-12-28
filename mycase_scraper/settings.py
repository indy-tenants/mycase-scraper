from enum import Enum
from os import getenv

from loguru import logger
from dotenv import load_dotenv

load_dotenv()


class Settings(Enum):

    GOOGLE_SERVICE_ACCOUNT_PATH = getenv('GOOGLE_SERVICE_ACCOUNT_PATH')
    GOOGLE_SPREADSHEETS_ID = getenv('GOOGLE_SPREADSHEETS_ID')
    PRIMARY_SHEET_NAME = getenv('PRIMARY_SHEET_NAME') or 'upcoming'
    ARCHIVE_SHEET_NAME = getenv('DATA_SHEET_NAME') or 'raw_data'
    CHROME_DEBUGGER_ADDRESS = getenv('CHROME_DEBUGGER_ADDRESS') or 9222
    CHROME_HEADLESS = getenv('CHROME_HEADLESS') or True


logger.debug(f'Using settings {Settings}')
