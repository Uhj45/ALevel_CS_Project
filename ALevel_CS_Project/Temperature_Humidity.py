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
        sensor.exit()  # This gets rid of the lost access to message queue error as it says that the sensor is exiting
        return self.temperature, self.humidity


readings = TempHumidity()  # Using the class TempHumidity, this creates the object for that class
readings.get_temperature_humidity()  # Calls method in the class
for i in range(0, 5):
    print(f"Temperature: {readings.temperature} °C", f"Humidity: {readings.humidity} %")
    time.sleep(1)
