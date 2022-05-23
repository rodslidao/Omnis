from api import logger, exception
from api.decorators import for_all_methods
from src.nodes.color.color_functions import hex2int, any2hex, rgb2hsv, hsv2rgb, hsv2cv2_hsv


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
            -- when a instance is created, the color is automatically converted to all
            other modes, the following methods does need be called --\n
            \n
            rgb2hsv(r, g, b) returns the hsv value of the rgb value.\n
            any2hex(hsv_) returns the hex value of the hsv value.\n
            hex2int(hex_) returns the int value of the hex value.\n

        """
        match mode:
            case self.HEX:
                self.HEX_V = value
                self.RGB_V = hex2int(value)
                self.HSV_V = rgb2hsv(*self.RGB_V)
                self.CV2_HSV_V = hsv2cv2_hsv(self.HSV_V)
            case self.RGB:
                self.RGB_V = value
                self.HEX_V = any2hex(value)
                self.HSV_V = rgb2hsv(*self.RGB_V)
                self.CV2_HSV_V = hsv2cv2_hsv(self.HSV_V)
            case self.HSV:
                self.HSV_V = value
                self.RGB_V = hsv2rgb(*self.HSV_V)
                self.HEX_V = any2hex(self.RGB_V)
                self.CV2_HSV_V = hsv2cv2_hsv(self.HSV_V)
            case self.CV2_HSV:
                self.CV2_HSV_V = value
                self.HSV_V = [
                    self.CV2_HSV_V[0],
                    (self.CV2_HSV_V[1] * 100) / 255,
                    (self.CV2_HSV_V[2] * 100) / 255,
                ]
                self.RGB_V = hsv2rgb(*self.HSV_V)
                self.HEX_V = any2hex(self.RGB_V)

    def get(self, mode):
        return getattr(self, f"{mode}_V")
