import board
import neopixel
import RPi.GPIO as GPIO
import time


class Neopixel:
    def __init__(self, brightness=0, g=0, r=0, b=0):
        """
        Initialise the GPIO pins and Neopixel LED
        Allow user to change the brightness and the colour of the leds
        :param brightness: float value between 0.0 and 1.0 where 1.0 is full brightness
        :param g: int values between 0 and 255
        :param r: int values between 0 and 255
        :param b: int values between 0 and 255
        """
        self.brightness = brightness
        self.g = g
        self.r = r
        self.b = b

        GPIO.setmode(GPIO.BCM)
        order = neopixel.GRB
        self.GRBLED = neopixel.NeoPixel(pin=board.D12, n=1, bpp=3, brightness=self.brightness, auto_write=False, pixel_order=order)

    def turn_led_on(self):
        """
        Turns the LED on
        :return:
        """
        self.GRBLED.fill((255, 0, 0))
        self.GRBLED.show()

    def turn_led_off(self):
        """
        Turns the LED off
        :return:
        """
        self.GRBLED.fill((0, 0, 0))
        self.GRBLED.show()

    def change_colour(self):
        """
        Allows the user to change the colour of the LED
        :return:
        """
        self.GRBLED.fill((self.g, self.r, self.b))
        self.GRBLED.show()


def flash_led(self):
    """
    This will flash the LED for any colour
    :return:
    """
    for i in range(0, 6):
        self.GRBLED.fill((self.g, self.r, self.b))
        self.GRBLED.show()
        time.sleep(1)
        self.GRBLED.fill((0, 0, 0))
        self.GRBLED.show()
        time.sleep(1)


def pulse_led(self):
    """
    Increases and decreases the intensity of the LEDs to show pulsing

    :return:
    """
    while True:
        for i in range(255):
            self.GRBLED.fill((i, self.r, self.b))
            self.GRBLED.show()
            time.sleep(0.001)

        self.GRBLED.fill((0, 0, 0))
        self.GRBLED.show()

        for i in reversed(range(255)):
            self.GRBLED.fill((i, self.r, self.b))
            self.GRBLED.show()
            time.sleep(0.001)

# TODO: add function to flash leds
# TODO: pulse leds,
# TODO: add docstrings for functions
# TODO: change colour function should just change the colour
