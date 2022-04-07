from numpy import unravel_index, bincount, zeros, uint8, mean, array
from cv2 import imread, cvtColor, COLOR_BGR2HSV_FULL
from numexpr import evaluate
from api import logger, exception

#! Verify @exception(logger) performance.

class Image:
    @exception(logger)
    def __init__(self, path=None, image=None) -> None:
        self.path = path
        self.image = imread(path) if path else image
        self.color_code = "BGR"
        assert self.image is not None

    @exception(logger)
    def __call__(self):
        return self.image

    @exception(logger)
    def color_space(self):
        return self.color_code

    @exception(logger)
    def path(self):
        return self.path

    @exception(logger)
    def height(self):
        return self.image.shape[0]

    @exception(logger)
    def width(self):
        return self.image.shape[1]

    @exception(logger)
    def size(self):
        return self.image.shape[:-1]

    @exception(logger)
    def channels(self):
        return self.image.sheape[2] if len(self.image.shape) == 3 else 1

    @exception(logger)
    def area(self):
        return self.width() * self.height()

    @exception(logger)
    def dominant_color(self):
        a2D = self.image.reshape(-1, self.image.shape[-1])
        col_range = (256, 256, 256)
        eval_params = {
            "a0": a2D[:, 0],
            "a1": a2D[:, 1],
            "a2": a2D[:, 2],
            "s0": col_range[0],
            "s1": col_range[1],
        }
        a1D = evaluate("a0*s0*s1+a1*s0+a2", eval_params)
        return unravel_index(bincount(a1D).argmax(), col_range)

    @exception(logger)
    def dominant_color_array(self):
        rgb_base = self.dominant_color()
        rgb_base_img = zeros([200, 200, 3], uint8)
        for c in range(0, 3):
            rgb_base_img[:, :, c] = zeros([200, 200]) + rgb_base[c]

        hsv_bkg = cvtColor(rgb_base_img, COLOR_BGR2HSV_FULL)
        return mean(array(hsv_bkg), axis=(1, 0)).tolist()

    @exception(logger)
    def dominant_color_range(self, variance=0.3):
        color_array = self.dominant_color_array()
        hsv_bkg_median_max = array(list(map(lambda x: x + (x * variance), color_array)))
        hsv_bkg_median_min = array(list(map(lambda x: x - (x * variance), color_array)))

        return hsv_bkg_median_min, hsv_bkg_median_max
