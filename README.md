Twitter-Bot Parkhäuser Osnabrück und Bicycle Counter :bicyclist:
=====================================================

Willkommen bei [Verkehrswatch-OS](https://twitter.com/VerkehrswatchOS), einem Projekt vom [Radentscheid Osnabrück](https://radentscheid-os.de). Die Inspiration für dieses Projekt kam vom Münsteraner Pendant [VerkehrswatchMS](https://twitter.com/verkehrswatchms)

Das Ziel dieses Tools ist es öffentlich zugängliche und verkehrsrelavante Daten zu sammeln und auf Twitter zu zeigen.

Folgende Quellen werden angezapft:

## Parkhäuser Osnabrück

Parken im öffentlich Raum verbraucht viel Platz, der gerade in der Innenstadt auch anderen Verkehrsarten, wie dem Fuß- oder Radverkehr, zugesprochen werden könnte. Daher möchten wir aufzeigen, dass es in Osnabrück bereits viele Parkmöglichkeiten in Parkhäusern gibt und diese auch sehr oft nicht ausgelastet sind. Innerstädtische Parkplätze könnten somit ersatzlos gestrichen und der Raum anderen Verkehrsarten zur Verfügung gestellt werden.

2 mal täglich werden die aktuell frei verfügbaren Parkplätze getwittert.

Zusätzlich wird die Verfügbarkeit stündlich abgefragt und für weitere Auswertungen gespeichert. Die Daten ab März 2021 sind hier unter [Parkhaus-Daten](./Parkhaus-Daten/) hinterlegt.

Quelle: https://www.parken-osnabrueck.de/

## Fahrradzählstellen

In Osnabrück gibt es aktuell 2 Fahrradzählstellen, eine an der Katharinenstraße und eine am Anfang vom Radschnellweg von Osnabrück nach Belm. Aktuell wird einmal im Monat die Anzahl der Radfahrenden des vergangen Monats ausgelesen und zusammen mit den Zahlen der letzten 2 Jahre auf Twitter geteilt.

Quelle: 
- Katharinenstr: https://data.eco-counter.com/public2/?id=300018001
- Radschnellweg Belm - OS: http://rswosnabelm.eco-counter.com/

## Parkhaus-Daten

Ab März 2021 wird stündlich die Belegung der Osnabrücker Parkhäuser abgefragt und werden nun hier für weitere Auswertungen zur Verfügung gestellt. Es gibt die Daten in 2 Formaten, einmal csv-Datei für die Weiterarbeitung in Excel oder als sqlite-Datenbank. Im Datensatz befinden sich 2 Tabellen.

### Tabelle 1: Parkhaus-Infos`ramps_details`

| Spalte | Bedeutung |
|--------|---------- |
| id | Parkhaus-ID |
| name | Name |
| street | Straße |
| zipcode | Postleitzahl |
| city | Stadt |
| latitude | geografische Breite |
| longitude | geografische Länge |
| address | komplette Adresse |

### Tabelle 2: Auslastung `ramp_utilization`

| Spalte | Bedeutung |
|--------|---------- |
| id | fortlaufende ID |
| ramp_id | ID des Parkhauses (siehe `ramps_details`) |
| capacity | Kapazität |
| utilization | Aktuelle Auslastung |
| utilization_ratio | prozentuale Auslastung |
| available | Aktuell verfügbare Parkplätze |
| created_at_utc | Zeitstempel in UTC (+0) |

## Tool 

### Setup


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
python verkehrswatch_os/twee_bicycle_counter.py -m
```


### Ramp Availability

```
python verkehrswatch_os/tweet_parking_ramps.py 
```

```
python verkehrswatch_os/store_parking_ramp_data.py 
```

### Bicycle Couter


python verkehrswatch_os/twee_bicycle_counter.py [OPTIONS]

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
- auf Mastadon tröten
