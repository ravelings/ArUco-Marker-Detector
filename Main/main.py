import cv2 as cv 
from cv2 import aruco as aruco

def getMarker(image):
    dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    param = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(dict, param)
    
    corners, ids, _ = detector.detectMarkers(image)
    
    if ids is not None:
        print("Detection successful")
        return corners, ids
    else:
        print("Error in detection")
        return None

def main() -> None: 
    image = cv.imread('images/ToDetect/Detect Markers 2.jpg', cv.IMREAD_UNCHANGED)
    corners, ids = getMarker(image)
    print("ids: ", ids)
    aruco.drawDetectedMarkers(image, corners, ids)
    while (True):
        cv.imshow('image', image)
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break 
    print("Program ended")
    return

main()
