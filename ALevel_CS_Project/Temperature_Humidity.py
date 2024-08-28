import adafruit_dht
import time
import board

class TempHumidity:
    def __int__(self, temperature=None, humidity=None):
        self.temperature = temperature
        self.humidity = humidity

    def get_temperature_humidity(self):
        sensor = adafruit_dht.DHT22(board.MOSI)
        return sensor.temperature, sensor.humidity


# for i in range(0, 5):
#     print(f"Temperature: {temperature} °C", f"Humidity: {humidity} %")
#     time.sleep(1)

readings = TempHumidity()
print(readings.get_temperature_humidity())