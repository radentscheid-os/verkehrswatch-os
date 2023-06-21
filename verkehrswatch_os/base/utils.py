from datetime import datetime
from pytz import timezone

def utc2cet(dt: str | datetime):
    if not isinstance(dt, datetime):
        dt = datetime.strptime(dt,"%Y-%m-%d %H:%M:%S")
    dt = timezone("UTC").localize(dt)
    dt = dt.astimezone(timezone("Europe/Berlin"))
    return datetime.strftime(dt, "%Y-%m-%d %H:%M:%S")

def cet2utc(dt: str | datetime) :
    if not isinstance(dt, datetime):
        dt = datetime.strptime(dt,"%Y-%m-%d %H:%M:%S")
    dt = timezone("Europe/Berlin").localize(dt)
    dt = dt.astimezone(timezone("UTC"))
    return datetime.strftime(dt, "%Y-%m-%d %H:%M:%S")