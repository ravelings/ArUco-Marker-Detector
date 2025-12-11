import cv2 as cv 
import numpy as np 
from Packages.videocapture import VideoCapture

def main() -> int: 
    
    capture = VideoCapture(0)