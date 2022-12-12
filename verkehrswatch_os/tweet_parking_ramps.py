import os
import traceback
import random
from urllib.parse import urljoin
from datetime import datetime
from twitter import *

from verkehrswatch_os.base import config
from verkehrswatch_os.base import mail

from verkehrswatch_os.parking.parking_ramps import get_ramps_utilization


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


def getFreeAndTotalNumber():

    ramp_utilization = get_ramps_utilization(urljoin(config.BASE_URL, config.UTILIZATION_URL))
    
    total = 0
    free = 0

    for key in ramp_utilization.keys():
        parkhaus = ramp_utilization[key]
        total += parkhaus["capacity"]
        free += parkhaus["available"]

    return [free, total]


def main():
    try:
        numbers = getFreeAndTotalNumber()
        comp = getComparisson(numbers[0])

        message = f"In #Osnabrück werden aktuell {numbers[0]} von {numbers[1]} Autoparkplätzen " \
                  f"in der Innenstadt nicht genutzt. Das ist eine Flächenverschwendung von " \
                  f"{comp[0]} m² (ca. {comp[1]} {comp[2]})."
           
        time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
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
