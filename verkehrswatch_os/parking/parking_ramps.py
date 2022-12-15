import re
import sys
import json
from base.request import send_request

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