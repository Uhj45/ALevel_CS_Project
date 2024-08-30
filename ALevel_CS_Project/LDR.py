import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time


class Ldr:
    def __init__(self, lightlevel=None):
        """
        Initialises GPIO pins for LDR
        :param lightlevel:
        """
        self.lightlevel = lightlevel

        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)
        self.ldr = AnalogIn(ads, ADS.P0)
    def get_light_level(self):
        """
        gets light readings from ldr and returns them
        :return:
        """
        self.lightlevel = self.ldr.value
        return self.lightlevel
