from src.utility.image_processing.generate_data import generate_data
from src.utility.image_processing.generate_calib import charuco_calibration
from src.utility.image_processing.guess_aruco_type import ARUCO_DICT
from src.manager.camera_manager import CameraManager
from api.store import calibrations
from api.subscriptions import SubscriptionFactory
from api import dbo
from datetime import datetime as dt, timedelta
from cv2.aruco import Dictionary_get, DetectorParameters_create, detectMarkers


class Steps:
    def __init__(
        self,
        number_of_steps,
        step_description=None,
        step_title=None,
        estimated_time=None,
    ):
        self.status = {
            "step": 0,
            "total_steps": number_of_steps,
            "step_description": "",
            "step_title": "",
            "estimated_time": None,
        }

    def next(self, step_description, step_title, estimated_time=None):
        self.status["step"] += 1
        self.status["step_description"] = step_description
        self.status["step_title"] = step_title
        self.status["estimated_time"] = estimated_time
        return self.status

    def get_status(self):
        return self.status


# CalibrationManager = SubscriptionFactory(calibrations, 'calibrations')


class CameraCalibration:
    def __init__(
        self,
        camera_id="6244b07d3a8338aceae96cee",
        frame_interval=2000,
        data_set_size=20,
        min_blur=100,
        max_blur=6100,
        show=False,
        export_path="./data_0",
        squaresX=6,
        squaresY=9,
        squareLength=30,
        markerSize=23,
        dictionary_name="DICT_7X7_1000",
    ):
        # self.kwargs = kwargs
        self.camera_id = camera_id
        self.steps = Steps(2)

        self.frame_interval = frame_interval
        self.data_set_size = data_set_size
        self.max_blur = max_blur
        self.min_blur = min_blur
        self.show = show

        self.export_path = export_path
        self.squaresX = squaresX
        self.squaresY = squaresY
        self.squareLength = squareLength
        self.markerSize = markerSize
        self.dictionary_name = dictionary_name
        self.cam = CameraManager.get_by_id(self.camera_id)

    def calibrate(self):
        self.update("Searching", "for the calibration board")
        arucoDict = Dictionary_get(ARUCO_DICT[self.dictionary_name])
        arucoParams = DetectorParameters_create()
        board = False
        start = dt.utcnow()
        while (dt.utcnow() - start) < timedelta(seconds=15):
            image = self.cam.read()
            (corners, ids, rejected) = detectMarkers(
                image, arucoDict, parameters=arucoParams
            )
            # if at least one ArUco marker was detected display the ArUco
            # name to our terminal
            if len(corners) > 0:
                self.update(
                    "Taking pictures",
                    "for camera calibration",
                    int((self.frame_interval * self.data_set_size) / 1000),
                )
                board = True
                break

        if not board:
            self.update("Fail to find a valid board", "check the camera and try again")
            return False

        self.data = generate_data(
            "./",
            self.cam,
            self.frame_interval,
            self.data_set_size,
            self.max_blur,
            self.min_blur,
            self.show,
            True,
        )
        self.update("Calibrating", "Calibrating...")
        try:
            self.calibration = charuco_calibration(
                self.data,
                self.export_path,
                self.squaresX,
                self.squaresY,
                self.squareLength,
                self.markerSize,
                self.dictionary_name,
            )
            print(self.calibration)
            self.update("Calibrated", "Calibrated")
            self.calibration["_id"] = str(self.camera_id)
            dbo.update_one(
                "camera-calibrations",
                {"_id": self.calibration["_id"]},
                {"$set": self.calibration},
                {"upsert": True},
            )
            return True
        except UnboundLocalError:
            self.update("Failed", "Failed")

    def update(self, step_title, step_description, estimated_time=None):
        self.steps.next(step_description, step_title, estimated_time)
        # CalibrationManager.put(self.steps.get_status())
