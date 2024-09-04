import adafruit_dht
import time
import board


class TempHumidity:
    """
    Gets the temperature and humidity readings from DHT22 sensor
    """
    def __init__(self):
        """
        Initialises the GPIO pin for the DHT22 sensor to talk over the SPI bus
        """
        self.temperature = None
        self.humidity = None
        self.sensor = None

    def get_temperature(self):

        # self.temperature = self.sensor.temperature
        # self.sensor.exit()  # This gets rid of the lost access to message queue error as it says that the sensor is exiting
        return self.temperature

    def get_humidity(self):
        # self.humidity = self.sensor.humidity
        return self.humidity

    def read_sensors(self):
        self.sensor = adafruit_dht.DHT22(board.MOSI)
        self.sensor.measure()
        self.temperature = self.sensor.temperature
        self.humidity = self.sensor.humidity
        self.sensor.exit()
