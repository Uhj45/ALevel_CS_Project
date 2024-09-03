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
        self.sensor = adafruit_dht.DHT22(board.MOSI)

    def get_temperature(self):
        """
        Gets the temperature and humidity from the sensor and returns them
        :return: returns temperature and humidity
        """

        self.temperature = self.sensor.temperature
# self.sensor.exit()  # This gets rid of the lost access to message queue error as it says that the sensor is exiting
        return self.temperature

    def get_humidity(self):
        self.humidity = self.sensor.humidity
        return self.humidity
