from enum import Enum
from os import getenv
from os.path import abspath, dirname, join

from dotenv import load_dotenv
from loguru import logger

load_dotenv()


class Settings(Enum):

    # App Settings
    APP_HOME_DIRECTORY = dirname(abspath(__file__))
    APP_CONFIG_FILENAME = abspath(join(APP_HOME_DIRECTORY, 'config.json'))

    # Selenium
    CHROME_DEBUGGER_ADDRESS = getenv('CHROME_DEBUGGER_ADDRESS') or 9222
    CHROME_HEADLESS = getenv('CHROME_HEADLESS') or True

    # DB General
    PERSISTENCE_STRATEGY = getenv('PERSISTENCE_STRATEGY').upper() or 'LIGHT_DB'

    # Google sheets
    GOOGLE_SERVICE_ACCOUNT_PATH = getenv('GOOGLE_SERVICE_ACCOUNT_PATH')
    GOOGLE_SPREADSHEETS_ID = getenv('GOOGLE_SPREADSHEETS_ID')
    PRIMARY_SHEET_NAME = getenv('PRIMARY_SHEET_NAME') or 'upcoming'
    ARCHIVE_SHEET_NAME = getenv('DATA_SHEET_NAME') or 'raw_data'

    # Supabase
    SUPABASE_URL = getenv('SUPABASE_URL')
    SUPABASE_KEY = getenv('SUPABASE_KEY')
    SUPABASE_SERVICE_ROLE_SECRET = getenv('SUPABASE_SERVICE_ROLE_SECRET')

    # Sqlite3
    SQLITE3_FILE_NAME = join(APP_HOME_DIRECTORY, 'db.sqlite3')

    LIGHT_DB_PATH = getenv('LIGHT_DB_PATH') or join(APP_HOME_DIRECTORY, 'tinydb.json')


logger.debug(f'Using settings {Settings}')
