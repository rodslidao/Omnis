from generate_data import generate_data
from generate_calib import charuco_calibration

from cv2 import VideoCapture


def calibrate_rotine(
    camera,
    frame_interval,
    data_set_size,
    min_blur,
    max_blur,
    show,
    export_path,
    squaresX,
    squaresY,
    squareLength,
    markerSize,
    dictionary_name,
):

    return charuco_calibration(
        generate_data(
            "./", camera, frame_interval, data_set_size, max_blur, min_blur, show, True
        ),
        export_path,
        squaresX,
        squaresY,
        squareLength,
        markerSize,
        dictionary_name,
    )


if __name__ == "__main__":
    print(
        calibrate_rotine(
            camera=VideoCapture(0),
            frame_interval=1000,
            data_set_size=20,
            min_blur=100,
            max_blur=6100,
            show=True,
            export_path="./data_0",
            squaresX=6,
            squaresY=9,
            squareLength=30,
            markerSize=23,
            dictionary_name="DICT_7X7_1000",
        )
    )
