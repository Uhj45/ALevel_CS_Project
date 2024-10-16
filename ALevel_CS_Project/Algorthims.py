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

    def schmitt_trigger_alg(self, target_height, upper_threshold, lower_threshold, threshold, runid, floats):
        fan = PCA9685Fan()
        fan.turn_fan_on()
        fan.set_fan_speed(60)
        distance_readings = DistanceSensor()
        LED1 = Neopixel2(brightness=0.8)
        LED2 = Neopixel2(brightness=0.8)
        results = StoreReadings()
        for i in range(0, 50):
            distance = distance_readings.get_distance()
            print(f"Distance: {distance}")
            results.add_item(runid, distance, target_height, threshold, upper_threshold, lower_threshold, fan.get_fan_speed(), floats, kp=0, ki=0, kd=0)
            if distance < float(lower_threshold):
                # Turn LED1 on and increase fan speed and add height value to table
                LED1.set_predefined_colour("red")
                LED1.turn_led_on()
                fan.decrement_fan_speed(2)
            elif distance > float(upper_threshold):
                # Turn LED1 on and decrease fan speed and add height value to table
                LED1.set_predefined_colour("red")
                LED1.turn_led_on()
                fan.increment_fan_speed(2)
            elif float(lower_threshold) < distance < float(upper_threshold) or distance == float(target_height):
                # Turn LED2 On and Add height value to table
                LED1.turn_led_off()
                LED2.set_predefined_colour("green")
                LED2.turn_led_on()

            else:
                fan.turn_fan_off()

            time.sleep(0.5)





