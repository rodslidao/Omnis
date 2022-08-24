from cv2 import (
    moments,
    cvtColor,
    COLOR_BGR2GRAY,
    warpPerspective,
    getPerspectiveTransform,
)

from numpy import squeeze, where, array, float32
from cv2.aruco import detectMarkers


def center(array):
    M = moments(array)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return (cX, cY)


def ROI_ARUCO(img, aruco_dict, aruco_parms, aruco_sequence_id=[160, 130, 159, 43], corners=None, ids=None):
    """
    return: ROI, (refPtTL, refPtTR, refPtBL, refPtBR)
    """
    if corners is None and ids is None:
        corners, ids, _ = detectMarkers(
            cvtColor(img, COLOR_BGR2GRAY),
            aruco_dict,
            parameters=aruco_parms,
        )
    ids = ids.flatten() if ids is not None else []
    if len(ids) == 4:
        try:
            refPts = [squeeze(corners[squeeze(where(ids == i))]) for i in aruco_sequence_id]
            dstMat = array(list(map(center, refPts)))
            x = [p[0] for p in dstMat]
            y = [p[1] for p in dstMat]
            sizes = [width, heigth] = [max(x) - min(x), max(y) - min(y)]
            return (
                warpPerspective(
                    img,
                    getPerspectiveTransform(
                        float32(dstMat), float32([[0, 0], [width, 0], [0, heigth], sizes])
                    ),
                    (width, heigth),
                ),
                dstMat,
                )
        except TypeError:
            pass
    return (img, [])
