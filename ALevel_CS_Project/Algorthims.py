# Algorithms for the fan: Schimtt Trigger, P, PI, PID
from PWM_Fan import PwmFan
from Distance_Sensor import DistanceSensor
from Neopixel_LEDs import NeopixelLeds
from OLED_Display import Oled
from sql_database import StoreReadings
import time


class Algorithms:
    """
    This is the base class for all the algorithms which will inherit these attributes
    """
    def __init__(self, hover_foam, target_height):
        self.hover_foam = hover_foam
        self.target_height = target_height
        self.fan = PwmFan()
        self.distance_readings = DistanceSensor()
        self.left_led = NeopixelLeds(brightness=0.8, phyiscal_led="LEFT_LED")
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
        print(f"P_Error: {self.target_height} - {measured_height:5.2f} = {self.error:5.2f}, P_Term: {self.p_term:9.2f}, "
              f"I_Error: {self.integral_error:9.2f}, I_Term: {self.i_term:9.2f}, D_Term: {self.d_term:9.2f} Duty_Cycle: {self.control}")

    def add_pid_values(self, runid, measured_height):
        self.results.add_item(runid,measured_height,self.target_height,self.threshold,self.upper_threshold,self.lower_threshold,
                              self.control,self.hover_foam,self.Kp,self.p_term,self.Ki,self.i_term,self.Kd,self.d_term)

    def calc_average_height(self):
        """
        function measures the height of the float three times and appends each measurement to a list
        The average is calculated and then returned
        :return: the calculated average height
        """
        heights_list = []
        for i in range(0, 3):
            height = self.distance_readings.get_distance()
            heights_list.append(height)
        average_height = sum(heights_list)/len(heights_list)
        return average_height

    def light_leds(self, measured_height, target_height):
        """
        Function lights the left LED when the measured height is within ±1 cm of the target height
        :param measured_height:
        :param target_height:
        :return:
        """
        if (target_height - 1) < measured_height < (target_height + 1):
            self.left_led.set_predefined_colour("green")
            self.left_led.turn_led_on()
        else:
            self.left_led.set_predefined_colour("red")
            self.left_led.turn_led_on()

    def log_values_to_oled_screen(self, measured_height, elapsed_time):
        """
        Function takes in the measured height and the elapsed time and displays it on the OLED screen
        The display updates after each iteration of the control loop
        :param measured_height:
        :param elapsed_time:
        :return:
        """
        self.oled_display.clear_screen()
        self.oled_display.display_text(f"AH : {measured_height:.2f} ({self.target_height})",0,0,1)
        self.oled_display.display_text(f"Fan: {self.control}",0, 12,1)
        self.oled_display.display_text(f"ET : {int(elapsed_time)}",0,24,1)

    def get_hover_foam_value(self):
        """
        Function sets the idle fan speed of the float that was selected in the webpage
        This is used when calculating the proportional term
        :return: the idle fan speed for the selected float
        """
        stalling_speed = {
               "hover_foam_1":{
                     5: 48000,
                    10: 46000,
                    15: 45000,
                    18: 44000,  # for heights greater than 18
                },
               "hover_foam_2":{
                     5: 48500,
                    10: 48000,
                    15: 47000,
                    18: 46000,  # for heights greater than 18
                },
               "hover_foam_3":{
                     5: 59500,
                    10: 59000,
                    15: 58000,
                    18: 57000,  # for heights greater than 18
                }
        }

        idle_fan_speed = 0
        # This checks what target height is being used and sets the idle fan speed to the correct stalling speed
        if self.target_height <= 12:
             idle_fan_speed = stalling_speed[self.hover_foam][10]
        elif 10 < self.target_height <= 17:
             idle_fan_speed = stalling_speed[self.hover_foam][15]
        elif self.target_height > 17:
             idle_fan_speed = stalling_speed[self.hover_foam][18]

        return idle_fan_speed


class Schmitttrigger(Algorithms):
    """
    This class contains the schmitt trigger algorithm to hover the foam at a certain height
    """
    def __init__(self, target_height, lower_threshold, upper_threshold, hover_foam=0,):
        super().__init__(hover_foam,target_height)
        """
        :param target_height: This is given by the user through the webpage
        :param lower_threshold: This is calculated using the target height and the threshold given by the user
        :param upper_threshold: This is calculated using the target height and the threshold given by the user
        """
        self.target_height = target_height
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold
        self.fan = PwmFan()
        self.distance_readings = DistanceSensor()
        self.RIGHT_LED = NeopixelLeds(brightness=0.8,phyiscal_led="RIGHT_LED")
        self.LEFT_LED = NeopixelLeds(brightness=0.8, phyiscal_led="LEFT_LED")
        self.results = StoreReadings()
        self.fan.turn_fan_off()
        time.sleep(2)

    def check_foam_stable(self, previous_height):
        """
        This checks if the previous average height is less than the current average height
        hence confirming if the float is still moving
        :param previous_height:
        :return:
        """
        current_av_height = 0
        for j in range(0, 3):
            current_av_height = self.calc_average_height()
            print(f"Current height: {current_av_height:.2f}, Previous height: {previous_height:.2f}", end=" ")
            if current_av_height > previous_height:
                print("Keep fan speed the same", end=" ")
            previous_height = current_av_height
        distance = current_av_height
        return distance

    def schmitt_trigger_alg(self, target_height, upper_threshold, lower_threshold, threshold, runid, hover_foam, duration):
        """
        This will lift the foam to the target height. It will use the LEDs to indicate whether the float is within the thresholds
        :param target_height: int that set by the user
        :param upper_threshold: int calculated using the threshold and the target height
        :param lower_threshold: int calculated using the threshold and the target height
        :param threshold: int that is set by the user, and it's used to calculate the upper and lower thresholds
        :param runid:
        :param hover_foam:
        :param duration: int that is set by the user and sets the amount of time the algorithm runs for
        :return:
        """
        previous_height = 0
        self.fan.turn_fan_on()
        self.fan.set_fan_speed(60)
        start_time = time.time()
        print(start_time)
        elapsed_time = 0
        while elapsed_time < duration:
            distance = self.check_foam_stable(previous_height)
            previous_height = distance
            self.results.add_item(runid, distance, target_height, threshold, upper_threshold, lower_threshold,
                                  self.fan.get_fan_speed(), hover_foam, kp=0, ki=0, kd=0, p_term=0,d_term=0,i_term=0)
            print(f"Elapsed Time: ({int(elapsed_time)}), Distance: {distance:.2f}")
            if distance > float(upper_threshold) and distance > float(lower_threshold):
                # Turn LED1 on and increase fan speed and add height value to table
                self.LEFT_LED.turn_led_off()
                self.RIGHT_LED.set_predefined_colour("red")
                self.RIGHT_LED.turn_led_on()
                self.fan.increment_fan_speed(2)
                print("Float is below upper threshold")
            elif distance < float(lower_threshold) and distance < float(upper_threshold):
                # Turn LED1 on and decrease fan speed and add height value to table
                self.LEFT_LED.turn_led_off()
                self.RIGHT_LED.set_predefined_colour("red")
                self.RIGHT_LED.turn_led_on()
                self.fan.decrement_fan_speed(1)
                print("Float is above lower threshold")
            elif float(upper_threshold) > distance > float(lower_threshold) or distance == float(target_height):
                # Turn LED2 On and Add height value to table
                self.RIGHT_LED.turn_led_off()
                self.LEFT_LED.set_predefined_colour("green")
                self.LEFT_LED.turn_led_on()

            else:
                self.fan.turn_fan_off()

            # time.sleep(0.5)
            elapsed_time = time.time() - start_time


class ProportionalAlgorithm(Algorithms):
    """
    This will include the function to run the proportional term of the PID algorithm
    """
    def __init__(self, hover_foam, target_height, Kp):
        super().__init__(hover_foam, target_height)
        self.hover_foam = hover_foam
        self.target_height = target_height
        self.Kp = Kp
        self.error = 0

    def calculate_proportional_term(self, measured_height):
        """
        This function will take in the measured height and the target height to calculate a value for
        the proportional term
        :param measured_height: this is a reading from the distance sensor.
        :return: proportional_term
        """
        self.error = measured_height - self.target_height
        proportional_term = int(self.Kp * self.error)
        if proportional_term < self.get_hover_foam_value():   # This checks the proportional term is not smaller than the idle fan speed of the float
            proportional_term = self.get_hover_foam_value()   # The proportional term is set to the idle fan speed so the float doesn't fall to the bottom
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
        self.left_led.turn_led_off()
        while elapsed_time < duration:
            measured_height = self.calc_average_height()
            # print(measured_height)
            self.p_term = self.calculate_proportional_term(measured_height)
            self.control = self.p_term                                      # Sets the fan speed to the p term
            self.log_values_to_screen(measured_height)                      # Gets the measured height to print to the terminal window
            self.log_values_to_oled_screen(measured_height, elapsed_time)   # Gets the measured height and elapsed to print to the OLED screen
            self.light_leds(measured_height, self.target_height)
            self.add_pid_values(runid, measured_height)                     # Gets the measured height and runid and adds it to the database
            if measured_height == self.target_height:
                print("Fan speed constant")
            else:
                self.fan.set_raw_fan_speed(self.control)
            elapsed_time = time.time() - start_time

    def get_config(self):
        print(f"Float: {self.hover_foam}, Target Height: {self.target_height}, Kp: {self.Kp}")

class ProportionalIntegralAlgorithm(ProportionalAlgorithm):
    """
    This will include the function to run the Proportional and Integral terms in the PID algorithm
    """
    def __init__(self, hover_foam, target_height, Kp, Ki):
        super().__init__(hover_foam, target_height, Kp)
        self.hover_foam = hover_foam
        self.target_height = target_height
        self.Kp = Kp
        self.Ki = Ki
        self.integral_error = 0

    def calculate_integral_term(self, measured_height):
        """
        This function will take in the measured height and the target height to calculate a value for
        the integral term
        :param measured_height: int
        :return: integral_term
        """
        # # self.error = self.calc_average_height() - self.target_height
        self.error = measured_height - self.target_height
        self.integral_error = self.integral_error + self.error
        integral_term = self.integral_error * self.Ki
        return integral_term

    def run_proportional_integral_algorithm(self, runid, duration):
        """
        This will run in a while loop for a set amount of time determined by the user.
        Adds the proportional and integral terms to determine and fan speed to lift the object to the target height.
        :param runid:
        :param duration:
        :return:
        """
        start_time = time.time()
        print(start_time)
        elapsed_time = 0
        self.left_led.turn_led_off()
        while elapsed_time < duration:
            measured_height = self.calc_average_height()
            self.p_term = self.calculate_proportional_term(measured_height)
            self.i_term = self.calculate_integral_term(measured_height)
            self.control = int(self.p_term + self.i_term)                   # Sets the fan speed
            self.log_values_to_screen(measured_height)
            self.log_values_to_oled_screen(measured_height, elapsed_time)
            self.light_leds(measured_height, self.target_height)
            self.add_pid_values(runid, measured_height)
            if measured_height == self.target_height:
                print("Fan speed constant")
            else:
                self.fan.set_raw_fan_speed(self.control)
            elapsed_time = time.time() - start_time

    def get_config(self):
        print(f"Float: {self.hover_foam}, Target Height: {self.target_height}, Kp: {self.Kp}, Ki: {self.Ki}")

class PIDAlgorithm(ProportionalIntegralAlgorithm):
    """
    This will include the function to run the full PID algorithm using proportional, integral and derivative terms
    """
    def __init__(self, hover_foam, target_height, Kp, Ki, Kd):
        super().__init__(hover_foam, target_height, Kp, Ki)
        self.hover_foam = hover_foam
        self.target_height = target_height
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.dt = 1
        self.prev_error = 0

    def calculate_derivative_term(self):
        """
        This function will take in the measured height and the target height to calculate a value for
        the derivative term
        :return:
        """
        derivative = self.error - self.prev_error
        derivative_term = derivative * self.Kd * self.dt
        return derivative_term

    def run_pid_algorithm(self, runid, duration):
        """
        This will run in a while loop for a set amount of time determined by the user.
        Adds the proportional, integral and derivative terms to determine and fan speed to lift the object to the target height.
        :param runid:
        :param duration:
        :return:
        """
        start_time = time.time()
        print(start_time)
        elapsed_time = 0
        self.left_led.turn_led_off()
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

    def get_config(self):
        print(f"Float: {self.hover_foam}, Target Height: {self.target_height}, Kp: {self.Kp}, Ki: {self.Ki}, Kd: {self.Kd}")

