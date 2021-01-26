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

                 #See hand coordinates and get thumb finger coordinates and wrist coordinates
                if results.multi_hand_landmarks:
                    multi_hand_coordinates = []
                    for hand_landmarks in results.multi_hand_landmarks:

                        ok_pose = self.ok_pose(hand_landmarks)
                        pause_pose = self.pause_pose(hand_landmarks)
                        stop_pose = self.stopPoseDetection(hand_landmarks.landmark)

                        #
                        if ok_pose:
                            print('Play video')
                        elif pause_pose:
                            print('Video pause')
                        elif stop_pose:
                            print('Stop video')
                            
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
        if(abs(index - middle) > 0.02 and abs(index - ring) > 0.02 and abs(index - pinky) > 0.02):
            return False
        else:
            return True

#
#@Name
#   ok_pose()
#@Description
# If hand pose is in hand pose 'oh rigth'
#
#   handmarks:np.array -->
#                         ok_pose()
#                                  --> boolean
#@Author
#   Matthew Conde Oltra
#@Date
#   26/01/2021
    def ok_pose(self, h):

        v = False
        #Finger Thumb
        
        #Take point 4
        point_4_x = h.landmark[self.mp_hands.HandLandmark.THUMB_TIP].x
        point_4_y = h.landmark[self.mp_hands.HandLandmark.THUMB_TIP].y
        #Take point 3
        point_3_x = h.landmark[self.mp_hands.HandLandmark.THUMB_IP].x
        point_3_y = h.landmark[self.mp_hands.HandLandmark.THUMB_IP].y
        #Take point 2
        point_2_x = h.landmark[self.mp_hands.HandLandmark.THUMB_MCP].x
        point_2_y = h.landmark[self.mp_hands.HandLandmark.THUMB_MCP].x
        #Take point 1
        point_1_x = h.landmark[self.mp_hands.HandLandmark.THUMB_CMC].x
        point_1_y = h.landmark[self.mp_hands.HandLandmark.THUMB_CMC].y

        ##Index finger mcp
        #Take point 5
        point_5_x = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].x
        point_5_y = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].y
        #Take point 6
        point_6_x = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP].x
        point_6_y = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP].y
        #Take point 7
        point_7_x = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_DIP].x
        point_7_y = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_DIP].y
        #Take point 8
        point_8_x = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x
        point_8_y = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y

        #Middle finger mcp
        point_9_x = h.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
        point_9_y = h.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
        #Take point 10
        point_10_x = h.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP].x
        point_10_y = h.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
        #Take point 11
        point_11_x = h.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_DIP].x
        point_11_y = h.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y
        #Take point 12
        point_12_x = h.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
        point_12_y = h.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y

        #Ring finger mcp
        point_13_x = h.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP].x
        point_13_y = h.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP].y
        #Take point 14
        point_14_x = h.landmark[self.mp_hands.HandLandmark.RING_FINGER_PIP].x
        point_14_y = h.landmark[self.mp_hands.HandLandmark.RING_FINGER_PIP].y
        #Take point 15
        point_15_x = h.landmark[self.mp_hands.HandLandmark.RING_FINGER_DIP].x
        point_15_y = h.landmark[self.mp_hands.HandLandmark.RING_FINGER_DIP].y
        #Take point 16
        point_16_x = h.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP].x
        point_16_y = h.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP].y

        #Pinky finger mcp
        point_17_x = h.landmark[self.mp_hands.HandLandmark.PINKY_MCP].x
        point_17_y = h.landmark[self.mp_hands.HandLandmark.PINKY_MCP].y
        #Take point 18
        point_18_x = h.landmark[self.mp_hands.HandLandmark.PINKY_PIP].x
        point_18_y = h.landmark[self.mp_hands.HandLandmark.PINKY_PIP].y
        #Take point 19
        point_19_x = h.landmark[self.mp_hands.HandLandmark.PINKY_DIP].x
        point_19_y = h.landmark[self.mp_hands.HandLandmark.PINKY_DIP].y
        #Take point 20
        point_20_x = h.landmark[self.mp_hands.HandLandmark.PINKY_TIP].x
        point_20_y = h.landmark[self.mp_hands.HandLandmark.PINKY_TIP].y

        #
        if point_2_x <= point_5_x and point_2_x >= point_1_x:
            if point_3_x <= point_5_x and point_3_x >= point_1_x:
                if point_4_x <= point_5_x and point_4_x >= point_1_x:
                    #
                    if point_17_y > point_13_y:
                        if point_13_y > point_9_y:
                            if point_9_y > point_5_y:
                                if point_8_x >= point_5_x and point_7_x >= point_5_x:
                                    if point_8_x <= point_6_x and point_7_x <= point_6_x:
                                        v = True

        return v


#
#@Name
#   pause_pose()
#@Description
# If hand pose is in hand pose 'oh rigth' but thumb is sleep
#
#   handmarks:np.array -->
#                         ok_pose()
#                                  --> boolean
#@Author
#   Matthew Conde Oltra
#@Date
#   26/01/2021
    def pause_pose(self, h):

        v = False
        #Finger Thumb
        
        #Take point 4
        point_4_x = h.landmark[self.mp_hands.HandLandmark.THUMB_TIP].x
        point_4_y = h.landmark[self.mp_hands.HandLandmark.THUMB_TIP].y
        #Take point 3
        point_3_x = h.landmark[self.mp_hands.HandLandmark.THUMB_IP].x
        point_3_y = h.landmark[self.mp_hands.HandLandmark.THUMB_IP].y
        #Take point 2
        point_2_x = h.landmark[self.mp_hands.HandLandmark.THUMB_MCP].x
        point_2_y = h.landmark[self.mp_hands.HandLandmark.THUMB_MCP].x
        #Take point 1
        point_1_x = h.landmark[self.mp_hands.HandLandmark.THUMB_CMC].x
        point_1_y = h.landmark[self.mp_hands.HandLandmark.THUMB_CMC].y

        #Index finger mcp
        #Take point 5
        point_5_x = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].x
        point_5_y = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].y
        #Take point 6
        point_6_x = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP].x
        point_6_y = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP].y
        #Take point 7
        point_7_x = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_DIP].x
        point_7_y = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_DIP].y
        #Take point 8
        point_8_x = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x
        point_8_y = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y
        

        #Middle finger mcp
        point_9_x = h.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
        point_9_y = h.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y

        #Ring finger mcp
        point_13_x = h.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP].x
        point_13_y = h.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP].y

        #Pinky finger mcp
        point_17_x = h.landmark[self.mp_hands.HandLandmark.PINKY_MCP].x
        point_17_y = h.landmark[self.mp_hands.HandLandmark.PINKY_MCP].y

        if point_17_y > point_13_y:
            if point_13_y > point_9_y:
                if point_9_y > point_5_y:
                    #print(point_5_x)
                    #print(point_3_x)
                    if point_4_x <= point_6_x and point_3_x >= point_5_x or point_4_x >= point_6_x and point_3_x >= point_5_x:
                        v = True
                
                                

        return v
