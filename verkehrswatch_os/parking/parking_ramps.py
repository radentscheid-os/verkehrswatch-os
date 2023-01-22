import re
import sys
import json
from datetime import datetime
from base.request import send_request
from parking.database import query

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
    # TODO: implement time_from and time_to
    pass