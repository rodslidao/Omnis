from pickle import TRUE
from cv2 import  MORPH_OPEN, THRESH_BINARY, THRESH_BINARY_INV,bgsegm, GaussianBlur, VideoCapture, absdiff, convertScaleAbs, accumulateWeighted, cvtColor, destroyAllWindows, dilate, equalizeHist, imshow, morphologyEx, COLOR_BGR2GRAY, threshold, waitKey

bkg_remover = bgsegm.createBackgroundSubtractorMOG()
def _delta(A, B, scale=True):
    if scale:
        return absdiff(A, convertScaleAbs(B))
    return absdiff(A, B)

def _accumulate(src, dst, alpha=0.1):
    if dst is None:
        return src.copy().astype("float")
    return accumulateWeighted(src, dst, alpha)

def _morph_ellipse_mask(mask, thresh=10, maxval=255, **kwargs):
    thresh = threshold(mask, 50, 255, THRESH_BINARY)[1]
    return dilate(thresh, None, iterations=5)

def diff(src, avg=None, avarage=True):
    # try: 
    gray = cvtColor(src, COLOR_BGR2GRAY)
    equalized = equalizeHist(gray)
    blur_gray_src = GaussianBlur(equalized, (5, 5), 0)
    
    imshow("equalized", blur_gray_src)
    if (not avarage and avg is None) or avarage:
        avg = _accumulate(blur_gray_src, avg)
    n = bkg_remover.apply(blur_gray_src)
    imshow("n", n)
    # avg = _accumulate(blur_gray_src, avg)
    delta = _delta(blur_gray_src, avg)
    imshow("delta", delta)
    mask = _morph_ellipse_mask(delta)
    return avg, delta, mask


cam = VideoCapture(0)
a = cam.read()[1]
avg = None
avg2 = None
avg3 = None
for n in range(100):
    cam.read()[1]
while waitKey(1) != 27:
    
    b = cam.read()[1]
    avg, delta, mask = diff(b, avg, avarage=False)
    avg2, delta2, mask2 = diff(b, avg2)
    # avg3, delta3, mask3= diff(mask, avg3)
    try:
        imshow('c', mask)
        imshow('c2', mask2)
        # imshow('c3', mask3)
    except:
        pass
cam.release()
destroyAllWindows()