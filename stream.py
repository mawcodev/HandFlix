"""
File: stream.py
Description: This file use the image capture and processing OpenCV libraries. 
Author: Matthew Conde Oltra
"""

import cv2

class VideoStream(object):
    
    #Initialize important variables
    def __init__(self):
        #Video capture 
        self.video = cv2.VideoCapture(0)
    def __del__(self):

        self.video.release()        

    def get_frame(self):

        # Read each frame 
        ret, frame = self.video.read()
        # Convert to jpeg
        ret, jpeg = cv2.imencode('.jpg', image)

        return jpeg.tobytes()
