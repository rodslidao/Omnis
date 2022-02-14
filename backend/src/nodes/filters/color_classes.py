import math
import colorsys


class Cor:
    """
    A class to convert color to hex, rgb, hsv and cv2_hsv formats.
    """

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
            case "hex":
                self.hex = value
                self.rgb = self.hex2int(value)
                self.hsv = self.rgb2hsv(*self.rgb)
                self.cv2_hsv = [
                    self.hsv[0],
                    (self.hsv[1] * 255) / 100,
                    (self.hsv[2] * 255) / 100,
                ]
            case "rgb":
                self.rgb = value
                self.hex = self.any2hex(value)
                self.hsv = self.rgb2hsv(*self.rgb)
                self.cv2_hsv = [
                    self.hsv[0],
                    (self.hsv[1] * 255) / 100,
                    (self.hsv[2] * 255) / 100,
                ]
            case "hsv":
                self.hsv = value
                self.rgb = self.hsv2rgb(*self.hsv)
                self.hex = self.any2hex(self.rgb)
                self.cv2_hsv = [
                    self.hsv[0],
                    (self.hsv[1] * 255) / 100,
                    (self.hsv[2] * 255) / 100,
                ]
            case "cv2_hsv":
                self.cv2_hsv = value
                self.hsv = [
                    self.cv2_hsv[0],
                    (self.cv2_hsv[1] * 100) / 255,
                    (self.cv2_hsv[2] * 100) / 255,
                ]
                self.rgb = self.hsv2rgb(*self.hsv)
                self.hex = self.any2hex(self.rgb)

    def get_color(self, mode):
        return getattr(self, mode)

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
        print("hsv:", color_hsv)
        return color_hsv

    def any2hex(self, hsv_):
        return tuple(map(hex, hsv_))

    def hex2int(self, hex_):
        return tuple(map(lambda x: int(x, 16), hex_))


class ColorRange:
    """
    A class to convert 2 color ranges to another color range format.\n
    \n
    :name: name of the color range\n
    :mode: color mode   -> i.eg. 'rgb' or 'hex'\n
    :lower: lower color value -> i.eg. (0, 0, 0) or #000000\n
    :upper: upper color value -> i.eg. (255, 255, 255) or #ffffff\n
    \n
    :methods: ->\n
        get_color(mode) returns the color in the specified mode.\n
        \n
        get_full() returns all converted color ranges.\n
    """

    def __init__(self, name, mode, lower, upper):
        self.name = name
        self.lower = Cor(lower, mode)
        self.upper = Cor(upper, mode)
        self.mode = mode

    def get(self, mode):
        """
        return a dict with all the color ranges
        """
        return {
            "lower": self.lower.getColor(mode),
            "upper": self.upper.getColor(mode),
        }

    def get_full(self):
        """
        return a dict with all the color ranges
        """
        return {
            self.name: {
                "hex": self.get("hex"),
                "rgb": self.get("rgb"),
                "hsv": self.get("hsv"),
            }
        }
