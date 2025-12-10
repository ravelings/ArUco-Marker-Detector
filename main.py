import cv2 as cv 
import numpy as np
from cv2 import aruco as aruco

def generateMarker(dict, id, size, border):

    canvas = np.zeros((size, size), dtype=np.uint8)

    return aruco.generateImageMarker(
    dictionary=dict,
    id=id,
    img=canvas,
    sidePixels=size,
    borderBits=border)

def main() -> None:    
    marker_id = 0 # image counter
    marker_size = 200
    border_bits = 1


    image_path = "images"

    arucoDict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

    marker_image = generateMarker(arucoDict, marker_id, marker_size, border_bits)

    cv.namedWindow('Marker', cv.WINDOW_NORMAL)
    while (True):
        cv.imshow('Marker', marker_image)
        print(f"Marker: {marker_id}")
        key = cv.waitKey(1)
        if key == ord('s'):
            cv.imwrite(f'{image_path}/Marker{marker_id}.jpeg', marker_image)
            marker_id += 1
            marker_image = generateMarker(arucoDict, marker_id, marker_size, border_bits)
        if key == ord('q'):
            cv.destroyAllWindows()
            break
    
main()