from datetime import date, time
from enum import Enum
from typing import Callable, Union

from dateutil.parser import parse
from loguru import logger


class CaseStatus(Enum):
    DECIDED = 'Decided'
    PENDING = 'Pending'

    def __str__(self):
        return self.value


class AbstractDataParser:

    _data: dict = {}

    # generic getter's for search data with type checking

    def get_type_field_from_data(self, field: str, func: Callable = lambda x: x) -> Union[bool, date, dict, int, list, str, time]:
        value = self._data.get(field)
        logger.debug(f'Getting {field} \'{value}\'')
        return None if value is None else func(value)

    def get_bool_field_from_data(self, field: str) -> bool:
        return self.get_type_field_from_data(field, bool)

    def get_date_field_from_data(self, field: str) -> date:
        return self.get_type_field_from_data(field, lambda x: None if x is None else parse(x).date())

    def get_dict_field_from_data(self, field: str) -> date:
        return self.get_type_field_from_data(field, dict)

    def get_int_field_from_data(self, field: str) -> int:
        return self.get_type_field_from_data(field, int)

    def get_list_field_from_data(self, field: str) -> date:
        return self.get_type_field_from_data(field, list)

    def get_str_field_from_data(self, field: str) -> str:
        return self.get_type_field_from_data(field, str)

    def get_time_field_from_data(self, field: str) -> time:
        return self.get_type_field_from_data(field, lambda x: None if x is None else time(x))


class SearchItem(AbstractDataParser):

    def __init__(self, data):
        self._data = data

    def __str__(self):
        return str(self._data)

    def get_data(self) -> dict:
        logger.debug(f'Getting data from SearchItem of case {self.get_case_number()}')
        return self._data

    def get_is_active(self) -> bool:
        is_active: bool = self.get_bool_field_from_data('IsActive')
        return is_active if type(is_active) == bool else is_active == 'active'

    def get_id(self) -> int:
        return self.get_int_field_from_data('CaseID')

    def get_file_date(self) -> date:
        return self.get_date_field_from_data('FileDate')

    def get_case_status_date(self) -> date:
        return self.get_date_field_from_data('CaseStatusDate')

    def get_case_status(self) -> CaseStatus:
        return CaseStatus(self.get_str_field_from_data('CaseStatus'))

    def get_case_number(self) -> str:
        return self.get_str_field_from_data('CaseNumber')

    def get_case_token(self) -> str:
        return self.get_str_field_from_data('CaseToken')

    def get_style(self) -> str:
        return self.get_str_field_from_data('Style')


class CaseEvent(AbstractDataParser):

    # This is the shape of the data

    _data: dict = {
        'EventKey'         : None,
        'CaseKey'          : None,
        'BaseEventType'    : None,
        'BaseEventTypeKey' : None,
        'EventType'        : None,
        'EventDate'        : None,
        'EventTime'        : None,
        'Description'      : None,
        'Judge'            : None,
        'EventVolume'      : None,
        'EventPage'        : None,
        'NumberOfPages'    : None,
        'IsDocketable'     : None,
        'EventDocuments'   : None,
        'CaseEvent'        : None,
        'DispEvent'        : None,
        'HearingEvent'     : None,
        'JEvent'           : None,
        'SEvent'           : None,
        'VEvent'           : None,
        'AEvent'           : None,
    }

    def __init__(self, data: dict):
        self._data: dict = data

    def get_dict_for_persistence(self):
        return {
            'pk_event_id'   : self.get_int_field_from_data('EventKey'),
            'fk_case_id'    : self.get_int_field_from_data('CaseKey'),
            'event_type'    : self.get_str_field_from_data('EventType'),
            'event_date'    : self.get_date_field_from_data('EventDate'),
            'event_time'    : self.get_time_field_from_data('EventTime'),
            'description'   : self.get_str_field_from_data('Description'),
            'judge'         : self.get_str_field_from_data('Judge'),
            'case_event'    : self.get_dict_field_from_data('CaseEvent'),
            'hearing_event' : self.get_dict_field_from_data('HearingEvent'),
            'disp_event'    : self.get_dict_field_from_data('DispEvent'),
            'j_event'       : self.get_dict_field_from_data('JEvent'),
            's_event'       : self.get_dict_field_from_data('SEvent'),
            'v_event'       : self.get_dict_field_from_data('VEvent'),
            'a_event'       : self.get_dict_field_from_data('AEvent'),
        }


class CaseParty(AbstractDataParser):

    # This is the shape of the data

    _party_data: dict = {
        'CasePartyKey'       : None,
        'CaseKey'            : None,
        'PartyKey'           : None,
        'RestrictPublicView' : None,
        'Connection'         : None,
        'BaseConnKey'        : None,
        'ExtConnCode'        : None,
        'ExtConnCodeDesc'    : None,
        'ActiveWarrants'     : None,
        'Description'        : None,
        'Name'               : None,
        'ExtendedName'       : None,
        'DOB'                : None,
        'DOD'                : None,
        'Address'            : None,
        'FeePayURL'          : None,
        'RemovedDate'        : None,
        'RemovedReason'      : None,
        'Attorneys'          : None,
        'OANs'               : None,
        'FeeSummary'         : None,
        'Transactions'       : None,
    }

    def get_dict_for_persistence(self):
        return {
            'pk_case_party_id'    : self.get_int_field_from_data('CasePartyKey'),
            'party_id'            : self.get_int_field_from_data('PartyKey'),
            'fk_case_id'          : self.get_int_field_from_data('CaseKey'),
            'base_connection_key' : self.get_str_field_from_data('BaseConnKey'),
            'name'                : self.get_str_field_from_data('Name'),
            'extended_name'       : self.get_str_field_from_data('ExtendedName'),
            'dob'                 : self.get_date_field_from_data('DOB'),
            'address'             : self.get_dict_field_from_data('Address'),
            'removed_date'        : self.get_date_field_from_data('RemovedDate'),
            'removed_reason'      : self.get_str_field_from_data('RemovedReason'),
            'attorney'            : self.get_dict_field_from_data('Attorneys'),
        }


class CaseDetails(SearchItem):

    # This is the shape of the data

    _detailed_case_data: dict = {
        'InvalidToken'      : None,
        'CaseKey'           : None,
        'CaseCategoryKey'   : None,
        'CaseCategoryGroup' : None,
        'CaseNumber'        : None,
        'Court'             : None,
        'CourtCode'         : None,
        'CountyCode'        : None,
        'IsAppellateCourt'  : None,
        'FileDate'          : None,
        'CaseStatus'        : None,
        'CaseStatusDate'    : None,
        'CaseType'          : None,
        'CaseTypeCode'      : None,
        'CaseSubType'       : None,
        'Style'             : None,
        'IsActive'          : None,
        'IsPublic'          : None,
        'AppearByDate'      : None,
        'Bonds'             : None,
        'Charges'           : None,
        'Events'            : None,
        'Parties'           : None,
        'CrossRefs'         : None,
        'Related'           : None,
        'CommCourtFlag'     : None,
    }

    def __init__(self, search_item: SearchItem, details=None):
        super(CaseDetails, self).__init__(search_item.get_data())
        self.add_details(details or {})

    def add_details(self, details: dict):
        if 'InvalidToken' in details and details.get('InvalidToken') is False:
            self._detailed_case_data.update(details)
        return self

    def get_details(self):
        logger.debug(f'Getting details for case {self._detailed_case_data.get("CaseNumber")}')
        return self._detailed_case_data

    def get_raw_data(self) -> dict:
        logger.debug(f'Getting raw data for case {self._detailed_case_data.get("CaseNumber")}')
        return {**self.get_details(), **self.get_data()}

    # generic getter's for search data with type checking

    def get_bool_field_from_detailed_case_data(self, field: str) -> bool:
        logger.debug(f'Getting {field} {self._detailed_case_data.get(field)}')
        return self._detailed_case_data.get(field)

    def get_date_field_from_detailed_case_data(self, field: str) -> date:
        logger.debug(f'Getting {field} \'{self._detailed_case_data.get(field)}\'')
        return parse(self._detailed_case_data.get(field)).date()

    def get_int_field_from_detailed_case_data(self, field: str) -> int:
        logger.debug(f'Getting {field} {self._detailed_case_data.get(field)}')
        return int(self._detailed_case_data.get(field))

    def get_str_field_from_detailed_case_data(self, field: str) -> str:
        logger.debug(f'Getting {field} {self._detailed_case_data.get(field)}')
        return str(self._detailed_case_data.get(field))

    def get_typed_list_from_detailed_case_data(self, field: str, function: Callable = lambda x: x) -> list[Callable]:
        logger.debug(f'Getting {field} {self._detailed_case_data.get(field)}')
        return [function(item) for item in self._detailed_case_data.get(field)]

    # other getters

    def get_appear_by_date(self) -> date:
        return self.get_date_field_from_detailed_case_data('AppearByDate')

    def get_case_key(self) -> int:
        return self.get_int_field_from_detailed_case_data('CaseKey')

    def get_cross_refs(self) -> str:
        return self.get_str_field_from_detailed_case_data('CrossRefs')

    def get_related_case(self) -> str:
        return self.get_str_field_from_detailed_case_data('Related')

    def get_case_dict_for_persistence(self) -> dict:
        return {
            'pk_case_id'          : self.get_id(),
            'uniform_case_number' : self.get_case_number(),
            # TODO make reference table for court ids
            # 'fk_court_id': 'smallint',
            'file_date'           : self.get_file_date(),
            'case_status'         : self.get_case_status(),
            'case_status_date'    : self.get_case_status_date(),
            # TODO make reference table for case_type
            # 'fk_case_type_id': 'smallint',
            'style'               : self.get_style(),
            'is_active'           : self.get_is_active(),
            'appear_by_date'      : self.get_appear_by_date(),
            'cross_refs'          : self.get_cross_refs(),
            'related_case'        : self.get_related_case(),
        }

    def get_events_array_for_persistence(self) -> list[CaseEvent]:
        events: [CaseEvent] = self.get_typed_list_from_detailed_case_data('Events', CaseEvent)
        return [event.get_dict_for_persistence() for event in events]

    def get_parties_array_for_persistence(self) -> list:
        return [{
            'pk_case_party_id'    : 'integer',
            'party_id'            : 'integer',
            'fk_case_id'          : 'integer',
            'base_connection_key' : 'character varying',
            'name'                : 'character varying',
            'extended_name'       : 'character varying',
            'dob'                 : 'date',
            'address'             : 'json',
            'removed_date'        : 'date',
            'removed_reason'      : 'character varying',
            'attorney'            : 'json',
        } for party in self.get_typed_list_from_detailed_case_data('Parties', CaseParty)]


class SearchResults:
    _results = {}

    def add(self, item: SearchItem):
        if item.get_case_number() not in self._results.keys():
            logger.debug(f'Adding item with case number {item.get_case_number()}')
            self._results.update({item.get_case_number(): item})
        else:
            logger.warning(f'Item with case number {item.get_case_number()} already exists in set')

    def add_list(self, items: [SearchItem]):
        logger.debug(f'Adding {len(items)} items to list of results')
        for i in items:
            self.add(i)

    def get_total(self):
        logger.debug(f'Getting total results, current: {len(self._results)}')
        return len(self._results.keys())

    def keys(self):
        logger.debug(f'Getting result keys {self._results.keys()}')
        return self._results.keys()

    def values(self) -> [SearchItem]:
        logger.debug(f'Getting result values {self._results.values()}')
        return self._results.values()

    def find_by_case_number(self, case_num: str):
        if case_num in self._results.keys():
            logger.debug(f'Found SearchItem for case number {case_num}')
            return self._results.get(case_num)
        else:
            logger.debug(f'Could not find SearchItem for case number {case_num}')
