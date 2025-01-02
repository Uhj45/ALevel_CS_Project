# Algorithms for the fan: Schimtt Trigger, P, PI, PID
from PWM_Fan import PCA9685Fan
from Distance_Sensor import DistanceSensor
from Neopixel_LEDs import Neopixel2
from OLED_Display import Oled
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

    def check_float_stable(self, previous_height):
        current_av_height = 0
        for j in range(0, 3):
            current_av_height = self.calc_average_height()
            print(f"Current height: {current_av_height}, Previous height: {previous_height}")
            if current_av_height > previous_height:
                print("Keep fan speed the same")
            previous_height = current_av_height
        distance = current_av_height
        return distance

    def schmitt_trigger_alg(self, target_height, upper_threshold, lower_threshold, threshold, runid, floats, duration):
        previous_height = 0
        self.fan.turn_fan_on()
        self.fan.set_fan_speed(60)
        start_time = time.time()
        print(start_time)
        elapsed_time = 0
        while elapsed_time < duration:
            distance = self.check_float_stable(previous_height)
            self.results.add_item(runid, distance, target_height, threshold, upper_threshold, lower_threshold, self.fan.get_fan_speed(), floats, kp=0, ki=0, kd=0, p_term=0,d_term=0,i_term=0)
            print(f"Distance ({elapsed_time}): {distance}")
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

            time.sleep(0.5)
            elapsed_time = time.time() - start_time

class Algorithms:
    def __init__(self, floats, target_height):
        self.float = floats
        self.target_height = target_height
        self.fan = PCA9685Fan()
        self.distance_readings = DistanceSensor()
        self.leds = Neopixel2(brightness=0.8, phyiscal_led="LED2")
        self.oled_display = Oled()
        self.results = StoreReadings()
        self.Kp = 0
        self.Ki = 0
        self.Kd = 0
        self.threshold = 0
        self.upper_threshold = 0
        self.lower_threshold = 0
        self.p_term = 0
        self.i_term = 0
        self.d_term = 0
        self.fan_speed = self.control = 0
        self.height = 0
        self.error = 0
        self.integral_error = 0
        self.fan.set_fan_speed(0)             # This is to initialise the fan speed to 0 so that the float is at the bottom
        time.sleep(2)                         # This is to give the float time to fall to the bottom if it was already at the top

    def log_values_to_screen(self, measured_height):
        print(f"P_Error: {self.target_height} - {measured_height:5.2f} = {self.error:5.2f}, P_Term: {self.p_term:9.2f}, I_Error: {self.integral_error:9.2f}, I_Term: {self.i_term:9.2f}, D_Term: {self.d_term:9.2f} Duty_Cycle: {self.control}")

    def add_pid_values(self, runid, measured_height):
        self.results.add_item(runid,measured_height,self.target_height,self.threshold,self.upper_threshold,self.lower_threshold,self.control,self.float,self.Kp,self.p_term,self.Ki,self.i_term,self.Kd,self.d_term)

    def calc_average_height(self):
        heights_list = []
        for i in range(0, 3):
            height = self.distance_readings.get_distance()
            heights_list.append(height)
        average_height = sum(heights_list)/len(heights_list)
        return average_height

    def light_leds(self, measured_height, target_height):
        if (target_height - 1) < measured_height < (target_height + 1):
            self.leds.set_predefined_colour("green")
            self.leds.turn_led_on()
        else:
            self.leds.set_predefined_colour("red")
            self.leds.turn_led_on()

    def log_values_to_oled_screen(self, measured_height, elapsed_time):
        self.oled_display.clear_screen()
        self.oled_display.display_text(f"AH : {measured_height:.2f} ({self.target_height})",0,0,1)
        self.oled_display.display_text(f"Fan: {self.control}",0, 12,1)
        self.oled_display.display_text(f"ET: {int(elapsed_time)}",0,24,1)

class ProportionalAlgorithm(Algorithms):
    def __init__(self, floats, target_height, Kp):
        super().__init__(floats, target_height)
        self.float = floats
        self.target_height = target_height
        self.Kp = Kp
        self.error = 0

    def calculate_proportional_term(self, measured_height):
        """
        This function will take in the measured height and the target height to calculate a value for
        the proportional term
        :param measured_height: this is a reading from the distance sensor.
        :return:
        """
        self.error = measured_height - self.target_height
        proportional_term = int(self.Kp * self.error)
        if proportional_term < 44000:
            proportional_term = 44000
        return proportional_term
        # return abs(proportional_term)

    def run_proportional_algorithm(self, runid, duration):
        """
        This will run in a while loop for a set amount of time determined by the user.
        This will try to lift the object to the target height.
        :return:
        """
        start_time = time.time()
        print(start_time)
        elapsed_time = 0
        while elapsed_time < duration:
            measured_height = self.calc_average_height()
            # print(measured_height)
            self.p_term = self.calculate_proportional_term(measured_height)
            self.control = self.p_term
            self.log_values_to_screen(measured_height)
            self.log_values_to_oled_screen(measured_height, elapsed_time)
            self.light_leds(measured_height, self.target_height)
            self.add_pid_values(runid, measured_height)
            if measured_height == self.target_height:
                print("Fan speed constant")
            else:
                self.fan.set_raw_fan_speed(self.control)
            elapsed_time = time.time() - start_time
            self.leds.turn_led_off()

    def get_config(self):
        print(f"Float: {self.float}, Target Height: {self.target_height}, Kp: {self.Kp}")

class ProportionalIntegralAlgorithm(ProportionalAlgorithm):
    def __init__(self, floats, target_height, Kp, Ki):
        super().__init__(floats, target_height, Kp)
        self.float = floats
        self.target_height = target_height
        self.Kp = Kp
        self.Ki = Ki
        self.integral_error = 0

    def calculate_integral_term(self, measured_height):
        # # self.error = self.calc_average_height() - self.target_height
        self.error = measured_height - self.target_height
        self.integral_error = self.integral_error + self.error
        integral_term = self.integral_error * self.Ki
        return integral_term

    def run_proportional_integral_algorithm(self, runid, duration):
        start_time = time.time()
        print(start_time)
        elapsed_time = 0

        while elapsed_time < duration:
            measured_height = self.calc_average_height()
            self.p_term = self.calculate_proportional_term(measured_height)
            self.i_term = self.calculate_integral_term(measured_height)
            self.control = int(self.p_term + self.i_term)
            self.log_values_to_screen(measured_height)
            self.log_values_to_oled_screen(measured_height, elapsed_time)
            self.light_leds(measured_height, self.target_height)
            self.add_pid_values(runid, measured_height)
            if measured_height == self.target_height:
                print("Fan speed constant")
            else:
                self.fan.set_raw_fan_speed(self.control)
            elapsed_time = time.time() - start_time
            self.leds.turn_led_off()

    def get_config(self):
        print(f"Float: {self.float}, Target Height: {self.target_height}, Kp: {self.Kp}, Ki: {self.Ki}")

class PIDAlgorithm(ProportionalIntegralAlgorithm):
    def __init__(self, floats, target_height, Kp, Ki, Kd):
        super().__init__(floats, target_height, Kp, Ki)
        self.float = floats
        self.target_height = target_height
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.dt = 1
        self.prev_error = 0

    def calculate_derivative_term(self):
        derivative = self.error - self.prev_error
        derivative_term = derivative * self.Kd * self.dt
        return derivative_term

    def run_pid_algorithm(self, runid, duration):
        start_time = time.time()
        print(start_time)
        elapsed_time = 0
        while elapsed_time < duration:
            measured_height = self.calc_average_height()
            self.p_term = self.calculate_proportional_term(measured_height)
            self.i_term = self.calculate_integral_term(measured_height)
            self.d_term = self.calculate_derivative_term()
            self.control = int(self.p_term + self.i_term + self.d_term)
            self.log_values_to_screen(measured_height)
            self.log_values_to_oled_screen(measured_height, elapsed_time)
            self.light_leds(measured_height, self.target_height)
            self.add_pid_values(runid, measured_height)
            if measured_height == self.target_height:
                print("Fan speed constant")
            else:
                self.fan.set_raw_fan_speed(self.control)
            elapsed_time = time.time() - start_time
            self.leds.turn_led_off()
    def get_config(self):
        print(f"Float: {self.float}, Target Height: {self.target_height}, Kp: {self.Kp}, Ki: {self.Ki}, Kd: {self.Kd}")

