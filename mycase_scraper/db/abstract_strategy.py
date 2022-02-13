from utils.case import CaseDetails


class AbstractPersistenceStrategy:

    def save_case(self, case: CaseDetails):
        pass

    def update_case(self, case: CaseDetails):
        pass

    def get_case_by_ucn(self, ucn: str) -> CaseDetails:
        pass
