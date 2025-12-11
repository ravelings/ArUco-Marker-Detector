import cv2 as cv 
from Packages.calibrator import Calibrate 
from Packages.videocapture import VideoCapture

def main() -> None:
    
    board_dim = (7, 7)
    
    capture = VideoCapture(0)
    capture.start()
    calibrator = Calibrate(board_dim, folder_path=None, capture=capture)
    calibrator.start()
    
    while True:
        cv.imshow('Camera', capture.frame)
        #print(f'Calibrator canvas: {calibrator.canvas}')
        if calibrator.canvas is not None:
            cv.imshow('Corners', calibrator.canvas)
        
        key = cv.waitKey(1)
        if key == ord('q'):
            cv.destroyAllWindows()
            calibrator.stop()
            capture.stop()
            break
        if key == ord('s'):
            capture.save()
            
    print("Program ended.")
    
main()