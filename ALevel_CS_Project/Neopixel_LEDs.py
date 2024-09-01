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

    def get_colour(self):
        return self.g, self.r, self.b

    def set_colour(self, g, r, b):
        self.g = g
        self.r = r
        self.b = b

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
        Each colour will increase/decrease by the same factor/ratio so that the required colour is kept the same
        User can pulse colour that has already been set
        To pulse from 0 up to 255, calculate the ratio of the three values and multiply it by the initial value
        To pulse down from 255 to 0,
        :return:
        """
        g = 22
        r = 59
        b = 31

        g = g / 255  # fraction of the sum of the
        r = (r / 255)
        b = (b / 255)
        print("Ratio: ", g, ", ", r, ", ", b, "\n")

        i = 0
        g2 = r2 = b2 = 0
        while max(g2, r2, b2) < 255:
            i += 1
            g2 = g*i
            r2 = r*i
            b2 = b*i
            # for i in range(0, 255):
                #print(g*i, ", ", r*i, ", ", b*i)

            print(f"{int(g2)}, {int(r2)}, {int(b2)}, Max value: {max(int(g2), int(r2), int(b2))} ", end="\r")

            # print(int(g2), ", ", int(r2), ", ", int(b2), "Max value: ", max(int(g2),int(r2),int(b2)))

            self.GRBLED.fill((int(g2), int(r2), int(b2)))
            self.GRBLED.show()
            time.sleep(0.01)


        # ratio_g = int(255 / self.g)
        # ratio_r = int(255 / self.r)
        # ratio_b = int(255 / self.b)
        #
        # while True:
        #     if self.g or self.r or self.b == 255:
        #
        #     else:
        #         for i in range(255):
        #             self.GRBLED.fill((self.g * ratio_g, self.r * ratio_r, self.b * ratio_b))
        #             self.GRBLED.show()
        #             time.sleep(0.001)
        #
        #         for i in reversed(range(255)):
        #             self.GRBLED.fill((self.g * ratio_g, self.r * ratio_r, self.b * ratio_b))
        #             self.GRBLED.show()
        #             time.sleep(0.001)

# TODO: add function to flash leds
# TODO: pulse leds,
# TODO: add docstrings for functions
# TODO: change colour function should just change the colour
