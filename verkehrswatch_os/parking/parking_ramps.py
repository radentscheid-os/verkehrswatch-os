import re
import sys
import json
from datetime import datetime
from base.request import send_request
from parking.database import query
from base.utils import utc2cet, cet2utc

def get_ramps_overview(url, onlyOsna = True):
  response = send_request(url)
  if response.status_code != 200:
        sys.stderr.write("Request failed with status code: {:d}!".format(
            response.status_code))
        exit(2)
  match = re.findall("var parkingRampData = (.*);", response.content.decode("utf-8"))
  if len(match) > 0:
    ramps = json.loads(match[0])  
  if onlyOsna:
    filtered_ramp_data = dict()
    for key, value in ramps.items():
        if value["city"].encode('utf-8') == "Osnabrück":
            filtered_ramp_data[key] = value
    return filtered_ramp_data
  else:
    return ramps

def get_ramps_utilization(url):
    response = send_request(url)
    if response.status_code != 200:
        sys.stderr.write("Request failed with status code: {:d}!".format(
            response.status_code))
        exit(2)
    return json.loads(response.content)

def ramp_is_closed(ramp_id, dt_str: str):
  dt = datetime.strptime(dt_str,"%Y-%m-%d %H:%M:%S")
  day_of_the_week = dt.isoweekday()
  time = datetime.strftime(dt, "%H:%M")
  result = query(
    """
      SELECT 
      CASE 
        WHEN 
          ? >= open_time AND ? <= close_time 
        THEN 
          False 
        ELSE True 
      END
      from business_hours bh 
      WHERE ramp_id = ?
      and day = ?
    """,
    (time, time, ramp_id, day_of_the_week)
  )
  return result[0] if len(result) > 0 else False


def get_ramps_utilization_from_db(city_center: bool, latest: bool = True, time_from: datetime = None, time_to: datetime = datetime.now() ):
  if latest:
    statement = """
      SELECT 
        SUM(capacity) as total, 
        SUM(available) as available, 
        created_at_utc
      FROM ramps_details rd LEFT JOIN ramp_utilization ru ON rd.id = ru.ramp_id  
      WHERE rd.city_center = 1
      GROUP BY created_at_utc
      ORDER BY created_at_utc desc
      LIMIT 1;
    """
    result = query(statement)
    return result[0]
  
  else:
    # get all ramps
    rows_ramp_data = query(
      """
        SELECT ramp_id, capacity, available, created_at_utc
        FROM ramps_details rd LEFT JOIN ramp_utilization ru ON rd.id = ru.ramp_id  
        WHERE
          rd.city_center = ? AND
          created_at_utc > ? AND
          created_at_utc < ?
      """,
      (city_center, cet2utc(time_from), cet2utc(time_to))
    )

    # Loop through ramps
    availablity_dict = dict()
    for row in rows_ramp_data:
      time_cet = utc2cet(row["created_at_utc"])
      # check if ramp is open
      
      is_closed = ramp_is_closed(row["ramp_id"], time_cet)
      capacity = row["capacity"]
      # if ramp is closed, assume it is empty and all parking spots are available (data shows none available, which is actually wrong, since there is a lot of unused space)
      available = row["available"] if not is_closed else capacity
      # add values to dict
      if time_cet in availablity_dict.keys():
          availablity_dict[time_cet]["capacity"] = availablity_dict[time_cet]["capacity"] + capacity
          availablity_dict[time_cet]["available"] = availablity_dict[time_cet]["available"] + available
      else:
        availablity_dict[time_cet] = {
          "capacity": row["capacity"],
          "available": row["available"]
        }
    return availablity_dict
