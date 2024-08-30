import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time


class Ldr:
    def __init__(self, lightlevel=None):
        self.lightlevel = lightlevel

    def get_light_level(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)
        ldr = AnalogIn(ads, ADS.P0)
        self.lightlevel = ldr.value
        return self.lightlevel
