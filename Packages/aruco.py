from cv2 import aruco as aruco
from cv2 import solvePnP
import numpy as np
import threading

class Aruco:
    def __init__(self, capture, calibrator):
        # init detector
        ## default dict = 6x6 250
        self.dict       = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
        self.param      = param = aruco.DetectorParameters()
        self.detector   = aruco.ArucoDetector(self.dict, self.param)
        # capture
        self.capture = capture
        # marker storage
        self.ids = []
        self.corners = []
        self.ret = False
        # camera calibration
        self.calibrator = calibrator
        # distancing
        self.rvec_id = None 
        self.tvec_id = None
        # threading
        self.stopped = False
        self.thread = None

    def start(self):
        self.stopped = False
        self.thread = threading.Thread(target=self.findMarker, daemon=True)
        self.thread.start()
        print("Aruco thread starts")
        return self
    
    def stop(self):
        self.stopped = True
        if self.thread:
            self.thread.join(timeout=1)
    
    def findMarker(self):
        while not self.stopped:
            corners, ids, _ = self.detector.detectMarkers(self.capture.frame)
    
            if ids is not None:
                # Marker detected
                self.ids = ids
                self.corners = corners
                self.ret = True
            else:
                # No marker found
                self.ret = False
                continue
    
    def findObjectPoints(self, index):
        print("Corners shape: ", self.corners)
        corners2 = self.corners[index]
        Z = 0
        MARKER_SIZE = 2.1 # cm
        center = [ 
                ( corners2[0][0] + corners2[1][0] ) / 2,
                ( corners2[0][1] + corners2[1][1] ) / 2 
                ]
        return [Z, MARKER_SIZE, center]
    
    def getVector(self, id):
        accesor = np.where(self.ids == id)
        index = accesor[0]
        if len(index) > 0: 
            
            objpoints = self.findObjectPoints(index[0])
            ret, rvec_id, tvec_id = solvePnP(
                objpoints,
                self.corners[index[0][0]], # imgpoints
                self.calibrator.matrix,
                self.calibrator.dist_cof,
                useExtrinsicGuess=False
            ) 
            if ret is True:
                return tvec_id, rvec_id
            else:
                print("Vector not found")
                return None, None
        else:
            print("index:", index)
            print("ids: ", self.ids)
            print("Corners at index 0: ", self.corners[0])
            
            #print("Index not found")
            return None, None 
    def calculateDistance(self, id=1):
        if self.ret is True:
            tvec_id, _ = self.getVector(id)
            if tvec_id is not None:
                access = np.where(self.ids == id)
                index = access[0]
                dist = np.sqrt(tvec_id[index][0][0]**2 
                            + tvec_id[index][0][1]**2
                            + tvec_id[index][0][2]**2)
                return dist 
            else:
                #print("No translation vector")
                return None
        else:
            return None
