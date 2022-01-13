from datetime import datetime
from json import dump, load


class ConfigFile:

    def __init__(self, filename):
        self.filename = filename

    def write(self, json_dict: dict):
        with open(self.filename, 'w') as outfile:
            dump(json_dict, outfile, indent=4)

    def read(self) -> dict:
        with open(self.filename) as json_file:
            return load(json_file)


def get_current_month_as_str():
    return str(datetime.now().month).zfill(2)


def get_current_year_as_str():
    return str(datetime.now().year)[2:]


def format_year_month(year: str, month: str):
    return f'{year[:2]}{month.zfill(2)}'
