import adafruit_dht
import time
import board

class TempHumidity:
    """
    Gets the temperature and humidity readings from DHT22 sensor
    """
    def __init__(self):
        """
        Initialises all the attributes to None
        """
        self.temperature = None
        self.humidity = None
        self.sensor = None

    def get_temperature(self):
        """
        This function returns the temperature reading
        :return: float the temperature reading
        """
        # self.temperature = self.sensor.temperature
        # self.sensor.exit()  # This gets rid of the "lost access to message queue" error as it says that the sensor is exiting
        return self.temperature

    def get_humidity(self):
        """
        This function returns the humidity reading
        :return: int the humidity reading as a percentage
        """
        # self.humidity = self.sensor.humidity
        return self.humidity

    def read_sensors(self):
        """
        Initialises the GPIO pin for the DHT22 sensor to talk over the SPI bus
        This function retrieves the temperature and humidity reading from the sensor and assigns it to "self.temperature"
        and "self.humidity" respectively.
        :return:
        """
        self.sensor = adafruit_dht.DHT22(board.MOSI)  # The pin needs to be initialised here every time to get a reading,
                                                      # can't be in the init function as it will only initialise once and
                                                      # won't be able to call the get functions to get a new reading
                                                      # and will keep using the same value
        self.sensor.measure()
        self.temperature = self.sensor.temperature
        self.humidity = self.sensor.humidity
        self.sensor.exit()
