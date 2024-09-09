import RPi.GPIO as GPIO
import time


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


# fan = Fan()
# fan.turn_fan_on()
# time.sleep(10)
# fan.turn_fan_off()
# time.sleep(5)
# fan.turn_fan_on()
# fan.set_speed(50)
# time.sleep(10)
# print(fan.get_speed())
# fan.increment_fan_speed(200)
# print(fan.get_speed())
# fan.set_speed(fan.get_speed() + 5)
# time.sleep(10)
# fan.decrement_fan_speed(12)
