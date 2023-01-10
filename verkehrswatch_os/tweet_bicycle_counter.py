import os
import traceback
import sys
import json
import argparse
import locale
import datetime
from pathlib import Path
from dateutil.relativedelta import relativedelta
from twitter import *
from base.request import send_request
from base.diagram import generate_diagram
from base import mail
from base import config

"""
Source: 
Katharinenstr: https://data.eco-counter.com/public2/?id=300018001
RSW Belm - OS: http://rswosnabelm.eco-counter.com/
"""

URL = "https://www.eco-visio.net/api/aladdin/1.0.0/pbl/publicwebpage/data/{counter_id}?domain=6821&t={token}&withNull=true&begin={begin}&end={end}&step={step}"
BELM_OS = {
    "token": "7b662872c592641dd8053ed7ecbccf8589659196b3e9f37cd9f5dede03c1880c",
    "ids": ["100050631"]
    }
KATHA = {
    "token": "a1905d602230a2e12fcaf9d3a8dc8b1fc88196072b65254105973a239d968be7",
    "ids": ["353271103"]
    }

def sendTweet(msg, image_filenames):
    api = Twitter(auth=OAuth(
        config.atoken,
        config.atsecret,
        config.ckey,
        config.csecret

    ))
    image_ids = []
    t_upload = Twitter(domain='upload.twitter.com',
    auth=OAuth(
        config.atoken,
        config.atsecret,
        config.ckey,
        config.csecret)
        )
    for image_filename in image_filenames:
        with open(image_filename, "rb") as imagefile:
            imagedata = imagefile.read()
            id_img = t_upload.media.upload(media=imagedata)["media_id_string"]
            image_ids.append(id_img)
    
    api.statuses.update(status=msg, media_ids=",".join(image_ids))

def request_json(url):
    response = send_request(url)
    if response.status_code != 200:
            sys.stderr.write("Request failed with status code: {:d}!".format(
                response.status_code))
            exit(2)
    return json.loads(response.content)

def get_count(counter_ids, token, begin, end, step):
    total_count = 0
    for counter_id in counter_ids:
        json = request_json(URL.format(counter_id=counter_id, token=token, begin=begin, end=end, step=step))
        if len(json) > 0:  
            total_count = total_count + json[0]["comptage"]
    return total_count if total_count > 0 else None


def monthly_stats():
    STEP = 6

    today = datetime.date.today()
    first = today.replace(day=1)
    
    last_month = first - datetime.timedelta(days=1)
    locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
    last_month_string = last_month.strftime("%B")

    end = first.strftime("%Y%m%d")  #last_month.strftime("%Y%m%d")
    begin = last_month.replace(day=1).strftime("%Y%m%d")
    
    end_last_year = (first - relativedelta(years=1)).strftime("%Y%m%d")
    begin_last_year = (last_month - relativedelta(years=1)).replace(day=1).strftime("%Y%m%d")

    end_two_years_ago = (first - relativedelta(years=2)).strftime("%Y%m%d")
    begin_two_years_ago = (last_month - relativedelta(years=2)).replace(day=1).strftime("%Y%m%d")

    belm_os_count = get_count(BELM_OS["ids"], BELM_OS["token"], begin, end, STEP)
    belm_os_count_last_year = get_count(BELM_OS["ids"], BELM_OS["token"], begin_last_year, end_last_year, STEP)
    belm_os_count_two_years_ago = get_count(BELM_OS["ids"], BELM_OS["token"], begin_two_years_ago, end_two_years_ago, STEP)

    katha_count = get_count(KATHA["ids"], KATHA["token"], begin, end, STEP)
    katha_count_last_year = get_count(KATHA["ids"], KATHA["token"], begin_last_year, end_last_year, STEP)
    katha_count_two_years_ago = get_count(KATHA["ids"], KATHA["token"], begin_two_years_ago, end_two_years_ago, STEP)
    
    year = last_month.strftime("%Y")
    last_year = (last_month - relativedelta(years=1)).strftime("%Y")
    two_years_ago = (last_month - relativedelta(years=2)).strftime("%Y")
    belm_path = Path(__file__).parent.resolve() / Path("img/belm.png")
    generate_diagram(
        [two_years_ago, last_year, year],
        [belm_os_count_two_years_ago or 0, belm_os_count_last_year or 0, belm_os_count or 0],
        f"Radschnellweg Belm \n\n Radfahrende im {last_month_string}",
        "royalblue",
        belm_path)

    kata_path = Path(__file__).parent.resolve() / Path("img/katharinenstr.png")
    generate_diagram(
        [two_years_ago, last_year, year],
        [katha_count_two_years_ago or 0, katha_count_last_year or 0, katha_count or 0],
        f"Katharinenstraße \n\n Radfahrende im {last_month_string}",
        "forestgreen",
        kata_path)
    message = "Im {last_month_string} {year} zählten die #Osnabrück|er Fahrradzählstellen folgende Anzahl an Fahrradfahrenden. Vorjahreszahlen in Klammern\
    \n\nRadschnellweg Belm-OS: {belm_os_count} ({last_year}: {belm_os_count_last_year}, {two_years_ago}: {belm_os_count_two_years_ago})\
    \nKatharinenstraße: {katha_count} ({last_year}: {katha_count_last_year}, {two_years_ago}: {katha_count_two_years_ago})"
    
    message = message.format(
        last_month_string=last_month_string,
        last_year=last_year,
        year=year,
        two_years_ago=two_years_ago,
        belm_os_count=belm_os_count or "-", 
        belm_os_count_last_year=belm_os_count_last_year or "-",
        belm_os_count_two_years_ago=belm_os_count_two_years_ago or "-",
        katha_count=katha_count or "-", 
        katha_count_last_year=katha_count_last_year or "-",
        katha_count_two_years_ago=katha_count_two_years_ago or "-")


    time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    print("{}: {}".format(time, message))

    sendTweet(message, [belm_path, kata_path])


def main():
    try:
        parser = argparse.ArgumentParser(description='Twitter-Bot für Fahrradzählstellen in Osnabrück')
        parser.add_argument('-m','--monthly', help='Tweet monthly bicylces', action='store_true')
        
        args = parser.parse_args()
        if args.monthly:
            monthly_stats()
        else:
            parser.error('No arguments provided.')
    except Exception as e:
        print (e)
        mail.send_email(config.EMAIL_ERROR_MESSAGE.format(
            script=os.path.basename(__file__),
            error=e,
            traceback=traceback.format_exc()
            )
        )

if __name__ == "__main__":
    main()
