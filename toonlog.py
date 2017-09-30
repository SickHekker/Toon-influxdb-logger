from Toon import Toon
from datetime import datetime
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError

toonusername = "YOURTOONUSERNAME"
toonpassword = "YOURTOONPASSWORD"

toon = Toon(toonusername,toonpassword)

client = InfluxDBClient('address', port, 'user', 'password', 'database')

def save_data(sensor):
	toon.login()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    thermostat = toon.get_thermostat_info()
	temperature = temp = float(thermostat["currentTemp"]) / 100"
	toon.logout()
    if temperature is not None:
        print('Sensor={0}  Temp={1:0.1f}*C'.format(sensor, temperature))
        json_body = [
            {
                "measurement": "{0}_temperature".format(sensor),
                "tags": {
                    "celsius": "temperature"
                },
                "timestamp": current_time,
                "fields": {
                    "value": float("{0:0.1f}".format(temperature))
                }
            }]
        # print(json_body)
        client.write_points(json_body)
		
		

save_data('toon')
