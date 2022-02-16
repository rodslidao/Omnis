
from datetime import datetime as date
from platform import system as platform_system
from os import system as os_system
DATE_FORMAT = "%a %b %d %H:%M:%S UTC %Y"

def stamp_to_date(timestamp):
    return date.fromtimestamp(timestamp).strftime(DATE_FORMAT)


def set_system_date(_date, write_date=True):
    match _date:
        case str():
            pass
        case date():
            _date = _date.strftime(DATE_FORMAT)
        case float() | int():
            _date = stamp_to_date(_date)
        case _:
            raise TypeError("Invalid date type")
    if platform_system() == "Linux" and write_date:
            print(f"Setting system date to {_date}")
            os_system(f"sudo date -s '{_date}'")
    return _date

def get_system_date(_str=False, _format=DATE_FORMAT):
    return date.now().timestamp() if not _str else date.now().strftime(_format)