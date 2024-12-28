import RPi.GPIO as GPIO
import time
import board
from adafruit_pca9685 import PCA9685

class Fan:
    """
    class to control the fan speed
    * Allow user to turn the fan on to max speed
    * Allow the user to turn the fan off
    * Allow the user to increment or decrement the fan speed
    * Allow the user to set the fan speed to any value between 0 an 100

    """
    def __init__(self, fan_speed=0):
        """
        Initialise the class by setting the GPIO pins used, the frequency of the PWM Dutycycle and setting the fan speed
        to 0% if the fan_speed hasn't been supplied
        :param fan_speed: int value, this sets the fan speed to a value between 0% (fan is off) and 100% (fan at max speed)
        """
        self.fan_speed = fan_speed
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(13, GPIO.OUT)
        Frequency = 50
        self.pwmFan = GPIO.PWM(13, Frequency)
        self.pwmFan.start(0)

    @staticmethod
    def check_speed_in_range(fan_speed):
        if 0 <= int(fan_speed) <= 100:
            return True
        else:
            print("Number is not between 0 and 100")
            return False

    def turn_fan_on(self):
        """
        This function will set the fan speed to max and switch it on
        :return:
        """
        self.fan_speed = 100
        self.pwmFan.ChangeDutyCycle(self.fan_speed)

    def turn_fan_off(self):
        """
        Sets the  fan speed back to zero turns it off
        :return:
        """
        self.fan_speed = 0
        self.pwmFan.ChangeDutyCycle(self.fan_speed)

    def get_speed(self):
        return self.fan_speed

    def set_speed(self, fan_speed):
        """
        Allow user to set whatever speed they want
        :return:
        """
        if self.check_speed_in_range(fan_speed):
            self.fan_speed = fan_speed
            self.pwmFan.ChangeDutyCycle(self.fan_speed)
            print(f"Fan speed is at: {self.fan_speed}")

    def increment_fan_speed(self, increment):
        speed_to_check = self.fan_speed + increment
        if self.check_speed_in_range(speed_to_check):
            self.fan_speed = self.fan_speed + increment
            self.pwmFan.ChangeDutyCycle(self.fan_speed)
            print(f"Fan speed was incremented by: {increment}", f"Fan speed is at: {self.fan_speed}")

    def decrement_fan_speed(self, decrement):
        if self.check_speed_in_range(self.fan_speed - decrement):
            self.fan_speed = self.fan_speed - decrement
            self.pwmFan.ChangeDutyCycle(self.fan_speed)
            print(f"Fan speed was decremented by {decrement}", f"Fan speed is at {self.fan_speed}")


class PCA9685Fan:
    """
    class to control the fan using the PCA9685 chip
    """
    def __init__(self, channel=0, fan_speed=0, duty_cycle=0):
        """
        Initialises the object with a channel number and a fan speed. If nothing is passed defaults to 0
        :param channel: int channel number (0 to 15)
        :param fan_speed: int percentage
        :param duty_cycle: int absolute value for the duty cycle (0 to 65535)
        """
        self.channel = channel
        self.percentage_fan_speed = fan_speed
        self.duty_cycle = duty_cycle
        i2c = board.I2C()
        self.pca = PCA9685(i2c)
        self.pca.frequency = 1400

    def check_fan_speed(self, fan_speed):
        if 0 <= fan_speed <= 100:
            self.percentage_fan_speed = fan_speed
            return True
        else:
            print(f"Value is not between 0 and 100, {fan_speed}, {type(fan_speed)}")

    def turn_fan_on(self):
        self.duty_cycle = 65300
        print(type(hex(self.duty_cycle)))
        # self.pca.channels[1].duty_cycle = 0xFFFF
        self.pca.channels[1].duty_cycle = self.duty_cycle

    def turn_fan_off(self):
        self.duty_cycle = 0
        self.pca.channels[1].duty_cycle = self.duty_cycle

    def get_fan_speed(self):
        return self.pca.channels[1].duty_cycle

    def set_fan_speed(self, fan_speed):
        """
        This function takes a speed and checks its between 0% and 100%, it then converts this percentage to an absolute value that is needed and updates the duty cycle
        :param fan_speed: integer that needs to be between 0% and 100%
        :return:
        """
        if self.check_fan_speed(fan_speed):
            self.duty_cycle = int((fan_speed / 100) * 65535)
            # self.fan_speed = 32767
            print(self.percentage_fan_speed)
            self.pca.channels[1].duty_cycle = self.duty_cycle
            print(f"Fan speed is {fan_speed}")

    def increment_fan_speed(self, increment):
        speed_to_check = self.percentage_fan_speed + increment
        if self.check_fan_speed(speed_to_check):
            self.percentage_fan_speed = speed_to_check
            self.set_fan_speed(self.percentage_fan_speed)
            print(f"Fan speed was incremented by: {increment}", f"Fan speed is at: {self.percentage_fan_speed}")

    def decrement_fan_speed(self, decrement):
        if self.check_fan_speed(self.percentage_fan_speed - decrement):
            self.percentage_fan_speed = self.percentage_fan_speed - decrement
            self.set_fan_speed(self.percentage_fan_speed)
            print(f"Fan speed was decremented by {decrement}", f"Fan speed is at {self.percentage_fan_speed}")