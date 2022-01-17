from enum import Enum

from mycase_scraper.db.models import Sqlite3Strategy
from mycase_scraper.db.supabase import SupabaseStrategy


class PersistenceStrategy(Enum):
    SUPABASE = 'SUPABASE'
    SQLITE3 = 'SQLITE3'


class PersistenceBuilder:

    @staticmethod
    def get_context(context: PersistenceStrategy):
        if context == PersistenceStrategy.SUPABASE:
            return SupabaseStrategy()
        if context == PersistenceStrategy.SQLITE3:
            return Sqlite3Strategy()
