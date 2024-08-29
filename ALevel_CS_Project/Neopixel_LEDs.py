import board
import neopixel
import RPi.GPIO as GPIO
import time

class Neopixel:
    def __init__(self, brightness, g, r, b):
        """
        These parameters are local to the class are can only be used inside the class
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

    def on_off(self):
        self.GRBLED2.fill((255, 0, 0))
        self.GRBLED2.show()
        time.sleep(1)
        self.GRBLED2.fill((0, 0, 0))
        self.GRBLED2.show()

    def change_colour(self):
        self.GRBLED2.fill((self.g, self.r, self.b))
        self.GRBLED2.show()
        time.sleep(1)
        self.GRBLED2.fill((0, 0, 0))
        self.GRBLED2.show()


# led = Neopixel(1.0, 255, 56, 79)
# led.change_colour()

led2 = Neopixel(0.8, 0, 100, 200)
led2.on_off()

