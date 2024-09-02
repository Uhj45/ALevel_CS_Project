# from Temperature_Humidity import TempHumidity
# from OLED_Display import Oled
from Neopixel_LEDs import Neopixel
# from LDR import Ldr
from Distance_Sensor import DistanceSensor
import time
import RPi.GPIO as GPIO

# Objects from the TempHumidity class
# readings = TempHumidity()  # Using the class TempHumidity, this creates the object for that class
# for i in range(0, 5):
#     readings.get_temperature_humidity()  # Calls method in the class
#     print(f"Temperature: {readings.temperature} °C", f"Humidity: {readings.humidity} %")
#     time.sleep(1)

# Objects from the Oled class
# display = Oled()   # This creates an object in the class to display simple text to the screen
# text = "This is my text"
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


# led = Neopixel(0.8)
# led.turn_led_on()
# time.sleep(2)
# led2 = Neopixel()
# led2.turn_led_off()
# time.sleep(2)
# led3 = Neopixel(1.0, 255, 205, 140)
# led3.change_colour()
# time.sleep(2)
led4 = Neopixel(1.0, 134, 145, 167)
led4.flash_led(4)
time.sleep(2)
led5 = Neopixel(1.0)
led5.pulse_led(3)

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
# for i in range(0,4):
#     dist = distance_readings.get_distance()
#     print(f"Distance: {dist:.1f} cm ")
#
# GPIO.cleanup()

