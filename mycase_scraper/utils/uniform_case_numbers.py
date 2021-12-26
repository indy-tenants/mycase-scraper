from re import match
from loguru import logger
from datetime import date


class UniformCaseNumber:

    def __init__(self, county_code: int, court_type: str, court_number: int, month: date, if_code: str,
                 case_number: int):
        logger.debug(f'initializing UniformCaseNumber {case_number}')
        self.county_code = county_code
        self.court_type = court_type
        self.court_number = court_number
        self.year = date.year
        self.month = month.month
        self.infraction_code = if_code
        self.case_number = case_number

    @staticmethod
    def from_string(ucn: str):
        logger.debug(f'parsing UniformCaseNumber {ucn}')
        case_num = match(r'(?P<a>\d{2})(?P<b>\D)(?P<c>\d{2})-(?P<d>\d{2})(?P<e>\d{2})-(?P<f>\D{2})-(?P<g>\d{6})', ucn)
        return UniformCaseNumber(
            int(case_num.groupdict().get('a')),
            case_num.groupdict().get('b'),
            int(case_num.groupdict().get('c')),
            date(int(case_num.groupdict().get('d')), int(case_num.groupdict().get('e')), 1),
            case_num.groupdict().get('f'),
            int(case_num.groupdict().get('g')),
        )

    def to_string(self):
        return f'{self.county_code}{self.court_type.upper()}{self.court_number}-{self.year}{self.month}-{self.infraction_code}-{self.case_number}'
