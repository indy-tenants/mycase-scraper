from enum import Enum

from .pscale_strategy import PScaleStrategy
from .sqlite_strategy import Sqlite3Strategy


class PersistenceStrategy(Enum):
    PSCALE = 'PSCALE'
    SQLITE3 = 'SQLITE3'


class PersistenceBuilder:

    @staticmethod
    def get_context(context: PersistenceStrategy):
        if context == PersistenceStrategy.PSCALE:
            return PScaleStrategy()
        if context == PersistenceStrategy.SQLITE3:
            return Sqlite3Strategy()
