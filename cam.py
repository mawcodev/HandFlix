"""
File: cam.py
Description: This file use the image capture and processing OpenCV libraries. 
             Also, the MediaPipe libraries is used to detect hand pose.

Author: Matthew Conde Oltra
"""

import cv2
import mediapipe as mp
import numpy as np

STOP_POSE = np.array([[458.9168644, 146.58317566],
                    [442.23644257, 200.36252975],
                    [418.75642776, 243.5219574 ],
                    [391.6795063,  278.67773056],
                    [371.20339394, 304.28642273],
                    [354.96382713, 204.44623947],
                    [301.20789528, 231.46738052],
                    [265.01764297, 246.67585373],
                    [234.32318687, 257.59262085],
                    [345.41095734, 173.3524704 ],
                    [287.27119446, 193.45767975],
                    [246.80110931, 206.39400482],
                    [214.25803185, 215.50016403],
                    [347.53460884, 142.29740143],
                    [294.08763885, 145.60795784],
                    [256.52137756, 148.37759972],
                    [225.27832031, 151.39935493],
                    [360.45687675, 112.87567139],
                    [321.61253929,  95.44146538],
                    [295.55768967,  84.65111732],
                    [271.31263733,  76.93968773]])



class VideoStream(object):
    
    #Initialize important variables
    def __init__(self):
        #Video capture 
        self.video = cv2.VideoCapture(0)
        #Drawing utils for hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        # For webcam input - initialize MediaPipe Hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        #Coordinates
        self.hand_coordinates = []
    def __del__(self):

        self.video.release()        

    def hand_pose(self):

        #print("Array stop pose: ",STOP_POSE)
        #print(len(STOP_POSE))
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
        image_height, image_width, _ = image.shape

        #Sí no encuentra manos no hará nada, pero devolverá image
        if results.multi_handedness == None:
            #solo devuelve la imagen de streaming
            #print('Type value is None')
            # Convert to jpeg
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()
        #Sí encuentra manos identificara cual es
        else:
            #print('Handedness: ', results.multi_handedness[0].classification[0].label)
            what_hand = results.multi_handedness[0].classification[0].label
            #Si la mano es la izquierda dibujara las landmarks
            if what_hand == 'Left':
                print('Left hand')

                if results.multi_hand_landmarks:
                    multi_hand_coordinates = []
                    for hand_landmarks in results.multi_hand_landmarks:

                        self.stopPoseDetection(hand_landmarks.landmark)

                        x = [landmark.x for landmark in hand_landmarks.landmark]
                        y = [landmark.y for landmark in hand_landmarks.landmark]
                        
                        self.hand_coordinates = np.transpose(np.stack((y, x))) * image.shape[0:2]
                        #print(self.hand_coordinates)
                        #print(STOP_POSE[0][0])
                        if round(STOP_POSE[0][0]) == round(self.hand_coordinates[0][0]):
                            print("Son iguales: ", self.hand_coordinates[0][0])

                    # Draw index finger tip coordinates
                    self.mp_drawing.draw_landmarks(
                        image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                # Convert to jpeg
                ret, jpeg = cv2.imencode('.jpg', image)
                return jpeg.tobytes()
            #sí la mano es la derecha no dibujara landmarks pero si devolvera image
            else:
                print('Debes utilizar la mano derecha')
                # Convert to jpeg
                ret, jpeg = cv2.imencode('.jpg', image)

                return jpeg.tobytes()

            ret, jpeg = cv2.imencode('.jpg', image)

            return jpeg.tobytes()
    def stopPoseDetection(self, landmark):
        index = landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].y
        middle = landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
        ring = landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP].y
        pinky = landmark[self.mp_hands.HandLandmark.PINKY_MCP].y
        if(abs(index - middle) > 0.02 or abs(index - ring) > 0.02 or abs(index - pinky) > 0.02):
            return False
        else:
            return True