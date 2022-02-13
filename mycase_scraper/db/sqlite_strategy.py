from datetime import datetime

from loguru import logger
from peewee import BlobField, BooleanField, CharField, DateField, ForeignKeyField, IntegerField, Model, SqliteDatabase, \
    TimeField, TimestampField

from abstract_strategy import AbstractPersistenceStrategy
from settings import Settings
from utils.case import CaseDetails


class Sqlite3Strategy(AbstractPersistenceStrategy):

    db = None
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logger.debug('Creating connection to supabase')
            cls._instance = super(Sqlite3Strategy, cls).__new__(cls)
            try:
                cls.db = SqliteDatabase(Settings.SQLITE3_FILE_NAME.value, pragmas={'journal_mode': 'wal'})
            except Exception as ex:
                logger.exception(f'Could not authenticate {ex}')
        return cls._instance

    @classmethod
    def save_case(cls, case: CaseDetails):
        try:
            Case.bulk_create(case.get_case_dict_for_persistence())
        except Exception as ex:
            logger.exception(f'Failed to save case record \'{case.get_data()}\'')


class Case(Model):

    pk_case_id = IntegerField(unique=True)
    retrieved_at = TimestampField(default=datetime.now)
    uniform_case_number = CharField()
    fk_court_id = IntegerField()
    file_date = DateField()
    case_status = CharField()
    case_status_date = DateField()
    fk_case_type_id = IntegerField()
    style = CharField()
    is_active = BooleanField()
    appear_by_date = DateField()
    cross_refs = CharField()
    related_case = CharField()

    class Meta:
        database = Sqlite3Strategy().db
        db_table = 'case'


class Event(Model):

    pk_event_id = IntegerField(unique=True)
    fk_case_id = ForeignKeyField(Case, field=Case.pk_case_id, backref='events')
    event_type = CharField()
    event_date = DateField()
    event_time = TimeField()
    description = CharField()
    judge = CharField()
    case_event = BlobField()
    hearing_event = BlobField()
    disp_event = BlobField()
    j_event = BlobField()
    s_event = BlobField()
    a_event = BlobField()

    class Meta:
        database = Sqlite3Strategy().db
        db_table = 'event'


class Party(Model):

    pk_case_party_id = IntegerField()
    party_id = IntegerField()
    fk_case_id = ForeignKeyField(Case, backref='parties')
    base_connection_key = CharField()
    name = CharField()
    extended_name = CharField()
    dob = DateField()
    address = BlobField()
    removed_date = DateField()
    removed_reason = CharField()
    attorney = BlobField()

    class Meta:
        database = Sqlite3Strategy().db
        db_table = 'party'


Sqlite3Strategy.db.connect()
Sqlite3Strategy.db.create_tables([Case, Event, Party])
