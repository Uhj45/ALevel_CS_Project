import board
import neopixel
import RPi.GPIO as GPIO
import time


class Neopixel:
    def __init__(self, brightness=0, g=0, r=0, b=0,):
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
        """
        These parameters will update the instance variables in the init function
        :param g:
        :param r:
        :param b:
        :return:
        """
        self.g = g
        self.r = r
        self.b = b

    def set_predefined_colour(self, colour):
        """
        Allow the user to set to a predefined colour
        Using a dictionary to store the list of colours and their rgb values
        This will then get the rgb values and assign them to the instance variable
        :return:
        """
        colours = {
            'green': (255, 0, 0),
            'red': (0, 255, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 0, 255),
            'orange': (153, 255, 0),
            'pink': (51, 255, 204),
            'purple': (0, 153, 204),
            'brown': (102, 153, 51),
            'mint': (255, 102, 204),
        }
        self.g, self.r, self.b = colours[colour]

        print(colours)
        print(colour)
        print(self.g, self.r, self.b)

    def turn_led_on(self):
        """
        Turns the LED on
        :return:
        """
        self.GRBLED.fill((self.g, self.r, self.b))
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
        :param: flash_iteration asks the user how many times they want to flash the LED
        :return:
        """
        self.GRBLED.fill((self.g, self.r, self.b))
        self.GRBLED.show()

    def flash_led(self, flash_iteration):
        """
        This will flash the LED for any colour
        :return:
        """
        for i in range(0, flash_iteration):
            self.GRBLED.fill((self.g, self.r, self.b))
            self.GRBLED.show()
            time.sleep(1)
            self.GRBLED.fill((0, 0, 0))
            self.GRBLED.show()
            time.sleep(1)

    def pulse_led(self, pulse_iteration):
        """
        Increases and decreases the intensity of the LEDs to show pulsing
        Each colour will increase/decrease by the same factor/ratio so that the required colour is kept the same
        User can pulse colour that has already been set
        To pulse from 0 up to 255, calculate the ratio of the three values and multiply it by the initial value
        To pulse down from 255 to 0, does the opposite to the comment above
        :param: pulse_iteration allows the user to input a value to pulse the LED a certain number of times
        :return:
        """
        g = self.g
        r = self.r
        b = self.b

        ratio_g = g / 255  # fraction of 255
        ratio_r = r / 255
        ratio_b = b / 255
        # print("Ratio: ", g, ", ", r, ", ", b, "\n")

        for j in range(0, pulse_iteration):
            i = 0  # Increment
            pulse_up_g = pulse_up_r = pulse_up_b = 0
            print("\nLED Fade in")
            while max(pulse_up_g, pulse_up_r, pulse_up_b) < 255:  # Checks value is less than 255 if not it will stop the loop
                self.GRBLED.fill((int(pulse_up_g), int(pulse_up_r), int(pulse_up_b)))   # sets values before calculating the next value
                self.GRBLED.show()
                i += 5
                pulse_up_g = ratio_g*i  # Calculates the new value from the ratio for each colour value and increases after each increment
                pulse_up_r = ratio_r*i
                pulse_up_b = ratio_b*i
                print(f"{i}, {int(pulse_up_g)}, {int(pulse_up_r)}, {int(pulse_up_b)}, Max value: {max(int(pulse_up_g), int(pulse_up_r), int(pulse_up_b))} ", end="\r")
                time.sleep(0.01)

            pulse_down_g = pulse_up_g
            pulse_down_r = pulse_up_r
            pulse_down_b = pulse_up_b
            print("\nLED fade out")
            while min(pulse_down_g, pulse_down_r, pulse_down_b) > 0:  # Checks if value is greater than 0 if not it will stop the loop
                self.GRBLED.fill((int(pulse_down_g), int(pulse_down_r), int(pulse_down_b)))  # Sets the calculated value
                self.GRBLED.show()
                i -= 5
                pulse_down_g = ratio_g*i  # Calculates the new value from the ratio for each colour value and decreases after each decrement
                pulse_down_r = ratio_r*i
                pulse_down_b = ratio_b*i
                print(f"{i} ,{int(pulse_down_g)}, {int(pulse_down_r)}, {int(pulse_down_b)}, Min value: {min(int(pulse_down_g), int(pulse_down_r), int(pulse_down_b))} ", end="\r")
                time.sleep(0.01)

# TODO: add function to flash leds
# TODO: pulse leds,
# TODO: add docstrings for functions
# TODO: change colour function should just change the colour
# TODO: Update variable names to be meaningful
# TODO: Add for loop with a parameter that allows the user to choose how many times they want to pulse the LED
# TODO: Do same for flash_led function
