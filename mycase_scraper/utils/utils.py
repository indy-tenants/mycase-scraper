from datetime import datetime


def get_current_month_as_str():
    return str(datetime.now().month).zfill(2)


def get_current_year_as_str():
    return str(datetime.now().year)[2:]


def format_year_month(year: str, month: str):
    return f'{year[:2]}{month.zfill(2)}'
