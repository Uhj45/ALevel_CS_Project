import busio
import board
import time
import adafruit_ssd1306


class Oled:
    """
    The class writes text to the OLED display at specified coordinates. The text can be set to either one of two sizes
    The text can be written to any x,y coordinate where 0 < x < 128 and 0 < y < 32
    """
    def __init__(self, x=0, y=0, size=1):
        """
        These parameters are localised to the class and can only be used inside the class
        :param x: int of the x coordinate, where 0 < x < 128
        :param y: int of the y coordinate, where 0 < y < 32
        :param size: int where size is either 1 or 2
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

    def display_text(self, text_to_display, x=0, y=0, size=1):
        """
        Function to display text
        :param text_to_display: string to display
        :param x: int of the x coordinate, where 0 < x < 128
        :param y: int of the y coordinate, where 0 < y < 32
        :param size: int where size is either 1 or 2
        :return: None
        """
        self.x = x
        self.y = y
        self.size = size
        self.oled.text(text_to_display, self.x, self.y, "white", font_name="font5x8.bin", size=self.size)
        self.oled.show()

    def clear_screen(self):
        """
        Clears the OLED display of any text
        :return:
        """
        self.oled.fill(0)
        self.oled.show()
        time.sleep(1)

    def display_test(self,device, test_name):
        """
        Function used by POST test
        :param device: string
        :param test_name: string
        :return: None
        """
        self.clear_screen()
        self.display_text(f"{device}", x=0, y=0, size=2)
        self.display_text(f"{test_name}", x=0, y=16, size=2)
        time.sleep(1)