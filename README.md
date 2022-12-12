Twitter-Bot Parkhäuser Osnabrück und Bicycle Couter
===================================================

Willkommen im bei Verkehrswatch-OS, einem Projekt vom [Radentscheid Osnabrück](https://radentscheid-os.de). 

Das Ziel dieses Tools ist es öffentlich zugängliche und verkehrsrelavante Daten zu sammeln und auf Twitter zu zeigen.

Folgende Quellen werden angezapft:

**Parkhäuser Osnabrück**

Parken im öffentlich Raum verbraucht viel Platz, der gerade in der Innenstadt auch anderen Verkehrsarten, wie dem Fuß- oder Radverkehr, zugesprochen werden könnte. Daher möchten wir aufzeigen, dass es in Osnabrück bereits viele Parkmöglichkeiten in Parkhäusern gibt und diese auch sehr oft nicht ausgelastet sind. Innerstädtische Parkplätze könnten somit ersatzlos gestrichen und der Raum anderen Verkehrsarten zur Verfügung gestellt werden.

2 mal täglich werden die aktuell frei verfügbaren Parkplätze getwittert.

Zusätzlich wird die Verfügbarkeit stündlich abgefragt und für weitere Auswertungen gespeichert. Die Daten ab März 2021 sind hier unter [Parkhaus-Daten](./Parkhaus-Daten/) hinterlegt.

Quelle: https://www.parken-osnabrueck.de/

**Fahrradzählstellen**
In Osnabrück gibt es aktuell 2 Fahrradzählstellen, einen an der Katharinenstraße und einen am Anfang vom Radschnell von Osnabrück nach Belm. Aktuell wird einmal im Monat die Anzahl der Radfahrenden des vergangen Monats ausgelesen und zusammen mit den Zahlen der letzten 2 Jahre auf Twitter geteilt.

## Getting started (Linux)


- create python virtual environment
```
virtualenv -p python3 --system-site-packages venv
```

- activate venv
```
. venv/bin/activate
```

- install libraries
```
venv/bin/pip3 install -r requirements.txt 
```

- install verkehrswatch_os
```
pip install -e .
```

- create config.py and enter own credentials and configuration
```
cp verkehrswatch_os/base/config.template verkehrswatch_os/base/config.py
```

- run script
```
python verkehrswatch_os/tweet_parking_ramps.py 
python verkehrswatch_os/store_parking_ramp_data.py 
python verkehrswatch_os/twee_bicycle_counter.py
```


### Ramp Availability

```
python ~/twitter-bot/tweet_parking_space.py 2>&1 ~/twitter-bot/tweet_parking_space.
```

```
python ~/twitter-bot/store_parking_space_data.py 2>&1 ~/twitter-bot/store_parking_space
```

### Bicycle Couter


python ~/twitter-bot/tweet_bicycle_counter.py [OPTIONS]

```
usage: tweet_bicycle_counter.py [-h] [-m]

Twitter-Bot für Fahrradzählstellen in Osnabrück

optional arguments:
  -h, --help     show this help message and exit
  -m, --monthly  Tweet monthly bicylce count
```

## TODO:
- Parkhaus Daten regelmäßig veröffentlichen
- Parkhausbelegung in Diagramm darstellen und wöchentlich twittern
- Anzahl der Radfahrenden im aktuellen Jahr (2 wöchentlich)
