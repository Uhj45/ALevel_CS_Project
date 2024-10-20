# from Temperature_Humidity import TempHumidity
from OLED_Display import Oled
from Neopixel_LEDs import Neopixel, Neopixel2
# from LDR import Ldr
from Distance_Sensor import DistanceSensor
from PWM_Fan import PCA9685Fan
import time
import RPi.GPIO as GPIO

# Objects from the TempHumidity class
# readings = TempHumidity()  # Using the class TempHumidity, this creates the object for that class
# for i in range(0, 5):
#     readings.read_sensors()  # Calls method in the class
#     print(f"Temperature: {readings.temperature} °C", f"Humidity: {readings.humidity} %")
#     time.sleep(1)

# Objects from the Oled class
# display = Oled()   # This creates an object in the class to display simple text to the screen
# text = "This is my text"
# display.display_text(text)
# time.sleep(2)
# display.clear_screen()
# text = "hello"
# display.display_text(text)
#
# display2 = Oled(x=20, y=20)   # This creates an object with two parameters that determine the position of the text
# text2 = "Hello World"
# display2.display_text(text2)
#
# display3 = Oled(size=2, x=10, y=10)  # This creates an object with another parameter that will change the size of the text
# display3.display_text(text2)
# display4 = Oled(2, 10, 10)  # This uses positional arguments instead of keyword arguments
# display4.display_text(text2)
#
# # Objects for the LED class


# led = Neopixel(brightness=0.8)
# led.set_colour(255, 0, 0)
# led.set_predefined_colour("blue")
# led.turn_led_on()
# time.sleep(2)
# led2 = Neopixel()
# led2.turn_led_off()
# time.sleep(2)
led3 = Neopixel2(1.0)
led3.set_predefined_colour("mint")
led3.change_colour()
led3.turn_led_on()
# time.sleep(2)
# led4 = Neopixel(1.0)
# led4.set_predefined_colour("brown")
# led4.flash_led(3)
# time.sleep(2)
# led5 = Neopixel(1.0, 6, 7, 8)
# led5.pulse_led(3)
# led6 = Neopixel2(brightness=1.0, phyiscal_led="LED2")
# led6.set_colour(0, 0, 255)
# led6.turn_led_on()
# time.sleep(4)
# led6.turn_led_off()
#
# led6 = Neopixel2(brightness=1.0)
# led6.set_colour(255, 0, 0)
# led6.turn_led_on()
# time.sleep(4)
# led6.turn_led_off()

# # Object for the LDR class
# ldr_sensor = Ldr()
# ldr_sensor.get_light_level()
#
# for i in range(0, 3):
#     print(f"LDR value: {ldr_sensor.lightlevel}")
#     time.sleep(1)
#
# # Object for the distance sensor class
# distance_readings = DistanceSensor()
#
# for i in range(0, 100):
#     dist = distance_readings.get_distance()
#     print(f"Distance: {i}, {dist:.1f} cm ")
#     time.sleep(3)
#
# GPIO.cleanup()

# pca_fan = PCA9685Fan()
# pca_fan.turn_fan_on()
# time.sleep(5)
# pca_fan.turn_fan_off()
# time.sleep(5)
# pca_fan.set_fan_speed(30)

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

# distance_readings = DistanceSensor()
# fan = PCA9685Fan()
#
# for i in range(0, 20):
#     fan.increment_fan_speed(5)
#     print(distance_readings.get_distance())
#     time.sleep(3)

# distance_readings = DistanceSensor()
# fan.turn_fan_off()
# for i in range(0, 100):
#     dist = distance_readings.get_distance()
#     print(f"Distance: {i}, {dist:.1f} cm ")
#     time.sleep(3)
