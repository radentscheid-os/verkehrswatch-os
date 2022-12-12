import sqlite3
import traceback
import os
from verkehrswatch_os.base import config
from verkehrswatch_os.base import mail

INSERT_STATEMENT_RAMPS = """
INSERT OR IGNORE INTO ramps_details
(id, name, street, zipcode, city, latitude, longitude, address)
VALUES(?, ?, ?, ?, ?, ?, ?, ?);
"""

INSERT_STATEMENT_UTILIZATION = """
INSERT INTO ramp_utilization (ramp_id,
 capacity, utilization, utilization_ratio, available)
  VALUES(?,?,?,?,?)
 """

def connect():
    conn = None
    try:
        conn = sqlite3.connect(config.DB_FILE)
    except Exception as e:
        mail.send_email(config.EMAIL_ERROR_MESSAGE.format(
            script=os.path.basename(__file__),
            error=e,
            traceback=traceback.format_exc()
            )
        )

    return conn

def execute(statement, data):

    with sqlite3.connect(config.DB_FILE) as connection:
        cursor = connection.cursor()
        cursor.executemany(statement, data)
        connection.commit()


def write_ramps_details_to_db(ramps_datails):
    """
    Uses following table:
    CREATE TABLE "ramps_details" (
        "id" INTEGER NOT NULL  ,
        "name" TEXT NOT NULL  ,
        "street" TEXT NOT NULL  ,
        "zipcode" TEXT NOT NULL  ,
        "city" TEXT NOT NULL  ,
        "latitude" DOUBLE NOT NULL DEFAULT '0' ,
        "longitude" DOUBLE NOT NULL DEFAULT '0' ,
        "address" TEXT NOT NULL  ,
        PRIMARY KEY ("id")
    );
    """

    data = []
    # prepare data to insert
    for key in ramps_datails.keys():
        data.append((
            ramps_datails[key]["identifier"],
            ramps_datails[key]["name"],
            ramps_datails[key]["street"],
            ramps_datails[key]["zipCode"],
            ramps_datails[key]["city"],
            float(ramps_datails[key]["latitude"]),
            float(ramps_datails[key]["longitude"]),
            ramps_datails[key]["address"],
        ))
    execute(INSERT_STATEMENT_RAMPS, data)

def write_ramp_utilization_to_db(ramp_utilization_data, ramps_details):
    """
    Uses following table:
        CREATE TABLE "ramp_utilization" (
            "id" INTEGER NOT NULL  ,
            "ramp_id" INTEGER NOT NULL DEFAULT '0' ,
            "capacity" INTEGER NOT NULL DEFAULT '0' ,
            "utilization" INTEGER NOT NULL DEFAULT '0' ,
            "utilization_ratio" FLOAT NOT NULL DEFAULT '0' ,
            "available" INTEGER NOT NULL DEFAULT '0' ,
            "created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ,
            PRIMARY KEY ("id")
        );
        )
    :param ramp_data:
    :return:
    """
    data = []
    # prepare data to insert
    for key in ramps_details.keys():
        key = "ramp-" + key
        data.append((
            ramp_utilization_data[key]["identifier"],
            ramp_utilization_data[key]["capacity"],
            ramp_utilization_data[key]["utilization"],
            float(ramp_utilization_data[key]["utilization_ratio"]),
            ramp_utilization_data[key]["available"],
        ))

    execute(INSERT_STATEMENT_UTILIZATION, data)

