from Temperature_Humidity import TempHumidity
from OLED_Display import Oled
from Neopixel_LEDs import Neopixel
import time

# Objects from the TempHumidity class
readings = TempHumidity()  # Using the class TempHumidity, this creates the object for that class
readings.get_temperature_humidity()  # Calls method in the class
for i in range(0, 5):
    print(f"Temperature: {readings.temperature} °C", f"Humidity: {readings.humidity} %")
    time.sleep(1)

# Objects from the Oled class
display = Oled()   # This creates an object in the class to display simple text to the screen
text = "This is my text"
display.display_text(text)

display2 = Oled(x=20, y=20)   # This creates an object with two parameters that determine the position of the text
text2 = "Hello World"
display2.display_text(text2)

display3 = Oled(size=2, x=10, y=10)  # This creates an object with another parameter that will change the size of the text
display3.display_text(text2)
display4 = Oled(2, 10, 10)  # This uses positional arguments instead of keyword arguments
display4.display_text(text2)

#
# led = Neopixel(1.0, 255, 56, 79)
# led.change_colour()

led2 = Neopixel(0.8, 0, 100, 200)
led2.on_off()

