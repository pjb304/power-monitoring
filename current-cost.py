#!/usr/bin/env python3

from serial import Serial
from urllib.request import urlopen
from json import loads
from bs4 import BeautifulSoup
from os import system
from power_database import PowerDatabase
from datetime import datetime

PORT = "/dev/ttyUSB0"
BAUDRATE = 57600
TIMEOUT = 5
def get_external_temp():
    try:
        return loads(urlopen("http://api.openweathermap.org/data/2.5/weather?q=Southampton&units=metric&APPID=", timeout=2).read())['main']['temp']
    except Exception:
        return 0

def connect_receiver():
    serial_port = Serial(PORT, BAUDRATE, timeout=TIMEOUT)
    db = PowerDatabase()
    print("Serial port opened")
    while(True):
        try:
            resp = serial_port.readline()
            if( None == resp and resp == ""):
                continue
            parsed = BeautifulSoup(resp, features="lxml")
            if( parsed.msg is None):
                continue
            internal_temp = float(parsed.msg.tmpr.text)
            power = float(parsed.msg.watts.text)
            print("Power " + str(power))
            print("Temperature " + str(internal_temp))
#            save_rrd(power, internal_temp)
            db.store_reading(power, internal_temp, get_external_temp())
        except Exception as e:
            print(e)


def save_rrd(power, internal_temp):
    external_temp = get_external_temp()
    cmd = "rrdtool update powertemp.rrd N:%s:%s:%s" %(power, internal_temp, external_temp)
    print(cmd)
    system(cmd)

if __name__ ==  "__main__":
    connect_receiver()
