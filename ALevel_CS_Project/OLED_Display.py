import busio
import board
import time
import adafruit_ssd1306

class Oled:
    def __init__(self, text=None):
        self.text = text

    def write_to_display(self):
        self.text = input("Enter a message to display to the screen: ")
        return self.text


user_input = Oled()
user_input.write_to_display()

i2c = busio.I2C(board.SCL, board.SDA)
width = 128
height = 32
display = adafruit_ssd1306.SSD1306_I2C(width, height, i2c, addr=0x3c)
display.poweron()
display.contrast(50)

for _ in range(0, 1):
    display.fill(0)
    display.text(user_input.text(), 1, 1, "white", font_name="font5x8.bin", size=1)
    display.show()
    time.sleep(1)
    display.fill(0)
    display.show()
