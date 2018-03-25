from Toon import Toon
from datetime import datetime
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
import time
import sys


toonusername = "YOURTOONUSERNAME"
toonpassword = "YOURTOONPASSWORD"

toon = Toon(toonusername, toonpassword)

client = InfluxDBClient('address', port, 'user', 'password', 'database', ssl=False)


def save_data(sensor):
    toon.login()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    thermostat = toon.get_thermostat_info()
    temperature = temp = float(thermostat["currentTemp"]) / 100
    power = toon.get_power_usage()
    toon.logout()
    if temperature is not None:
            json_body = [
                {
                    "measurement": "toon",
                    "timestamp": current_time,
                    "fields": {
                        "temperature": float("{0:0.1f}".format(temperature)),
                        "power": power["value"]
                    }
                }
            ]
            # print(json_body) #for debug, not enabled
            client.write_points(json_body)

while True:
    try:
        save_data('toon')
        time.sleep(60)
    except KeyboardInterrupt:
        sys.exit()
    except KeyError:
         continue

