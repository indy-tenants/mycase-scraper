from ctypes import Union
from unittest import TestCase

from gotrue.types import Session, User
from loguru import logger
from supabase.client import Client, create_client

from db.persistence import SupabaseStrategy
from mycase_scraper.utils.utils import ConfigFile
from settings import Settings


class TestSupabase(TestCase):

    def test_init(self):
        self.instance = SupabaseStrategy()
        self.assertIsNotNone(self.instance)

    def test_create_user(self):
        config_file: ConfigFile = ConfigFile(Settings.APP_CONFIG_FILENAME.value)
        self.url: str = Settings.SUPABASE_URL.value
        self.key: str = Settings.SUPABASE_KEY.value
        self.supabase: Client = create_client(self.url, self.key)
        self.user: Union[Session, User] = self.supabase.auth.sign_up(
            email=config_file.read().get('email'),
            password=config_file.read().get('password')
        )
        logger.info(self.user)
        self.assertIsNotNone(self.user)
