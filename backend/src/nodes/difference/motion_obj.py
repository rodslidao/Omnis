from cv2.bgsegm import createBackgroundSubtractorMOG
from api import logger, exception


class MotionSensor:
    @exception(logger)
    def __init__(self, learningRate=-1) -> None:
        self.background_subtractor = createBackgroundSubtractorMOG()
        self.lr = learningRate

    @exception(logger)
    def get_motion_mask(self, frame):
        return self.background_subtractor.apply(frame, learningRate=self.lr)
