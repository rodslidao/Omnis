import math
import colorsys


def hsv2rgb(h, s_, v_):
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


def rgb2hsv(r, g, b):
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


def any2hex(hsv_):
    return tuple(map(hex, hsv_))


def hex2int(hex_):
    return tuple(map(lambda x: int(x, 16), hex_))
