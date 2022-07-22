from cv2 import absdiff, cvtColor, COLOR_BGR2GRAY, THRESH_BINARY_INV, THRESH_OTSU
from numpy import uint8, zeros_like, full
from skimage.metrics import structural_similarity as ssim
from api import logger, exception


@exception(logger)
def direct_diff(img1, img2, threshold):
    mask = absdiff(img1, img2)
    imask = mask > threshold
    canvas = zeros_like(img2, uint8)
    c2 = full(canvas.shape, 255, dtype=uint8)
    canvas[imask] = c2[imask]
    return canvas


@exception(logger)
def similarity_diff(img1, img2, threshold):
    img1 = cvtColor(img1, COLOR_BGR2GRAY)
    img2 = cvtColor(img2, COLOR_BGR2GRAY)

    (score, diff) = ssim(img2, img1, full=True)
    diff = (diff * 255).astype("uint8")
    thresh = threshold(diff, threshold, 255, THRESH_BINARY_INV | THRESH_OTSU)[1]
    return thresh
