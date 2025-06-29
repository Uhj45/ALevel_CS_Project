import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time

class Ldr:
    """
    Class to retrieve and return light level from the LDR sensor connected to the ADC chip on channel 0
    """
    def __init__(self):
        """
        Initialises GPIO pins for ADC chip to use I2C bus
        :param self.lightlevel:
        """
        self.lightlevel = None

        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)
        self.ldr = AnalogIn(ads, ADS.P0)

    def get_light_level(self):
        """
        Returns the ldr reading
        :return: int value
        """
        self.lightlevel = self.ldr.value
        return self.lightlevel
