# This file will run on the Raspberry Pi to test all the hardware is working
from OLED_Display import Oled
from Temperature_Humidity import TempHumidity
from Neopixel_LEDs import Neopixel, NeopixelLeds
from LDR import Ldr
from Distance_Sensor import DistanceSensor
from PWM_Fan import PwmFan
import time
import RPi.GPIO as GPIO

class PostTest:
    def __init__(self):

        self.screen = Oled()
    # Testing Hardware
    # Test Temperature
    def test_temperature_sensor(self):
        """
        Prints out the title of the test on the screen and then prints out a three values one at a time
        :return:
        """
        temp_humidity = TempHumidity()
        self.screen.clear_screen()
        temp_test = "Temp Test"
        self.screen.display_text(temp_test, 0, 0, 2)
        temp_readings = ""
        for i in range(0, 3):
            # This for loop gets the temperature reading and concatenates it to an empty string and displays the value to the screen. Does this 3 times
            temp_humidity.read_sensors()
            readings = str(temp_humidity.temperature)
            temp_readings = temp_readings + readings + "  "
            self.screen.display_text(temp_readings, 0, 24)
            time.sleep(1)

    # Test Humidity
    def test_humidity_sensor(self):
        """
        Same function as for temperature
        :return:
        """
        temp_humidity = TempHumidity()
        self.screen.clear_screen()
        humidity_label = "Humidity"
        self.screen.display_text(humidity_label, 0, 0, 2)
        humidity_readings = ""
        for i in range(0, 3):
            temp_humidity.read_sensors()
            humid_readings = str(temp_humidity.humidity)
            humidity_readings = humidity_readings + humid_readings + "  "
            self.screen.display_text(humidity_readings, 0, 24, 1)
            time.sleep(1)

    # Test LED 1 and LED 2
    def led_test(self, physical_led):
        if physical_led == "RIGHT_LED":
            led = NeopixelLeds(brightness=0.8, phyiscal_led="LED1")
            led_label = "Right LED"
        elif physical_led == "LEFT_LED":
            led = NeopixelLeds(brightness=0.8, phyiscal_led="LED2")
            led_label = "Left LED"
        self.screen.clear_screen()

        self.screen.display_text(led_label, 0, 0, 2)
        time.sleep(1)
        self.screen.clear_screen()
        led_1_label = f"On"
        self.screen.display_text(led_label, 0, 0, 1)
        self.screen.display_text(led_1_label, 15,15, 2)
        led.set_predefined_colour("pink")
        led.change_colour()
        led.turn_led_on()
        time.sleep(1)

        self.screen.clear_screen()
        led_1_label = f"Off"
        self.screen.display_text(led_label, 0, 0, 2)
        self.screen.display_text(led_1_label, 15,15, 2)
        time.sleep(1)
        led.turn_led_off()
        time.sleep(1)

        self.screen.clear_screen()
        led_1_label = f"Green"
        self.screen.display_text(led_label, 0, 0, 2)
        self.screen.display_text(led_1_label, 15,15, 2)
        time.sleep(1)
        led.set_predefined_colour("green")
        led.turn_led_on()
        time.sleep(1)

        self.screen.clear_screen()
        led_1_label = f"Blue"
        self.screen.display_text(led_label, 0, 0, 2)
        self.screen.display_text(led_1_label, 15,15, 2)
        time.sleep(1)
        led.set_predefined_colour("blue")
        led.turn_led_on()
        time.sleep(1)

        self.screen.clear_screen()
        led_1_label = f"Red"
        self.screen.display_text(led_label, 0, 0, 2)
        self.screen.display_text(led_1_label, 15,15, 2)
        time.sleep(1)
        led.set_predefined_colour("red")
        led.turn_led_on()
        time.sleep(1)

        # led_2.turn_led_off()
        self.screen.clear_screen()
        led_1_label = f"Purple"
        self.screen.display_text(led_label, 0, 0, 2)
        self.screen.display_text(led_1_label, 15,15, 2)
        time.sleep(1)
        led.set_colour(0, 153, 204)
        led.change_colour()
        led.turn_led_on()
        time.sleep(1)

        led.turn_led_off()
        self.screen.clear_screen()
    # Test LDR
    def test_ldr_sensor(self):
        """
        Same function as for temperature
        :return:
        """
        ldr = Ldr()
        self.screen.clear_screen()
        ldr_label = "LDR Test"
        self.screen.display_text(ldr_label, 0, 0, 2)
        ldr_readings = ""
        for i in range(0, 3):
            readings = str(ldr.get_light_level())
            ldr_readings = ldr_readings + readings + "  "
            self.screen.display_text(ldr_readings, 0, 24, 1)
            time.sleep(1)

    # Test Distance sensor
    def test_distance(self):
        distance = DistanceSensor()
        self.screen.clear_screen()
        distance_label = "Distance"
        self.screen.display_text(distance_label, 0, 0, 2)
        distance_readings = ""
        for i in range(0, 3):
            dist_readings = str(distance.get_distance())
            distance_readings = distance_readings + dist_readings + "  "
            self.screen.display_text(distance_readings, 0, 24, 1)
            time.sleep(1)

    # Test Fan
    def test_fan(self):
        fan = PwmFan()
        self.screen.clear_screen()
        self.screen.display_text("Fan Test", 0, 0, 2)
        time.sleep(1)

        self.screen.display_test("Fan Test", "Speed: 100")
        fan.turn_fan_on()
        time.sleep(3)

        self.screen.display_test("Fan Test", "Speed: 10")
        fan.set_fan_speed(10)
        time.sleep(3)

        self.screen.display_test("Fan Test", "Speed: 0")
        fan.turn_fan_off()
        time.sleep(3)

        self.screen.display_test("Fan Test", "Incr: 50")
        fan.increment_fan_speed(50)
        time.sleep(3)

        self.screen.clear_screen()
        fan.turn_fan_off()

    def start_finish_post(self, message):
        self.screen.display_text("POST",0, 0, 2)
        self.screen.display_text(message, 0, 16, 2)


test = PostTest()
test.start_finish_post("Starting")
test.test_temperature_sensor()
test.test_humidity_sensor()
test.led_test("LEFT_LED")
test.led_test("RIGHT_LED")
test.test_ldr_sensor()
test.test_distance()
test.test_fan()
test.start_finish_post("Finished")




# test_temperature_sensor()
# time.sleep(2)
# test_humidity_sensor()
# time.sleep(1)
# test_ldr_sensor()
# led_test("LED1")
# led_test("LED2")
# test_distance()
# test_fan()
