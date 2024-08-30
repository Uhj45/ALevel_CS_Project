import board
import neopixel
import RPi.GPIO as GPIO
import time


class Neopixel:
    def __init__(self, brightness, g, r, b):
        """
        These instance variables are local to the class are can only be used inside the class
        Allow user to change the brightness and the colour of the leds
        :param brightness:
        :param g:
        :param r:
        :param b:
        """
        self.brightness = brightness
        self.g = g
        self.r = r
        self.b = b

        GPIO.setmode(GPIO.BCM)
        order = neopixel.GRB
        self.GRBLED2 = neopixel.NeoPixel(pin=board.D12, n=1, bpp=3, brightness=self.brightness, auto_write=False, pixel_order=order)

    def turn_led_on(self):
        self.GRBLED2.fill((self.g, self.r, self.b))
        self.GRBLED2.show()

    def turn_led_off(self):
        self.GRBLED2.fill((0, 0, 0))
        self.GRBLED2.show()

    def change_colour(self):
        self.GRBLED2.fill((self.g, self.r, self.b))
        self.GRBLED2.show()
        time.sleep(1)
        self.GRBLED2.fill((0, 0, 0))
        self.GRBLED2.show()




