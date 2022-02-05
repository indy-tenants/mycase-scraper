from loguru import logger
from supabase.client import Client, create_client

from mycase_scraper.settings import Settings
from mycase_scraper.utils.case import CaseDetails
from mycase_scraper.utils.utils import ConfigFile


class SupabaseStrategy:

    key = None
    url = None
    config_file = None
    supabase = None
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logger.debug('Creating connection to supabase')
            cls._instance = super(SupabaseStrategy, cls).__new__(cls)
            try:
                cls.url: str = Settings.SUPABASE_URL.value
                cls.key: str = Settings.SUPABASE_SERVICE_ROLE_SECRET.value
                cls.config_file: ConfigFile = ConfigFile(Settings.APP_CONFIG_FILENAME.value)

                logger.debug(f'Attempting to connect to Supabase at url: \'{cls.url}\' with key \'{cls.key}\'')
                cls.supabase: Client = create_client(cls.url, cls.key)
                cls.user = cls.supabase.auth.sign_in(
                    email=cls.config_file.read().get('email'),
                    password=cls.config_file.read().get('password')
                )
            except Exception as ex:
                logger.exception(f'Could not authenticate {ex}')
        return cls._instance

    def save_cases(self, case_list: [CaseDetails]):
        responses = []
        for case in case_list:
            if case:
                responses.append(self.save_case(case))
        return responses

    def save_case(self, case: CaseDetails):
        try:
            responses = [self.supabase.table('case').upsert(case.get_case_dict_for_persistence()).execute()]

            for event in case.get_events_array_for_persistence():
                try:
                    logger.debug(f'parsing event \'{event}\'')
                    responses.append(self.supabase.table('event').upsert(event).execute())
                except AttributeError as ae:
                    logger.exception(f'Failed to extract item from data for event \'{event}\' : {ae}')
            for party in case.get_parties_array_for_persistence():
                try:
                    logger.debug(f'parsing party \'{party}\'')
                    responses.append(self.supabase.table('party').upsert(party).execute())
                except AttributeError as ae:
                    logger.exception(f'Failed to extract item from data for event \'{party}\' : {ae}')

            logger.debug(f'{[res for res in responses]}')
            return responses

        except AttributeError as ae:
            logger.exception(f'Failed to extract item from data for case \'{case}\' : {ae}')
        except Exception as ex:
            logger.exception(f'Failed to save case record \'{case}\'\n : {ex}')
