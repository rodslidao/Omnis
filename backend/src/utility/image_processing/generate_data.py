from cv2 import imshow, imwrite, waitKey, CV_64F, Laplacian, VideoCapture
from datetime import datetime, timedelta

from os.path import exists
from os import makedirs

from shutil import rmtree

import argparse


def variance_of_laplacian(image):
    return Laplacian(image, CV_64F).var()


def generate_data(
    relative_path,
    camera,
    interval=1500,
    data_set_size=100,
    max_blur=1100,
    min_blur=300,
    show=False,
    internal=False,
):
    """
    Generate data for the given id.
    """
    if not internal:
        if exists(relative_path):
            op = input(f"{relative_path} already exists. Overwrite? [y/n]\nR: ")
            if op.lower() != "y":
                print(f"Directory {relative_path} already exists")
                camera.release()
            else:
                rmtree(relative_path)
                print(f"Created directory {relative_path}")
        makedirs(relative_path)
    else:
        data = []

    start = datetime.utcnow()
    for counter in range(data_set_size):
        frame = camera.read()
        if isinstance(frame, tuple):
            frame = frame[1]
        if show:
            imshow("frame", frame)
            waitKey(1)
        blur = variance_of_laplacian(frame)
        if (datetime.utcnow() - start) > timedelta(milliseconds=interval):
            print("blur:", blur)
            if not (min_blur < blur < max_blur):
                continue
            print(f"{counter}/{data_set_size}")

            if not internal:
                imwrite(
                    f"{relative_path}/frame_" + str(counter) + ".png",
                    frame,
                )
            else:
                data.append(frame)

            start = datetime.utcnow()
    return data


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Generate images for calibration process."
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
        "-e",
        "--export",
        action="store",
        dest="images_path",
        default="./images/source_0",
        required=False,
        help="Path to save images. eg ./images/source_0",
    )

    parser.add_argument(
        "-s",
        "--show",
        action="store",
        dest="show",
        default=False,
        required=False,
        help="Flag to open an window and show images during capture process",
    )

    parser.add_argument(
        "-i",
        "--interval",
        action="store",
        dest="interval",
        default=1500,
        required=False,
        help="Interval between frames in milliseconds",
    )

    parser.add_argument(
        "-d",
        "--data_set_size",
        action="store",
        dest="data_set_size",
        default=20,
        required=False,
        help="Number of images to generate",
    )

    parser.add_argument(
        "-m",
        "--max_blur",
        action="store",
        dest="max_blur",
        default=700,
        required=False,
        help="Max blur value to accept",
    )

    parser.add_argument(
        "-n",
        "--min_blur",
        action="store",
        dest="min_blur",
        default=5,
        required=False,
        help="Min blur value to accept",
    )

    args = parser.parse_args()

    generate_data(
        f"{args.images_path}/",
        VideoCapture(
            int(args.cam_source) if args.cam_source.isdigit() else args.cam_source
        ),
        float(args.interval),
        int(args.data_set_size),
        int(args.max_blur),
        int(args.min_blur),
        args.show == "True",
    )
