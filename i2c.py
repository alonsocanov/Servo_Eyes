# Import all board pins.
from PIL import Image, ImageDraw, ImageFont
from board import SCL, SDA
import busio
import subprocess
# Import the SSD1306 module
import adafruit_ssd1306
# Import the mpu6050 module
import adafruit_mpu6050

class I2C:
    def __init__(self):
        # Create the I2C interface.
        self.__i2c = busio.I2C(SCL, SDA)

    def set_display_height(self, height:int):
        self.__height = height

    def set_display_width(self, width:int):
        self.__width = width

    def set_display_padding(self, padding:int):
        self.__padding = padding

    def set_display(self, address=None):
        '''
        Create the SSD1306 OLED class.The first two parameters are the pixel width and pixel height.
        The MakerFocus I2C OLED Display is meant to be comptible with Adafruit CircuitPython API.
        '''
        if not address:
            self.__display = adafruit_ssd1306.SSD1306_I2C(128, 32, self.__i2c)
        else:
            self.__display = adafruit_ssd1306.SSD1306_I2C(128, 32, self.__i2c, addr=address)

        self.__width = 128
        self.__height = 32
        # setup Image for oled
        # create a single bit image of size (width, height)
        self.__image = Image.new('1', (self.__width, self.__height))
        # create a draw object to manipulate image
        self.__draw = ImageDraw.Draw(self.__image)
        # draw a black filled box to clear image
        self.__draw.rectangle((0, 0, self.__width, self.__height), outline=0, fill=0)
        # define padding
        self.__padding = -2
        # load default font
        self.__font = ImageFont.load_default()

    def draw_display(self, text:str, pos:tuple):
        x, y = pos
        size = 8
        if x > self.__width + size:
            x = self.__width + size
        elif x < self.__padding - size:
            x = self.__padding - size
        if y > self.__height + size:
            y = self.__height + size
        elif y < self.__padding - size:
            y = self.__padding - size

        # clear display portion
        self.__draw.rectangle((x, y, self.__width - x, y - size), outline=0, fill=0)
        # set text in display
        self.__draw.text((x, y), text, font=self.__font, fill=255)
        # set to the PIL image
        self.__display.image(self.__image)
        # display image
        self.__display.show()

    def clear_display(self):
        # clear display portion
        self.__draw.rectangle((0, 0, self.__width, self.__height), outline=0, fill=0)
        # set to the PIL image
        self.__display.image(self.__image)
        # display image
        self.__display.show()

    def set_imu(self):
        self.__mpu = adafruit_mpu6050.MPU6050(self.__i2c)

    def get_accleration(self):
        return self.__mpu.acceleration

    def get_gyro(self):
        return self.__mpu.gyro

    def get_temperature(self):
        return self.__mpu.temperature
