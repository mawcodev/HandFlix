"""
File: cam.py
Description: This file use the image capture and processing OpenCV libraries. 
             Also, the MediaPipe libraries is used to detect hand pose.

Author: Matthew Conde Oltra
"""

import cv2
import mediapipe as mp
import numpy as np



class VideoStream(object):
    
    #Initialize important variables
    def __init__(self):
        self.play_counter = 0
        self.pause_counter = 0
        self.stop_counter = 0
        self.debug_counter = 0
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

        #If don't found a hand, return image only
        if results.multi_handedness == None:
            #solo devuelve la imagen de streaming
            #print('Type value is None')
            # Convert to jpeg
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()
        #If found a hand identify pose
        else:
            #print('Handedness: ', results.multi_handedness[0].classification[0].label)
            what_hand = results.multi_handedness[0].classification[0].label
            #If hand is left draw
            if what_hand == 'Left':
                #print('Left hand')

                 #See hand coordinates and get thumb finger coordinates and wrist coordinates
                if results.multi_hand_landmarks:
                    multi_hand_coordinates = []
                    for hand_landmarks in results.multi_hand_landmarks:
                        
                        #Call funtions to detect pose
                        self.stop_pose_detection(hand_landmarks.landmark)
                        self.debug_pose_detection(hand_landmarks.landmark)
                        self.ok_pose(hand_landmarks)
                        self.pause_pose(hand_landmarks)


                        if(self.stop_counter > 10):
                            print("STOP")
                            self.stop_counter = 0
                        if(self.debug_counter > 20):
                            print("DEBUG")
                            self.debug_counter = 0
                        if(self.play_counter > 20):
                            print("PLAY")
                            self.play_counter = 0
                        if(self.pause_counter > 20):
                            print("PAUSE")
                            self.pause_counter = 0

                    # Draw index finger tip coordinates
                    self.mp_drawing.draw_landmarks(
                        image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                # Convert to jpeg
                ret, jpeg = cv2.imencode('.jpg', image)
                return jpeg.tobytes()
                
            #If hand is rigth don't draw
            else:
                #print('You must use rigth hand')
                # Convert to jpeg
                ret, jpeg = cv2.imencode('.jpg', image)

                return jpeg.tobytes()

            ret, jpeg = cv2.imencode('.jpg', image)

            return jpeg.tobytes()
    #
    #@Name
    # stop_pose_detection()
    #@Description
    # If a hand pose is in STOP pose
    #
    # landmarks: np.array
    #                 -->
    #                       stop_pose_detection()
    #                                       -->
    #                                           void
    # @Author
    # Oscar Blanquez
    # @Date
    # 26/01/2021
    def stop_pose_detection(self, landmark):
        index = landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].y
        middle = landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
        ring = landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP].y
        pinky = landmark[self.mp_hands.HandLandmark.PINKY_MCP].y
        if(abs(index - middle) < 0.02 and abs(index - ring) < 0.02 and abs(index - pinky) < 0.02):
            self.stop_counter += 1
        else:
            return
    #
    #@Name
    # debug_pose_detection()
    #@Description
    # If a hand pose is in troll pose
    #
    # landmarks: np.array
    #                 -->
    #                       debug_pose_detection()
    #                                       -->
    #                                           void
    # @Author
    # Oscar Blanquez
    # @Date
    # 26/01/2021
    def debug_pose_detection(self, landmark):
        thumb = landmark[self.mp_hands.HandLandmark.THUMB_TIP].y
        index = landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y
        if(abs(thumb - index) < 0.05):
            self.debug_counter += 1
        else:
            return

#
#@Name
#   ok_pose()
#@Description
# If hand pose is in hand pose 'oh rigth'
#
#   handmarks:np.array -->
#                         ok_pose()
#                                  --> void
#@Author
#   Matthew Conde Oltra
#@Date
#   26/01/2021
    def ok_pose(self, h):

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
                                        self.play_counter += 1


#
#@Name
#   pause_pose()
#@Description
# If hand pose is in hand pose 'oh rigth' but thumb is sleep
#
#   handmarks:np.array -->
#                         pause_pose()
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
                        self.pause_counter += 1
