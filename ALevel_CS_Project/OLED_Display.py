import busio
import board
import time
import adafruit_ssd1306


class Oled:
    """
    Uhjas
    """
    def __init__(self, size=1, x=0, y=0):
        """
        These parameters are localised to the class and can only be used inside the class
        :param x:
        :param y:
        :param size:
        """
        self.x = x
        self.y = y
        self.size = size
        DISPLAY_WIDTH = 128
        DISPLAY_HEIGHT = 32
        i2c = busio.I2C(board.SCL, board.SDA)
        self.oled = adafruit_ssd1306.SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, i2c, addr=0x3c)  # oled has been changed to an instance variable so it can be used throughout the class
        self.oled.poweron()
        self.oled.contrast(50)

    def display_text(self, text_to_display):
        print(f"displaying text, {text_to_display}")
        self.oled.text(text_to_display, self.x, self.y, "white", font_name="font5x8.bin", size=self.size)
        self.oled.show()



