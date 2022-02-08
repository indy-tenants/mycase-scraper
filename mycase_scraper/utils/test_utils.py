from json import load
from unittest import TestCase

from utils.utils import ConfigFile


class TestConfigFile(TestCase):

    def test_write(self):
        config_filename = '../config-test.json'
        config = {
            'email': 'admin@example.com',
            'password': 'g00dp@ssw04d'
        }
        config_file = ConfigFile(config_filename)
        config_file.write(config)
        with open(config_filename) as file:
            json_config = load(file)
            self.assertTrue('email' in json_config)
            self.assertEqual(config.get('email'), json_config.get('email'))
            self.assertTrue('password' in json_config)
            self.assertEqual(config.get('password'), json_config.get('password'))

    def test_read(self):
        self.fail()
