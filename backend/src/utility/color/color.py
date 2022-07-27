class ColorPrint:
    R = "\033[91m"
    G = "\033[92m"
    B = "\033[94m"
    C = "\033[96m"
    Y = "\033[93m"

    WARNING = "\033[93m" + "[⚠ ]: " + "\033[0m"
    ERROR = "\033[91m" + "[⚠ ]:  " + "\033[0m"
    INFO = "\033[96m" + "[🛈 ]:  " + "\033[0m"
    SUCCESS = "\033[92m" + "[✓ ]:  " + "\033[0m"
    U = "\033[4m"
    B = "\033[1m"


def color(string, color):
    return str(getattr(ColorPrint, color) + str(string) + "\033[0m")
