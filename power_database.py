from configobj import ConfigObj
from datetime import datetime

import MySQLdb

class PowerDatabase:
    
    def __init__(self):
        self.read_config()
        self.connect_database()

    def read_config(self):
        config = ConfigObj("cc-db.ini")
        self.host = config["host"]
        self.user = config["user"]
        self.password = config["password"]
        self.database = config["database"]

    def connect_database(self):
        self.db = MySQLdb.connect(
            host = self.host,
            user = self.user,
            passwd = self.password,
            db = self.database)

    def store_reading(self, power, internal, external):
        try:
            self.store_power("cc128", power)
        except MySQLdb.OperationalError:
            self.connect_database()
            self.store_power("cc128", power)
        self.store_temperature("cc128", internal)
        self.store_temperature("openwthr", external)

    def store_power(self, device, reading):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO power_readings (timestamp, device, value) VALUES (%s, %s, %s);", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), device, reading))
        cursor.close()
        self.db.commit()

    def store_temperature(self, device, reading):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO temperature_readings (timestamp, device, value) VALUES (%s, %s, %s);", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), device, reading))
        cursor.close()
        self.db.commit()
