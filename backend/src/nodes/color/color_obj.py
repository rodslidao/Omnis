import math
import colorsys
from api import logger, exception, for_all_methods

@for_all_methods(exception(logger))
class ColorOBJ:
    """
    A class to convert color to hex, rgb, hsv and cv2_hsv formats.
    """
    HEX = "HEX"
    RGB = "RGB"
    HSV = "HSV"
    CV2_HSV = "CV2_HSV"

    def __init__(self, value, mode):
        """
        :value: color value -> i.eg. (255, 255, 255) or #ffffff\n
        :mode: color mode   -> i.eg. 'rgb' or 'hex'\n
        \n
        :methods: ->\n
            get_color(mode) returns the color in the specified mode.\n
            \n
            -- when a instance is created, the color is automatically converted to all other modes, the following methods does need be called --\n
            \n
            rgb2hsv(r, g, b) returns the hsv value of the rgb value.\n
            any2hex(hsv_) returns the hex value of the hsv value.\n
            hex2int(hex_) returns the int value of the hex value.\n

        """
        match mode:
            case self.HEX:
                self.HEX_V = value
                self.RGB_V = self.hex2int(value)
                self.HSV_V = self.rgb2hsv(*self.rgb)
                self.CV2_HSV_V = [
                    self.hsv[0],
                    (self.hsv[1] * 255) / 100,
                    (self.hsv[2] * 255) / 100,
                ]
            case self.RGB:
                self.RGB_V = value
                self.HEX_V = self.any2hex(value)
                self.HSV_V = self.rgb2hsv(*self.rgb)
                self.CV2_HSV_V = [
                    self.hsv[0],
                    (self.hsv[1] * 255) / 100,
                    (self.hsv[2] * 255) / 100,
                ]
            case self.HSV:
                self.HSV_V = value
                self.RGB_V = self.hsv2rgb(*self.hsv)
                self.HEX_V = self.any2hex(self.rgb)
                self.CV2_HSV_V = [
                    self.hsv[0],
                    (self.hsv[1] * 255) / 100,
                    (self.hsv[2] * 255) / 100,
                ]
            case self.CV2_HSV:
                self.CV2_HSV_V = value
                self.HSV_V = [
                    self.cv2_hsv[0],
                    (self.cv2_hsv[1] * 100) / 255,
                    (self.cv2_hsv[2] * 100) / 255,
                ]
                self.RGB_V = self.hsv2rgb(*self.hsv)
                self.HEX_V = self.any2hex(self.rgb)

    def get(self, mode):
        return getattr(self, f"{mode}_V")

    def hsv2rgb(self, h, s_, v_):
        s = s_ / 100
        v = v_ / 100
        c = v * s
        x = c * (1 - abs(math.fmod(h / 60.0, 2) - 1))
        m = v - c
        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))

    def rgb2hsv(self, r, g, b):
        red_percentage = r / 255
        green_percentage = g / 255
        blue_percentage = b / 255
        color_hsv_percentage = colorsys.rgb_to_hsv(
            red_percentage, green_percentage, blue_percentage
        )

        color_h = round(360 * color_hsv_percentage[0])
        color_s = round(100 * color_hsv_percentage[1])
        color_v = round(100 * color_hsv_percentage[2])
        
        color_hsv = (color_h, color_s, color_v)
        return color_hsv

    def any2hex(self, hsv_):
        return tuple(map(hex, hsv_))

    def hex2int(self, hex_):
        return tuple(map(lambda x: int(x, 16), hex_))
