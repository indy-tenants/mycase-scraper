from unittest import TestCase

from utils.uniform_case_numbers import UniformCaseNumber


class TestUniformCaseNumber(TestCase):

    def test_from_string(self):
        case: UniformCaseNumber = UniformCaseNumber.from_string("49K01-2102-EV-000520")
        print(repr(case.case_number))
