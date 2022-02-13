from enum import Enum
from os import getenv
from os.path import abspath, dirname, join

from dotenv import load_dotenv

from utils.utils import format_year_month, get_current_month_as_str, get_current_year_as_str

load_dotenv()


class Settings(Enum):

    # App Settings
    APP_HOME_DIRECTORY = dirname(abspath(__file__))
    APP_CONFIG_FILENAME = abspath(join(APP_HOME_DIRECTORY, 'config.json')) # noqa

    APP_DEFAULT_SEARCH_TERM = f'49K01-{format_year_month(get_current_year_as_str(), get_current_month_as_str())}-EV-*'

    # Selenium
    CHROME_DEBUGGER_ADDRESS = getenv('CHROME_DEBUGGER_ADDRESS') or 9222
    CHROME_HEADLESS = getenv('CHROME_HEADLESS') or True

    # DB General
    PERSISTENCE_SCHEMA_NAME = 'mcsdata'
    PERSISTENCE_PARTY_TABLE = 'my_case_party'
    PERSISTENCE_EVENT_TABLE = 'my_case_event'
    PERSISTENCE_CASE_TABLE = 'my_case_details'
    PERSISTENCE_STRATEGY = getenv('PERSISTENCE_STRATEGY').upper() or 'SQLITE'
    PERSISTENCE_HOST = getenv('PERSISTENCE_HOST')
    PERSISTENCE_USER = getenv('PERSISTENCE_USER')
    PERSISTENCE_PASSWORD = getenv('PERSISTENCE_PASSWORD')
    PERSISTENCE_PORT = getenv('PERSISTENCE_PORT')

    # Sqlite3
    SQLITE3_FILE_NAME = join(APP_HOME_DIRECTORY, 'db.sqlite3') # noqa
