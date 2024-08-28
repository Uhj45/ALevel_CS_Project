import adafruit_dht
import time
import board

class TempHumidity:
    def __init__(self, temperature=None, humidity=None):
        self.temperature = temperature
        self.humidity = humidity

    def get_temperature_humidity(self):
        sensor = adafruit_dht.DHT22(board.MOSI)
        self.temperature = sensor.temperature
        self.humidity = sensor.humidity
        return self.temperature, self.humidity


# for i in range(0, 5):
#     print(f"Temperature: {temperature} °C", f"Humidity: {humidity} %")
#     time.sleep(1)

readings = TempHumidity()
readings.get_temperature_humidity()
print(f"Temperature: {readings.temperature} °C", f"Humidity: {readings.humidity} %")