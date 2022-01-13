from unittest import TestCase

from settings import Settings


class TestSettings(TestCase):

    def test_values(self):
        print(Settings.APP_CONFIG_FILENAME.value)
        print(Settings.APP_HOME_DIRECTORY.value)
