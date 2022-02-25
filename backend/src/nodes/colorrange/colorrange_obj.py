from api import logger, exception

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

    @exception(logger)
    def __init__(self, name, mode, lower, upper):
        self.name = name
        self.lower = Cor(lower, mode)
        self.upper = Cor(upper, mode)
        self.mode = mode

    @exception(logger)
    def get(self, mode):
        """
        return a dict with all the color ranges
        """
        return {
            "lower": self.lower.getColor(mode),
            "upper": self.upper.getColor(mode),
        }

    @exception(logger)
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