from enum import Enum

from mycase_scraper.db.models import Sqlite3Strategy
from mycase_scraper.db.supabase_strategy import SupabaseStrategy
from mycase_scraper.db.tdb_strategy import TinyDBStrategy


class PersistenceStrategy(Enum):
    SUPABASE = 'SUPABASE'
    SQLITE3 = 'SQLITE3'
    TINYDB = 'TINYDB'
    JSON = 'JSON'


class PersistenceBuilder:

    @staticmethod
    def get_context(context: PersistenceStrategy):
        if context == PersistenceStrategy.SUPABASE:
            return SupabaseStrategy()
        if context == PersistenceStrategy.SQLITE3:
            return Sqlite3Strategy()
        if context == PersistenceStrategy.TINYDB:
            return TinyDBStrategy()
        # if context == PersistenceStrategy.JSON:
        #     return JSONStrategy()
