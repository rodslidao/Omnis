import colorsys
from numpy import array, rint


def hsv2rgb(h, s_, v_):
    return (
        rint(array(colorsys.hsv_to_rgb(*array([h, s_, v_]) / [360, 100, 100])) * 255)
        .astype(int)
        .tolist()
    )


def rgb2hsv(r, g, b):
    return rint(array(colorsys.rgb_to_hsv(*array([r, g, b]) / 255)) * [360, 100, 100])


def any2hex(hsv_):
    return tuple(map(hex, hsv_))


def hex2int(hex_):
    return tuple(map(lambda x: int(x, 16), hex_))


def hsv2cv2_hsv(hsv):
    return rint((array(hsv) * 255) / [360, 100, 100])
