from typing import Union

from mysql.connector import cursor  # noqa
from mysql.connector.connection import MySQLConnection

from db.abstract_strategy import AbstractPersistenceStrategy
from settings import Settings
from utils.case import CaseDetails, SearchItem


class PScaleStrategy(AbstractPersistenceStrategy):

    _insert_case_query = (
        'INSERT INTO `my_case_details` (' +
        '    `pk_case_id`,' +
        '    `uniform_case_number`,' +
        '    `file_date`,' +
        '    `case_status`,' +
        '    `case_status_date`,' +
        '    `style`,' +
        '    `is_active`,' +
        '    `appear_by_date`,' +
        '    `cross_refs`,' +
        '    `related_case`' +
        ') VALUES (' +
        '    %(pk_case_id)s,' +
        '    %(uniform_case_number)s,' +
        '    %(file_date)s,' +
        '    %(case_status)s,' +
        '    %(case_status_date)s,' +
        '    %(style)s,' +
        '    %(is_active)s,' +
        '    %(appear_by_date)s,' +
        '    %(cross_refs)s,' +
        '    %(related_case)s' +
        ')'
    )

    _update_case_query = (
            'UPDATE `my_case_details` SET' +
            '    `case_status`=%(case_status)s, ' +
            '    `case_status_date`=%(case_status_date)s, ' +
            '    `is_active`=%(is_active)s, ' +
            '    `appear_by_date`=%(appear_by_date)s, ' +
            '    `cross_refs`=%(cross_refs)s, ' +
            '    `related_case`=%(related_case)s ' +
            'WHERE `uniform_case_number`=%(uniform_case_number)s'
    )

    _insert_event_query = (
        'INSERT IGNORE INTO `my_case_event` (' +
        '    `pk_event_id`,' +
        '    `fk_case_id`,' +
        '    `event_type`,' +
        '    `event_date`,' +
        '    `event_time`,' +
        '    `description`,' +
        '    `judge`,' +
        '    `case_event`,' +
        '    `hearing_event`,' +
        '    `disp_event`,' +
        '    `j_event`,' +
        '    `s_event`,' +
        '    `v_event`,' +
        '    `a_event`' +
        ') VALUES (' +
        '    %(pk_event_id)s,' +
        '    %(fk_case_id)s,' +
        '    %(event_type)s,' +
        '    %(event_date)s,' +
        '    %(event_time)s,' +
        '    %(description)s,' +
        '    %(judge)s,' +
        '    %(case_event)s,' +
        '    %(hearing_event)s,' +
        '    %(disp_event)s,' +
        '    %(j_event)s,' +
        '    %(s_event)s,' +
        '    %(v_event)s,' +
        '    %(a_event)s' +
        ')'
    )

    _insert_party_query = (
        'INSERT IGNORE INTO `my_case_party` ('
        '    `pk_case_party_id`,' +
        '    `party_id`,' +
        '    `fk_case_id`,' +
        '    `base_connection_key`,' +
        '    `name`,' +
        '    `extended_name`,' +
        '    `dob`,' +
        '    `address`,' +
        '    `removed_date`,' +
        '    `removed_reason`,' +
        '    `attorney`' +
        ') VALUES (' +
        '    %(pk_case_party_id)s,' +
        '    %(party_id)s,' +
        '    %(fk_case_id)s,' +
        '    %(base_connection_key)s,' +
        '    %(name)s,' +
        '    %(extended_name)s,' +
        '    %(dob)s,' +
        '    %(address)s,' +
        '    %(removed_date)s,' +
        '    %(removed_reason)s,' +
        '    %(attorney)s' +
        ')'
    )

    def __init__(self):
        self.cnx: MySQLConnection = MySQLConnection(**{
            'host': Settings.PERSISTENCE_HOST.value,
            'user': Settings.PERSISTENCE_USER.value,
            'password': Settings.PERSISTENCE_PASSWORD.value,
            'port': Settings.PERSISTENCE_PORT.value,
        })

    def __del__(self):
        self.cnx.close()

    def execute_statement(self, sql: str, data: Union[dict, tuple] = None) -> list:
        _cursor: cursor = self.cnx.cursor(dictionary=True)
        _cursor.execute(sql, data)
        results = _cursor.fetchall()
        self.cnx.commit()
        _cursor.close()
        return results

    def get_case_by_ucn(self, uniform_case_number: str):
        data: list = self.execute_statement(
            'SELECT * FROM my_case_details WHERE (uniform_case_number=%s) LIMIT 1',
            (uniform_case_number,)
        )
        return None if len(data) == 0 else CaseDetails(SearchItem(data.pop()))

    def get_active_cases_before_this_month(self) -> list:
        active_cases = self.execute_statement('SELECT * FROM my_case_details WHERE is_active=TRUE AND file_date < CONCAT(LEFT(NOW(), 7),\'-01\')')
        return list(map(lambda c: CaseDetails(SearchItem(c)), active_cases))

    def update_case(self, case: CaseDetails):
        return self.execute_statement(self._update_case_query, case.get_case_dict_for_persistence())

    def save_case(self, case: CaseDetails):
        self.execute_statement(self._insert_case_query, case.get_case_dict_for_persistence())
        for event in case.get_events_array_for_persistence():
            self.execute_statement(self._insert_event_query, event)
        for party in case.get_parties_array_for_persistence():
            self.execute_statement(self._insert_party_query, party)

    def save_cases(self, cases: [CaseDetails]):
        map(self.save_case, cases)
