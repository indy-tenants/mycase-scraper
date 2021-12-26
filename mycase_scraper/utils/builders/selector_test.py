from unittest import TestCase

from utils.builders.selector import CSSSelectorBuilder


class CSSSelectorBuilderTest(TestCase):

    def test_build_case_number_search_selector(self):
        self.assertEqual(
            ' input#SearchCaseNumber',
            CSSSelectorBuilder()
                .tag('input')
                .withId('SearchCaseNumber')
                .build()
        )

    def test_find_class_with_attribute(self):
        self.assertEqual(
            '',
            CSSSelectorBuilder()
                .tag('button')
                .withAttribute('title', 'Go to next result page')
                .build()
        )
