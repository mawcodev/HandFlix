"""
File: cam.py
Description: This file use the image capture and processing OpenCV libraries. 
             Also, the MediaPipe libraries is used to detect hand pose.

Author: Matthew Conde Oltra
"""

import cv2
import mediapipe as mp

class VideoStream(object):
    
    #Initialize important variables
    def __init__(self):
        #Video capture 
        self.video = cv2.VideoCapture(0)
        #Drawing utils for hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        # For webcam input - initialize MediaPipe Hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    #
    def __del__(self):

        self.video.release()        

    def hand_pose(self):

        # Read each frame 
        ret, frame = self.video.read()
        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB) 
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = self.hands.process(image)

        # Draw hand landmarks of each hand
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
          for hand_landmarks in results.multi_hand_landmarks:
            # Draw index finger tip coordinates
            self.mp_drawing.draw_landmarks(
                image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        # Convert to jpeg
        ret, jpeg = cv2.imencode('.jpg', image)

        return jpeg.tobytes()
