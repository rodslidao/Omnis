import argparse
import pickle

from guess_aruco_type import ARUCO_DICT

from cv2 import waitKey, undistort, cvtColor, COLOR_BGR2GRAY, imshow, VideoCapture

from cv2.aruco import (
    DetectorParameters_create,
    detectMarkers,
    drawDetectedMarkers,
    estimatePoseSingleMarkers,
    drawAxis,
    DICT_7X7_1000,
    Dictionary_get,
)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Test Calibration files (.pckl) with the source."
    )

    parser.add_argument(
        "-c",
        "--cam_source",
        action="store",
        dest="cam_source",
        default=None,
        required=True,
        help="ID or path (/dev/video*)",
    )

    parser.add_argument(
        "-p",
        "--path",
        action="store",
        dest="path",
        default=None,
        required=True,
        help="Path for loadcalibration file. (pckl)",
    )

    args = parser.parse_args()

    def get_args(name, default_value):
        if getattr(args, name) is not None:
            return getattr(args, name)
        return default_value

    _id = int(args.cam_source) if args.cam_source.isdigit() else args.cam_source
    store = pickle.load(open(f"{get_args('path', './conf.pckl')}", "rb"))
    cam = VideoCapture(_id)

    while waitKey(1) & 0xFF != ord("q"):
        frame = cam.read()[1]
        imshow(f"ruim_{_id}", frame)
        frame = undistort(frame, store["mtx"], store["dist"], None)
        gray = cvtColor(frame, COLOR_BGR2GRAY)
        aruco_dict = Dictionary_get(ARUCO_DICT.get(store["dictonary"], DICT_7X7_1000))
        parameters = DetectorParameters_create()
        corners, ids, rejectedImgPoints = detectMarkers(
            gray, aruco_dict, parameters=parameters
        )
        frame_markers = drawDetectedMarkers(frame.copy(), corners, ids)
        size_of_marker = 0.023  # side lenght of the marker in meter
        rvecs, tvecs, _ = estimatePoseSingleMarkers(
            corners, size_of_marker, store["mtx"], store["dist"]
        )
        length_of_axis = size_of_marker / 2
        imaxis = drawDetectedMarkers(frame.copy(), corners, ids)
        if tvecs is not None:
            for i in range(len(tvecs)):
                imaxis = drawAxis(
                    imaxis,
                    store["mtx"],
                    store["dist"],
                    rvecs[i],
                    tvecs[i],
                    length_of_axis,
                )
        imshow(f"frame_{_id}", imaxis)
