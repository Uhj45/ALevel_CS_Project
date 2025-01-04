import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time


class Ldr:
    """
    class to retrieve light level from the LDR sensor
    """
    def __init__(self):
        """
        Initialises GPIO pins for LDR to use I2C bus
        :param lightlevel:
        """
        self.lightlevel = None

        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)
        self.ldr = AnalogIn(ads, ADS.P0)

    def get_light_level(self):
        """
        returns the ldr reading
        :return: int value
        """
        self.lightlevel = self.ldr.value
        return self.lightlevel
