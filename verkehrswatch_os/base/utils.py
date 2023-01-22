from datetime import datetime
from pytz import timezone

def utc_to_berlin(datetime_string: str):
    dt = datetime.strptime(datetime_string,"%Y-%m-%d %H:%M:%S")
    dt = timezone("UTC").localize(dt)
    dt = dt.astimezone(timezone("Europe/Berlin"))