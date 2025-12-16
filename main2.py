from Packages.aruco import Aruco 
from Packages.videocapture import VideoCapture 
from Packages.calibrator import Calibrate
import cv2 as cv 

def getCalibrate(dimension, folder_path):
    calibrator = Calibrate(board_diemension=dimension, folder_path=folder_path)
    calibrator.calibrateMatrix()
    
    return calibrator 
    
def main() -> None: 
    dimension = (7,7)
    calibrator = getCalibrate(dimension=dimension, folder_path ='images')
    capture = VideoCapture(0)
    capture.start() # get video capture continously
    marker = Aruco(capture=capture, calibrator=calibrator)
    marker.start() # detect marker continously
    
    while (True):

        if marker.ret is True:
            copy = capture.frame.copy()
            cv.aruco.drawDetectedMarkers(copy, marker.corners, marker.ids)
            cv.imshow('window', copy)
            dist = marker.calculateDistance()
            print(dist)
        else:
            
            cv.imshow('window', capture.frame)
        
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            marker.stop()
            capture.stop()
            break
    
if __name__ == "__main__":
    print("Hello World")
    main()

