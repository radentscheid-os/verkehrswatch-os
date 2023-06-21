import os
import traceback
import random
import argparse
from urllib.parse import urljoin
from datetime import datetime, timedelta
from twitter import *
import pytz
from verkehrswatch_os.base import config
from verkehrswatch_os.base import mail

from verkehrswatch_os.parking.parking_ramps import get_ramps_utilization_from_db


def sendTweet(msg):
    api = Twitter(auth=OAuth(
        config.atoken,
        config.atsecret,
        config.ckey,
        config.csecret

    ))
    api.statuses.update(status=msg)


def getRandomNumber(min, max):
    value = max - min
    result = round(min + value * random.random(), 0)
    return int(result)


def getComparisson(freeSpots):
    # [m², 'Bezeichnung', Anzahl]
    spotSize = 12.5  # Größe eines Autostellplatze 2,5 * 5
    totalArea = round(freeSpots * spotSize)
    comparissons = [
        [7140, 'Fußball-Spielfelder', 1],
        [2910, 'mal die Fläche des Rathaus-Marktes', 1],
        [3537, 'mal die Fläche des Domplatzes', 1],
        [1983, 'mal die Fläche des Nikolaiortes', 1],
        [20000, 'mal die Fläche des Schlossgartens', 1],
        [243274, 'mal die Fläche des Rubbenbruchsees', 1],
        [46, 'Gelenkbusse', 0],
        [2, 'Fahrradabstellplätze', 0]
    ]

    comparrisonCount = getRandomNumber(0, len(comparissons) - 1)
    singleComp = comparissons[comparrisonCount]
    if singleComp[2] == 0:
        factor = round(totalArea / int(singleComp[0]))
    else:
        factor = round(totalArea / int(singleComp[0]), singleComp[2])
    text = singleComp[1]
    return [round(totalArea), factor, text]

def weekly_overview():
    today = datetime.today()
    time_to = (today - timedelta(days=today.weekday())).replace(hour=0,minute=0,second=0,microsecond=0) # Monday 0:00
    time_from = time_to - timedelta(days=7)
    data = get_ramps_utilization_from_db(city_center=True, latest=False, time_from=time_from, time_to=time_to)
    # TODO: plot data
    # TODO: tweet image
    # TODO: save image in git
    # TODO: may create website with parking space diagrams


def main():
    try:
        parser = argparse.ArgumentParser(description='Twitter-Bot für Parkhausverfügbarkeit in Osnabrück')
        parser.add_argument('-o','--overview', help='Tweet weekly overview of ramp availability ', action='store_true')
        
        args = parser.parse_args()
        if args.overview:
            weekly_overview()

        else:
            numbers = get_ramps_utilization_from_db(True)
            comp = getComparisson(numbers["available"])

            message = f"In #Osnabrück werden aktuell {numbers['available']} von {numbers['total']} Autoparkplätzen " \
                    f"in der Innenstadt nicht genutzt. Das ist eine Flächenverschwendung von " \
                    f"{comp[0]} m² (ca. {comp[1]} {comp[2]})."
            
            time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            # check if data is current
            time_now = datetime.now(pytz.UTC)
            time_data = datetime.strptime(numbers["created_at_utc"],"%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.UTC)
            delta = time_now - time_data
            if delta.seconds > 10 * 60: # data shouldn't be older than 10 minutes
                raise Exception("Data outdated. Skip tweet.")

            print(f"{time}: {message}")
            sendTweet(message)
    except Exception as e:
        mail.send_email(config.EMAIL_ERROR_MESSAGE.format(
            script=os.path.basename(__file__),
            error=e,
            traceback=traceback.format_exc()
            )
        )

if __name__ == "__main__":
    main()
