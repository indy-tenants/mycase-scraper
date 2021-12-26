from unittest import TestCase

from uri import URI


class TestURI(TestCase):
    def test_decode_slug(self):
        self.fail()

    def test_encode_slug(self):
        self.fail()

    # noinspection SpellCheckingInspection
    def test_get_case_url(self):
        self.assertEqual(
            'https://public.courts.in.gov/mycase/#/vw/CaseSummary/eyJ2IjogeyJDYXNlVG9rZW4iOiAiOURkU0RPNFZHZ0VWbVRJQUM0dG1FV2VYVXU1RkRrTmpYTTg3VmpDVlN2STEifX0=', # noqa
            URI.get_case_url('9DdSDO4VGgEVmTIAC4tmEWeXUu5FDkNjXM87VjCVSvI1')
        )

    def test_get_search_url_with_court_and_date(self):
        self.assertEqual(
            'https://public.courts.in.gov/mycase/#/vw/SearchResults/eyJ2IjogeyJNb2RlIjogIkJ5Q2FzZSIsICJDYXNlTnVtIjogIjQ5SzAxLTIxMDEtRVYtKiIsICJDaXRlTnVtIjogbnVsbCwgIkNyb3NzUmVmTnVtIjogbnVsbCwgIkZpcnN0IjogbnVsbCwgIk1pZGRsZSI6IG51bGwsICJMYXN0IjogbnVsbCwgIkJ1c2luZXNzIjogbnVsbCwgIkRvQlN0YXJ0IjogbnVsbCwgIkRvQkVuZCI6IG51bGwsICJPQU51bSI6IG51bGwsICJCYXJOdW0iOiBudWxsLCAiU291bmRFeCI6IGZhbHNlLCAiQ291cnRJdGVtSUQiOiBudWxsLCAiQ2F0ZWdvcmllcyI6IG51bGwsICJMaW1pdHMiOiBudWxsLCAiQWR2YW5jZWQiOiBmYWxzZSwgIkFjdGl2ZUZsYWciOiAiQWxsIiwgIkZpbGVTdGFydCI6IG51bGwsICJGaWxlRW5kIjogbnVsbCwgIkNvdW50eUNvZGUiOiBudWxsfX0=', # noqa
            URI.get_search_url_with_court_and_date('49K01', '2101')
        )
