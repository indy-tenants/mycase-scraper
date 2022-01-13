from enum import Enum

from loguru import logger
from supabase.client import Client, create_client

from mycase_scraper.settings import Settings
from mycase_scraper.utils.utils import ConfigFile
from utils.case import CaseDetails


class PersistenceStrategy(Enum):
    SUPABASE = {}


class Persistence:

    def save_case(self, case: CaseDetails):
        pass


class SupabaseStrategy(Persistence):

    def __init__(self):
        try:
            self.url: str = Settings.SUPABASE_URL.value
            self.key: str = Settings.SUPABASE_SERVICE_ROLE_SECRET.value
            self.config_file: ConfigFile = ConfigFile(Settings.APP_CONFIG_FILENAME.value)

            logger.debug(f'Attempting to connect to Supabase at url: \'{self.url}\' with key \'{self.key}\'')
            self.supabase: Client = create_client(self.url, self.key)
            self.user = self.supabase.auth.sign_in(
                email=self.config_file.read().get('email'),
                password=self.config_file.read().get('password')
            )
        except Exception as ex:
            logger.exception(f'Could not authenticate {ex}')

    def save_case(self, case: CaseDetails):
        try:
            case_res = self.supabase.table('case').upsert(case.get_case_dict_for_persistence()).execute()
            # event_res = self.supabase.table('event').upsert(case.get_events_array_for_persistence()).execute()
            # party_res = self.supabase.table('party').upsert(case.get_parties_array_for_persistence()).execute()

        except Exception as ex:
            logger.exception(f'Failed to save case record \'{case.get_raw_data()}\'')


class PersistenceBuilder:

    @staticmethod
    def get_context(context: PersistenceStrategy):
        if context == PersistenceStrategy.SUPABASE:
            return SupabaseStrategy()
