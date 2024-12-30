# Algorithms for the fan: Schimtt Trigger, P, PI, PID
from PWM_Fan import PCA9685Fan
from Distance_Sensor import DistanceSensor
from Neopixel_LEDs import Neopixel2
from sql_database import StoreReadings
import time


class Schmitttrigger:
    def __init__(self, target_height, lower_threshold, upper_threshold):
        """
        This class will contain the schmitt trigger algorithm to hover the fan at a certain height
        :param target_height: This is given by the user through the webpage
        :param lower_threshold: This is calculated using the target height and the threshold given by the user
        :param upper_threshold: This is calculated using the target height and the threshold given by the user
        """
        self.target_height = target_height
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold
        self.fan = PCA9685Fan()
        self.distance_readings = DistanceSensor()
        self.LED1 = Neopixel2(brightness=0.8)
        self.LED2 = Neopixel2(brightness=0.8)
        self.results = StoreReadings()

    def calc_average_height(self):
        heights_list = []
        for i in range(0, 5):
            height = 23 - self.distance_readings.get_distance()
            heights_list.append(height)
        average_height = sum(heights_list)/len(heights_list)
        return average_height

    def check_float_stable(self, target_height, threshold, upper_threshold, lower_threshold, runid, floats):
        previous_height = 0
        current_av_height = 0
        for j in range(0, 5):
            current_av_height = self.calc_average_height()
            print(f"Current height: {current_av_height}, Previous height: {previous_height}")
            if current_av_height > previous_height:
                print("Keep fan speed the same")
            elif current_av_height < previous_height:
                self.fan.increment_fan_speed(2)
            previous_height = current_av_height
        distance = current_av_height
        self.results.add_item(runid, distance, target_height, threshold, upper_threshold, lower_threshold, self.fan.get_fan_speed(), floats, kp=0, ki=0, kd=0)
        return distance
    def schmitt_trigger_alg(self, target_height, upper_threshold, lower_threshold, threshold, runid, floats):
        self.fan.turn_fan_on()
        self.fan.set_fan_speed(60)
        for i in range(0, 50):
            # distance = 23 - self.distance_readings.get_distance()  # This measures the distance and subtracts from 23 (original height)
            distance = self.calc_average_height()
            print(f"Distance ({i}): {distance}")
            self.results.add_item(runid, distance, target_height, threshold, upper_threshold, lower_threshold, self.fan.get_fan_speed(), floats, kp=0, ki=0, kd=0)
            if distance > float(upper_threshold):
                # Turn LED1 on and increase fan speed and add height value to table
                self.LED1.set_predefined_colour("red")
                self.LED1.turn_led_on()
                self.fan.decrement_fan_speed(2)
            elif distance < float(lower_threshold):
                # Turn LED1 on and decrease fan speed and add height value to table
                self.LED1.set_predefined_colour("red")
                self.LED1.turn_led_on()
                self.fan.increment_fan_speed(2)
            elif float(lower_threshold) < distance < float(upper_threshold) or distance == float(target_height):
                # Turn LED2 On and Add height value to table
                self.LED1.turn_led_off()
                self.LED2.set_predefined_colour("green")
                self.LED2.turn_led_on()

            else:
                self.fan.turn_fan_off()

            self.check_float_stable(target_height, threshold, upper_threshold, lower_threshold, runid, floats)
            time.sleep(0.5)


class Algorithms:
    def __init__(self, float, target_height):
        self.float = float
        self.target_height = target_height


class ProportionalAlgorithm(Algorithms):
    def __init__(self, float, target_height, Kp):
        super().__init__(float, target_height)
        self.float = float
        self.target_height = target_height
        self.Kp = Kp

    def get_config(self):
        print(f"Float: {self.float}, Target Height: {self.target_height}, Kp: {self.Kp}")

class ProportionalIntegralAlgorithm(Algorithms):
    def __init__(self, float, target_height, Kp, Ki):
        super().__init__(float, target_height)
        self.float = float
        self.target_height = target_height
        self.Kp = Kp
        self.Ki = Ki

    def get_config(self):
        print(f"Float: {self.float}, Target Height: {self.target_height}, Kp: {self.Kp}, Ki: {self.Ki}")

class PIDAlgorithm(Algorithms):
    def __init__(self, float, target_height, Kp, Ki, Kd):
        super().__init__(float, target_height)
        self.float = float
        self.target_height = target_height
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

    def get_config(self):
        print(f"Float: {self.float}, Target Height: {self.target_height}, Kp: {self.Kp}, Ki: {self.Ki}, Kd: {self.Kd}")

