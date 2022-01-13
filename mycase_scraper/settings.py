from enum import Enum
from os import getenv
from os.path import abspath, dirname, join

from dotenv import load_dotenv
from loguru import logger

load_dotenv()


class Settings(Enum):
    # App Settings
    APP_HOME_DIRECTORY = dirname(abspath(__file__))
    APP_CONFIG_FILENAME = abspath(join(APP_HOME_DIRECTORY.value, 'config.json'))

    # Selenium
    CHROME_DEBUGGER_ADDRESS = getenv('CHROME_DEBUGGER_ADDRESS') or 9222
    CHROME_HEADLESS = getenv('CHROME_HEADLESS') or True

    # DB General
    PERSISTENCE_STRATEGY = getenv('PERSISTENCE_STRATEGY')

    # Google sheets
    GOOGLE_SERVICE_ACCOUNT_PATH = getenv('GOOGLE_SERVICE_ACCOUNT_PATH')
    GOOGLE_SPREADSHEETS_ID = getenv('GOOGLE_SPREADSHEETS_ID')
    PRIMARY_SHEET_NAME = getenv('PRIMARY_SHEET_NAME') or 'upcoming'
    ARCHIVE_SHEET_NAME = getenv('DATA_SHEET_NAME') or 'raw_data'

    # Supabase
    SUPABASE_URL = getenv('SUPABASE_URL')
    SUPABASE_KEY = getenv('SUPABASE_KEY')
    SUPABASE_SERVICE_ROLE_SECRET = getenv('SUPABASE_SERVICE_ROLE_SECRET')


logger.debug(f'Using settings {Settings}')
