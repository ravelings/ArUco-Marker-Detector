import cv2 as cv 
import numpy as np
import os  
import glob as glob
import threading

class Calibrate():
    def __init__(self, board_diemension, folder_path, capture=None):
        # prelim
        self.capture    = capture # for drawCorners()
        self.folder_path = folder_path
        self.diemension = np.array(board_diemension, dtype=np.uint8)
        self.criteria   = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.canvas     = None
        self.image      = None
        # cam matrix
        self.ret        = None
        self.matrix     = None
        self.dist_cof   = None
        self.rot_vec    = None
        self.trans_vec  = None 
        # init obj and img points
        self.objp = np.zeros((board_diemension[0]*board_diemension[1],3), np.float32)
        self.objp[:,:2] = np.mgrid[0:board_diemension[0],0:board_diemension[1]].T.reshape(-1,2)
        self.objpoints  = []
        self.imgpoints  = []
        # threading
        self.thread     = None
        self.stopped    = True
        
    def start(self):
        self.stopped = False
        self.thread = threading.Thread(target=self.drawCorners, daemon=True)
        self.thread.start()
        print("Calibrator thread starts")
        return self
    
    def stop(self):
        self.stopped = True
        if self.thread:
            self.thread.join(timeout=1)
    def findCorners(self, image):
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(gray, (self.diemension[0],self.diemension[1]), None)
        if ret == True:
            corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), self.criteria)
            return ret, corners2
        else:
            return ret, corners

    def calibrateMatrix(self):
        file = glob.glob(f'{self.folder_path}/*.jpeg')
        #print(f'Working path: {os.getcwd()}')
        for image in file: # loop through folder
            read = cv.imread(image, cv.IMREAD_UNCHANGED)# read image as gray
            print(f'file: {image}')
            cv.waitKey(100)
            ret, corners = self.findCorners(read)
            if ret == True:
                self.objpoints.append(self.objp)
                
                self.imgpoints.append(corners)
                
            else:
                print(f"Error in file: {self.folder_path}/{file} ") 
                break
        else:
            print("All points stored.")
            image2 = (cv.imread(file[0], cv.IMREAD_GRAYSCALE))
            ret, self.matrix, self.dist_cof, self.rot_vec, self.trans_vec = cv.calibrateCamera(
                self.objpoints,
                self.imgpoints,
                image2.shape[::-1],
                None,
                None
                )
            print("Return is: ", ret)
            self.ret = ret
        
    def drawCorners(self):
        while not self.stopped:
            canvas = self.capture.frame.copy()
            ret, corners = self.findCorners(canvas)
            if ret:
                cv.drawChessboardCorners(canvas,
                                        (self.diemension[0], self.diemension[1]),
                                        corners,
                                        ret
                                        )
                #print("Drawn successfully")
                self.canvas = canvas
            else:
                print("No corners to be drawn")
                self.canvas = canvas