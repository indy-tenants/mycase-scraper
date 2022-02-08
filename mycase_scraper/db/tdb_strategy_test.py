from unittest import TestCase, main

from db.persistence_builder import PersistenceBuilder, PersistenceStrategy
from utils.case import CaseDetails, SearchItem


class TinyDBStrategyTest(TestCase):

    def test_save_case(self):
        out = PersistenceBuilder.get_context(
            PersistenceStrategy.TINYDB
        ).save_case({'test0': 'test'})
        self.assertIsNotNone(out)

    def test_save_cases(self):
        out = PersistenceBuilder.get_context(
            PersistenceStrategy.TINYDB
        ).save_cases([
            CaseDetails(SearchItem( ))
        ])
        self.assertIsNotNone(out)


if __name__ == '__main__':
    main()
