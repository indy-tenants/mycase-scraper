from unittest import TestCase

from mycase_scraper.db.sheets import Sheets
from mycase_scraper.settings import Settings
from utils.case import CaseDetails


class TestSheets(TestCase):

    def test_init(self):
        sheets = Sheets(Settings)
        self.assertIn(Settings.ARCHIVE_SHEET_NAME, sheets.spreadsheet.get_sheets())
        self.assertIn(Settings.PRIMARY_SHEET_NAME, sheets.spreadsheet.get_sheets())

    def test_add_raw_data_for_case(self):
        case_items = {
            'CaseID': 40229763,
            'CaseToken': 'hd-ZjujwqRaKh5es61TNYvrNsxrcCF8YpYrhZMVnWto1',
            'CaseNumber': '49K01-2101-EV-000399',
            'Court': 'Center Township',
            'FileDate': '01/31/2021',
            'CaseStatus': 'Decided',
            'CaseStatusDate': '02/10/2021',
            'CaseType': 'EV - Evictions (Small Claims Docket)',
            'CaseSubType': None,
            'Style': 'Rickey Pascarella Investment Group v. Cornelius Logwood',
            'IsActive': False,
            'IsPublic': True,
            'Parties': 'Rickey Pascarella Investment Group, Logwood',
            'Attorneys': None,
            'ShowWarrantIcon': False,
            'CommCourtFlag': None,
            'CiteNumbers': None,
            'Charges': None
        }

        case_details = {
            'InvalidToken': False,
            'CaseKey': '40229374',
            'CaseCategoryKey': 'CV',
            'CaseCategoryGroup': 'Civil',
            'CaseNumber': '49K01-2101-EV-000394',
            'Court': 'Center Township',
            'CourtCode': 'K01',
            'CountyCode': '49',
            'IsAppellateCourt': False,
            'FileDate': '01/30/2021',
            'CaseStatus': 'Decided',
            'CaseStatusDate': '03/24/2021',
            'CaseType': 'EV - Evictions (Small Claims Docket)',
            'CaseTypeCode': 'EVSC',
            'CaseSubType': None,
            'Style': 'HomeRiver Group as agent for the owner v. Alaine Jones, Any and all other occupants',
            'IsActive': None,
            'IsPublic': True,
            'AppearByDate': None,
            'Bonds': None,
            'Charges': None,
            'Events': [
                {
                    'EventKey': '609100778',
                    'CaseKey': '40229374',
                    'BaseEventType': 'C',
                    'BaseEventTypeKey': 'C',
                    'EventType': 'QCSNEW',
                    'EventDate': '01/30/2021',
                    'EventTime': None,
                    'Description': 'Case Opened as a New Filing',
                    'Judge': None,
                    'EventVolume': None,
                    'EventPage': None,
                    'NumberOfPages': None,
                    'IsDocketable': True,
                    'EventDocuments': None,
                    'CaseEvent': {
                        'EventKey': '609100778',
                        'Comment': None,
                        'Date2': None,
                        'Date2Label': 'Date 2',
                        'Parties': [{'PartyLabel': 'For Party', 'Name': 'HomeRiver Group as agent for the owner'}]
                    },
                    'DispEvent': None,
                    'HearingEvent': None,
                    'JEvent': None,
                    'SEvent': None,
                    'VEvent': None,
                    'AEvent': None
                },
                {
                    'EventKey': '621715064',
                    'CaseKey': '40229374',
                    'BaseEventType': 'H',
                    'BaseEventTypeKey': 'H',
                    'EventType': 'HDAM',
                    'EventDate': '05/24/2021',
                    'EventTime': '1:30 PM',
                    'Description': 'Damages Hearing',
                    'Judge': None,
                    'EventVolume': None,
                    'EventPage': None,
                    'NumberOfPages': None,
                    'IsDocketable': True,
                    'EventDocuments': None,
                    'CaseEvent': None,
                    'DispEvent': None,
                    'HearingEvent': {
                        'HearingEventKey': '621715064',
                        'CanceledReason': 'Dismissal / Judgment',
                        'Comment': None,
                        'Result': None,
                        'CourtName': 'Center Township',
                        'Sessions': [
                            {
                                'HearingEventKey': '621715064',
                                'HearingEventSessionKey': '28246558',
                                'SessionDate': '05/24/2021',
                                'SessionTime': '1:30 PM',
                                'DisplayText': '05/24/2021 1:30 PM, Cancelled',
                                'CancelStatus': 2,
                                'JudicialOfficers': [
                                    {
                                        'JudicialOfficerKey': '75580',
                                        'FormattedName': 'Roper, Brenda A.'
                                    }
                                ]
                            }
                        ]
                    },
                    'JEvent': None,
                    'SEvent': None,
                    'VEvent': None,
                    'AEvent': None
                }
            ],
            'Parties': [
                {
                    'CasePartyKey': '121182712',
                    'CaseKey': '40229374',
                    'PartyKey': '67110111',
                    'RestrictPublicView': False,
                    'Connection': 3,
                    'BaseConnKey': 'PL',
                    'ExtConnCode': 'PLN',
                    'ExtConnCodeDesc': 'Plaintiff',
                    'ActiveWarrants': 0,
                    'Description': None,
                    'Name': 'HomeRiver Group as agent for the owner',
                    'ExtendedName': None,
                    'DOB': None,
                    'DOD': None,
                    'Address': {
                        'ProviderName': None,
                        'Line1': 'C/o Landman Beatty, Lawyers, LLP',
                        'Line2': '9100 Keystone Crossing #870',
                        'Line3': None,
                        'Line4': None,
                        'City': 'Indianapolis',
                        'State': 'IN',
                        'Zip': '46240',
                        'Zip4': None
                    },
                    'FeePayURL': None,
                    'RemovedDate': None,
                    'RemovedReason': None,
                    'Attorneys': [
                        {
                            'AttyCasePartyID': 121182717,
                            'BarNumber': '#1852449',
                            'Lead': True,
                            'Label': '#1852449, Retained',
                            'WorkPhone': '317-236-1040',
                            'Name': 'Cynthia L Ball',
                            'Address': {
                                'ProviderName': None,
                                'Line1': '9100 Keystone Crossing Suite 870',
                                'Line2': 'P. O. Box 40960',
                                'Line3': None,
                                'Line4': None,
                                'City': 'Indianapolis',
                                'State': 'IN',
                                'Zip': '46240',
                                'Zip4': None
                            }
                        }
                    ],
                    'OANs': None,
                    'FeeSummary': {
                        'Balance': '0.00',
                        'AsOf': '12/27/2021',
                        'Categories': [
                            {
                                'Key': 'CC',
                                'Desc': 'Court Costs and Filing Fees',
                                'Charge': '115.00',
                                'Credit': '0.00',
                                'Payment': '115.00'
                            }
                        ]
                    },
                    'Transactions': [
                        {
                            'Date': '02/01/2021',
                            'Desc': 'Transaction Assessment',
                            'Amount': '102.00'
                        },
                    ]
                },
                {
                    'CasePartyKey': '121182713',
                    'CaseKey': '40229374',
                    'PartyKey': '67110112',
                    'RestrictPublicView': False,
                    'Connection': 2,
                    'BaseConnKey': 'DF',
                    'ExtConnCode': 'DEF',
                    'ExtConnCodeDesc': 'Defendant',
                    'ActiveWarrants': 0,
                    'Description': None,
                    'Name': 'Jones, Alaine',
                    'ExtendedName': None,
                    'DOB': None,
                    'DOD': None,
                    'Address': {
                        'ProviderName': None,
                        'Line1': '1111 North Parker Avenue',
                        'Line2': None,
                        'Line3': None,
                        'Line4': None,
                        'City': 'Indianapolis',
                        'State': 'IN',
                        'Zip': '46201',
                        'Zip4': None
                    },
                    'FeePayURL': None,
                    'RemovedDate': None,
                    'RemovedReason': None,
                    'Attorneys': None,
                    'OANs': None,
                    'FeeSummary': None,
                    'Transactions': None
                },
                {
                    'CasePartyKey': '121182714',
                    'CaseKey': '40229374',
                    'PartyKey': '67110113',
                    'RestrictPublicView': False,
                    'Connection': 2,
                    'BaseConnKey': 'DF',
                    'ExtConnCode': 'DEF',
                    'ExtConnCodeDesc': 'Defendant',
                    'ActiveWarrants': 0,
                    'Description': None,
                    'Name': 'other occupants, Any and all',
                    'ExtendedName': None,
                    'DOB': None,
                    'DOD': None,
                    'Address': None,
                    'FeePayURL': None,
                    'RemovedDate': None,
                    'RemovedReason': None,
                    'Attorneys': None,
                    'OANs': None,
                    'FeeSummary': None,
                    'Transactions': None
                }
            ],
            'CrossRefs': None,
            'Related': None,
            'CommCourtFlag': None
        }

        sheets = Sheets(Settings)
        sheets.add_raw_data_for_case(CaseDetails(case_items, case_details))
        self.assertTrue(None)

    def test_get_decided_sheet(self):
        self.fail()
