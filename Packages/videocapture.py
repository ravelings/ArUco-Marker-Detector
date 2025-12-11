import cv2 as cv 
import threading 
import os

class VideoCapture:
    
    def __init__(self, camera=0, savePath=None):
        #camera
        self.camera = camera
        self.stream = cv.VideoCapture(camera)
        self.grabbed, self.frame = self.stream.read()
        # save image
        self.count  = 0 # number of saves
        self.name   = "image"
        #threading
        self.stopped = False
        self.thread = None
        self.exchange = None
        
        if savePath is None:
            current_dir = os.getcwd()
            savePath = f'{current_dir}/images'
            if not os.path.isdir(f'{current_dir}/images'):
                os.makedirs(savePath)
                self.path = savePath
                print(f'Image path created at: {current_dir}/images')
            else:
                self.path = savePath
        
    
    def start(self):
        if self.thread and self.thread.is_alive():
            print("Video Capture thread already running")
            return self
        self.stopped = False
        self.thread = threading.Thread(target=self.get, daemon=True)
        self.thread.start()
        print("Video Capture thread starts")
        return self
    
    def stop(self):
        self.stopped = True
        if self.thread:
            self.stream.release()
            self.thread.join(timeout=1)
    
    def get(self):
        while not self.stopped:
            self.grabbed, self.frame = self.stream.read()
        """ if self.grabbed:
            print("Frame grabbed")"""
    
    def save(self):
        if self.grabbed:
            print(f'{self.path}/{self.name}_{self.count}.jpeg')
            cv.imwrite( f'{self.path}/{self.name}_{self.count}.jpeg',self.frame)
            print("Image saved successfully")
            self.count += 1
        else:
            print("Save fail: No frame grabbed")
            
    def setName(self, name):
        assert name is str, 'TypeError: Name is not string'
        self.name = name