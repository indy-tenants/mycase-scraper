from base64 import b64decode
from base64 import b64encode
from json import dumps
from json import loads

from loguru import logger


class URI:

    BASE = 'https://public.courts.in.gov/mycase/'
    SEARCH = BASE + '#/vw/Search'
    SEARCH_RESULTS = BASE + '#/vw/SearchResults/{}'
    CASE_SUMMARY = BASE + '#/vw/CaseSummary/{}'
    CASE_SUMMARY_RE = r'.*public\.courts\.in\.gov\/mycase\/Case\/CaseSummary\?CaseToken.*'
    SEARCH_CASES = BASE + 'Search/SearchCases'
    SEARCH_CASES_RE = r'.*public\.courts\.in\.gov\/mycase\/Search\/SearchCases.*'

    @staticmethod
    def decode_slug(s):
        logger.debug(f'Decoding {s}')
        return loads(b64decode(s))

    @staticmethod
    def encode_slug(s):
        logger.debug(f'Encoding {s}')
        return b64encode(str.encode(dumps(s))).decode('utf-8')

    @classmethod
    def get_case_url(cls, case_token):
        logger.debug(f'Creating case summary url for {case_token}')
        data = {
            'v': {
                'CaseToken': f'{case_token}'
            }
        }
        return cls.CASE_SUMMARY.format(
            cls.encode_slug(
                data
            )
        )

    @classmethod
    def get_case_url_for_case_number(cls, case_num: str):
        logger.debug(f'Creating search result url for case number {case_num}')
        return cls.get_search_url_with_data({'CaseNum': case_num})

    @classmethod
    def get_search_url_with_court_and_date(cls, court, date):
        logger.debug(f'Creating search result url for {court} on {date}')
        return cls.get_search_url_with_data({'CaseNum': f'{court}-{date}-EV-*'})

    @classmethod
    def get_search_url_with_data(cls, data: {}):
        logger.debug(f'Creating search result url with data {data}')
        slug = {
            'v': {
                'Mode': 'ByCase', 'CaseNum': data.get('CaseNum'), 'CiteNum': None, 'CrossRefNum': None, 'First': None,
                'Middle': None, 'Last': None, 'Business': None, 'DoBStart': None, 'DoBEnd': None, 'OANum': None,
                'BarNum': None, 'SoundEx': False, 'CourtItemID': None, 'Categories': None, 'Limits': None,
                'Advanced': False, 'ActiveFlag': 'All', 'FileStart': None, 'FileEnd': None, 'CountyCode': None
            }
        }
        return cls.SEARCH_RESULTS.format(
            cls.encode_slug(
                slug
            )
        )
