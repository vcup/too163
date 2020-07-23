from datetime import datetime
from json import loads
from time import strftime, localtime


def timestamp(stamp: float, time_zone_info=None) -> datetime:
    time_tuple = loads(strftime('["%Y", "%m", "%d", "%H", "%M", "%S"]', localtime(stamp)))
    return datetime(*(int(n) for n in time_tuple), tzinfo=time_zone_info)
