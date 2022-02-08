from tinydb.database import TinyDB

from settings import Settings
from utils.case import CaseDetails


class TinyDBStrategy:

    def __init__(self):
        self.db = TinyDB(Settings.LIGHT_DB_PATH.value)

    def save_case(self, case: CaseDetails):
        self.db.upsert(case.get_data())

    def save_cases(self, cases: [CaseDetails]):
        map(self.save_case, cases)
