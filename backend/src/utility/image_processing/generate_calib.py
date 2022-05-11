import os
import pickle
import cv2
from cv2 import aruco
import numpy as np
import argparse

from cv2.aruco import (
    DICT_4X4_50,
    DICT_4X4_100,
    DICT_4X4_250,
    DICT_4X4_1000,
    DICT_5X5_50,
    DICT_5X5_100,
    DICT_5X5_250,
    DICT_5X5_1000,
    DICT_6X6_50,
    DICT_6X6_100,
    DICT_6X6_250,
    DICT_6X6_1000,
    DICT_7X7_50,
    DICT_7X7_100,
    DICT_7X7_250,
    DICT_7X7_1000,
    DICT_ARUCO_ORIGINAL,
    DICT_APRILTAG_16h5,
    DICT_APRILTAG_25h9,
    DICT_APRILTAG_36h10,
    DICT_APRILTAG_36h11,
    Dictionary_get,
)

ARUCO_DICT = {
    "DICT_4X4_50": DICT_4X4_50,
    "DICT_4X4_100": DICT_4X4_100,
    "DICT_4X4_250": DICT_4X4_250,
    "DICT_4X4_1000": DICT_4X4_1000,
    "DICT_5X5_50": DICT_5X5_50,
    "DICT_5X5_100": DICT_5X5_100,
    "DICT_5X5_250": DICT_5X5_250,
    "DICT_5X5_1000": DICT_5X5_1000,
    "DICT_6X6_50": DICT_6X6_50,
    "DICT_6X6_100": DICT_6X6_100,
    "DICT_6X6_250": DICT_6X6_250,
    "DICT_6X6_1000": DICT_6X6_1000,
    "DICT_7X7_50": DICT_7X7_50,
    "DICT_7X7_100": DICT_7X7_100,
    "DICT_7X7_250": DICT_7X7_250,
    "DICT_7X7_1000": DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": DICT_APRILTAG_36h11,
}


def generate_charuco_board(
    squaresX=6,
    squaresY=9,
    squareLength=30,
    markerLength=23,
    dictionary="DICT_7X7_1000",
    **kwargs,
):
    """
    Generate a charuco board.
    """
    dictionary = Dictionary_get(ARUCO_DICT.get(dictionary, DICT_7X7_1000))
    board = aruco.CharucoBoard_create(
        squaresX, squaresY, squareLength, markerLength, dictionary
    )
    _ = board.draw(kwargs.get("outSize", (1280, 720)))
    if kwargs.get("show", False):
        cv2.imshow("Charuco Board", _)
        cv2.waitKey(0)
    if kwargs.get("save", False):
        cv2.imwrite(
            kwargs.get(
                "savePath", f"charuco_board_{squaresX}X_{squaresY}_{dictionary}.png"
            ),
            _,
        )

    return board, dictionary


def sort_images(path):
    images = np.array([path + f for f in os.listdir(path) if f.endswith(".jpg")])
    order = np.argsort([int(p.split(".")[-2].split("_")[-1]) for p in images])
    return list(map(cv2.imread, images[order]))


def read_chessboards(images, board, aruco_dict):
    """
    Charuco base pose estimation.
    """
    print("POSE ESTIMATION STARTS:")
    allCorners = []
    allIds = []
    decimator = 0
    # SUB PIXEL CORNER DETECTION CRITERION
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)

    for frame in images:
        # print("=> Processing image {0}".format(im))
        # frame = cv2.imread(im)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict)

        if len(corners) > 0:
            # SUB PIXEL DETECTION
            for corner in corners:
                cv2.cornerSubPix(
                    gray, corner, winSize=(3, 3), zeroZone=(-1, -1), criteria=criteria
                )
            res2 = cv2.aruco.interpolateCornersCharuco(corners, ids, gray, board)
            if (
                res2[1] is not None
                and res2[2] is not None
                and len(res2[1]) > 3
                and decimator % 1 == 0
            ):
                allCorners.append(res2[1])
                allIds.append(res2[2])

        decimator += 1

    imsize = gray.shape
    return allCorners, allIds, imsize


def calibrate_camera(allCorners, allIds, imsize, board):
    """
    Calibrates the camera using the dected corners.
    """
    print("CAMERA CALIBRATION")

    cameraMatrixInit = np.array(
        [
            [1000.0, 0.0, imsize[0] / 2.0],
            [0.0, 1000.0, imsize[1] / 2.0],
            [0.0, 0.0, 1.0],
        ]
    )

    distCoeffsInit = np.zeros((5, 1))
    flags = (
        cv2.CALIB_USE_INTRINSIC_GUESS
        + cv2.CALIB_RATIONAL_MODEL
        + cv2.CALIB_FIX_ASPECT_RATIO
    )
    # flags = (cv2.CALIB_RATIONAL_MODEL)
    (
        ret,
        camera_matrix,
        distortion_coefficients0,
        rotation_vectors,
        translation_vectors,
        stdDeviationsIntrinsics,
        stdDeviationsExtrinsics,
        perViewErrors,
    ) = cv2.aruco.calibrateCameraCharucoExtended(
        charucoCorners=allCorners,
        charucoIds=allIds,
        board=board,
        imageSize=imsize,
        cameraMatrix=cameraMatrixInit,
        distCoeffs=distCoeffsInit,
        flags=flags,
        criteria=(cv2.TERM_CRITERIA_EPS & cv2.TERM_CRITERIA_COUNT, 10000, 1e-9),
    )

    return (
        ret,
        camera_matrix,
        distortion_coefficients0,
        rotation_vectors,
        translation_vectors,
    )


def charuco_calibration(
    path="./images/stereoLeft/",
    export_path="./data_calib",
    squaresX=6,
    squaresY=9,
    squareLength=30,
    markerLength=23,
    dictionary="DICT_7X7_1000",
    **kwargs,
):
    board, aruco_dict = generate_charuco_board(
        squaresX, squaresY, squareLength, markerLength, dictionary, **kwargs
    )
    images = sort_images(path) if isinstance(path, str) else path
    allCorners, allIds, imsize = read_chessboards(images, board, aruco_dict)
    ret, mtx, dist, rvecs, tvecs = calibrate_camera(allCorners, allIds, imsize, board)
    store = {
        "ret": ret,
        "mtx": mtx,
        "dist": dist,
        "rvecs": rvecs,
        "tvecs": tvecs,
        "corners": allCorners,
        "dictonary": dictionary,
        "squaresX": squaresX,
        "squaresY": squaresY,
        "squareLength": squareLength,
        "markerLength": markerLength,
    }
    f = open(f"{export_path}.pckl", "wb")
    pickle.dump(store, f)
    return store


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Test Calibration files (.pckl) with the source."
    )

    parser.add_argument(
        "-e",
        "--export",
        action="store",
        dest="export_path",
        default="./data",
        required=False,
        help="Path for save calibration file. eg ./data_0",
    )

    parser.add_argument(
        "-f",
        "--from",
        action="store",
        dest="images_path",
        default="./images/source_0",
        required=False,
        help="Images for calibration process. eg ./images/source_0",
    )

    args = parser.parse_args()
    charuco_calibration(
        f"{args.images_path}/",
        f"{args.export_path}",
    )
