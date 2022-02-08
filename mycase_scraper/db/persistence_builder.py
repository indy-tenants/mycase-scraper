from enum import Enum

from .models import Sqlite3Strategy
from .supabase_strategy import SupabaseStrategy
from .tdb_strategy import TinyDBStrategy


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
