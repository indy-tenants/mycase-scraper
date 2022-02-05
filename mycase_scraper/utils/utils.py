from datetime import datetime
from json import dump, load


def write_json_to_file(filename: str, json_dict: dict):
    with open(filename, 'w') as outfile:
        dump(json_dict, outfile, indent=4)


def read_json_from_file(filename: str) -> dict:
    with open(filename) as json_file:
        return load(json_file)


class ConfigFile:

    def __init__(self, filename):
        self.filename = filename

    def write(self, json_dict: dict):
        write_json_to_file(self.filename, json_dict)

    def read(self) -> dict:
        return read_json_from_file(self.filename)


def get_current_month_as_str():
    return str(datetime.now().month).zfill(2)


def get_current_year_as_str():
    return str(datetime.now().year)[2:]


def format_year_month(year: str, month: str):
    return f'{year[:2]}{month.zfill(2)}'
