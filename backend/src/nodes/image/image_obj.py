from numpy import unravel_index, bincount, zeros, uint8, mean, array
from cv2 import imread, resize, cvtColor, COLOR_BGR2HSV_FULL
from numexpr import evaluate

class Image:
    def __init__(self, path=None, image=None) -> None:
        self.path = path
        self.image = imread(path) if path else image
        assert self.image is not None
        
    def resize(self, width, height):
        self.image = resize(self.image, (width, height))

    def __call__(self):
        return self.image

    def path(self):
        return self.path

    def height(self):
        return self.image.shape[0]

    def width(self):
        return self.image.shape[1]

    def channels(self):
        return self.image.sheape[2] if len(self.image.shape) == 3 else 1

    def pixel(self, x, y):
        return self.image[y, x]

    def area(self):
        return self.width() * self.height()

    def pixel_area(self, x, y, w, h):
        return self.image[y : y + h, x : x + w]

    def pixel_area_mean(self, x, y, w, h):
        return mean(self.image[y : y + h, x : x + w])

    def dominant_color(self):
        a2D = self.image.reshape(-1, self.image.shape[-1])
        col_range = (256, 256, 256)  # generically : a2D.max(0)+1
        eval_params = {
            "a0": a2D[:, 0],
            "a1": a2D[:, 1],
            "a2": a2D[:, 2],
            "s0": col_range[0],
            "s1": col_range[1],
        }
        a1D = evaluate("a0*s0*s1+a1*s0+a2", eval_params)
        return unravel_index(bincount(a1D).argmax(), col_range)

    def dominant_color_array(self):
        rgb_base = self.dominant_color()
        rgb_base_img = zeros([200, 200, 3], uint8)
        for c in range(0, 3):
            rgb_base_img[:, :, c] = zeros([200, 200]) + rgb_base[c]

        hsv_bkg = cvtColor(rgb_base_img, COLOR_BGR2HSV_FULL)
        return mean(array(hsv_bkg), axis=(1, 0)).tolist()

    def dominant_color_range(self, variance=0.3):
        color_array = self.dominant_color_array()
        hsv_bkg_median_max = list(map(lambda x: x + (x * variance), color_array))
        hsv_bkg_median_min = list(map(lambda x: x - (x * variance), color_array))

        return hsv_bkg_median_min, hsv_bkg_median_max
