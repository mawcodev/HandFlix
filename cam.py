"""
File: cam.py
Description: This file use the image capture and processing OpenCV libraries. 
             Also, the MediaPipe libraries is used to detect hand pose.

Author: Matthew Conde Oltra
"""

import cv2
import mediapipe as mp
import numpy as np

"""
This code is used to take fingers dot

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
        point_17_y = h.landmark[self.mp_hands.HandLandmark.PINKY_MCP].y"""

class VideoStream(object):
    
    #Initialize important variables
    def __init__(self):
        self.play_counter = 0
        self.pause_counter = 0
        self.stop_counter = 0
        self.debug_counter = 0
        self.response = "."
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
        
    def getGesture(self):
        return self.response

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
            #return streaming image only
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
                        self.stop_pose_detection(hand_landmarks)
                        self.debug_pose_detection(hand_landmarks)
                        self.ok_pose(hand_landmarks)
                        self.pause_pose(hand_landmarks)


                        if(self.stop_counter > 10):
                            self.response = 'STOP'
                            print("STOP")
                            self.stop_counter = 0
                        if(self.debug_counter > 20):
                            self.response = 'DEBUG'
                            print("DEBUG")
                            self.debug_counter = 0
                        if(self.play_counter > 20):
                            self.response = 'PLAY'
                            print("PLAY")
                            self.play_counter = 0
                        if(self.pause_counter > 20):
                            self.response = 'PAUSE'
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
    #  handmarks:np.array
    #                 -->
    #                       stop_pose_detection()
    #                                       -->
    #                                           void
    # @Author
    # Oscar Blanquez
    # @Date
    # 26/01/2021
    def stop_pose_detection(self, h):
        
        #Wrist
        point_0_x = h.landmark[self.mp_hands.HandLandmark.WRIST].x
        point_0_y = h.landmark[self.mp_hands.HandLandmark.WRIST].y
        #Finger Thumb
        #Take point 4
        point_4_x = h.landmark[self.mp_hands.HandLandmark.THUMB_TIP].x
        point_4_y = h.landmark[self.mp_hands.HandLandmark.THUMB_TIP].y
        ##Index finger
        #Take point 5
        point_5_x = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].x
        point_5_y = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].y
        #Take point 8
        point_8_x = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x
        point_8_y = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y

        #Middle finger
        #Take point 9
        point_9_x = h.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
        point_9_y = h.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
        #Take point 12
        point_12_x = h.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
        point_12_y = h.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y

        #Ring finger
        #Take point 13
        point_13_x = h.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP].x
        point_13_y = h.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP].y
        #Take point 16
        point_16_x = h.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP].x
        point_16_y = h.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP].y

        #Pinky finger
        #Take point 17
        point_17_x = h.landmark[self.mp_hands.HandLandmark.PINKY_MCP].x
        point_17_y = h.landmark[self.mp_hands.HandLandmark.PINKY_MCP].y
        #Take point 20
        point_20_x = h.landmark[self.mp_hands.HandLandmark.PINKY_TIP].x
        point_20_y = h.landmark[self.mp_hands.HandLandmark.PINKY_TIP].y

        if(abs(point_5_y - point_9_y) < 0.02 and abs(point_5_y - point_13_y) < 0.02 and abs(point_5_y - point_17_y) < 0.02):            
            self.stop_counter += 1
        else:
            return
    #
    #@Name
    # debug_pose_detection()
    #@Description
    # If a hand pose is in troll pose
    #
    #  handmarks:np.array
    #                 -->
    #                       debug_pose_detection()
    #                                       -->
    #                                           void
    # @Author
    # Oscar Blanquez
    # @Date
    # 26/01/2021
    def debug_pose_detection(self, h):

        #Finger Thumb
        #Take point 4
        point_4_x = h.landmark[self.mp_hands.HandLandmark.THUMB_TIP].x
        point_4_y = h.landmark[self.mp_hands.HandLandmark.THUMB_TIP].y

        ##Index finger
        #Take point 8
        point_8_x = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x
        point_8_y = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y

        #Middle finger
        #Take point 12
        point_12_x = h.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
        point_12_y = h.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y

        #Ring finger
        #Take point 16
        point_16_x = h.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP].x
        point_16_y = h.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP].y

        #Pinky finger
        #Take point 20
        point_20_x = h.landmark[self.mp_hands.HandLandmark.PINKY_TIP].x
        point_20_y = h.landmark[self.mp_hands.HandLandmark.PINKY_TIP].y
        
        if (abs(point_4_y - point_8_y) < 0.05) :     
            if point_12_y < point_8_y and point_12_y < point_4_y:
                if point_16_y < point_8_y and point_16_y < point_4_y:
                    if point_20_y < point_8_y and point_20_y < point_4_y:
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

        ##Index finger
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

        #Middle finger
        point_9_x = h.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
        point_9_y = h.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y

        #Ring finger
        point_13_x = h.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP].x
        point_13_y = h.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP].y

        #Pinky finger
        point_17_x = h.landmark[self.mp_hands.HandLandmark.PINKY_MCP].x
        point_17_y = h.landmark[self.mp_hands.HandLandmark.PINKY_MCP].y
        

        #
        if point_2_x <= point_5_x and point_2_x >= point_1_x:
            if point_3_x <= point_5_x and point_3_x >= point_1_x:
                if point_4_x <= point_5_x and point_4_x >= point_1_x:
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
#                                  --> void
#@Author
#   Matthew Conde Oltra
#@Date
#   26/01/2021
    def pause_pose(self, h):

        #Finger Thumb
        #Take point 4
        point_4_x = h.landmark[self.mp_hands.HandLandmark.THUMB_TIP].x
        point_4_y = h.landmark[self.mp_hands.HandLandmark.THUMB_TIP].y
        #Take point 3
        point_3_x = h.landmark[self.mp_hands.HandLandmark.THUMB_IP].x
        point_3_y = h.landmark[self.mp_hands.HandLandmark.THUMB_IP].y

        #Index finger
        #Take point 5
        point_5_x = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].x
        point_5_y = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].y
        #Take point 6
        point_6_x = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP].x
        point_6_y = h.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP].y
        

        #Middle finger
        point_9_x = h.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
        point_9_y = h.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y

        #Ring finger
        point_13_x = h.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP].x
        point_13_y = h.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP].y

        #Pinky finger
        point_17_x = h.landmark[self.mp_hands.HandLandmark.PINKY_MCP].x
        point_17_y = h.landmark[self.mp_hands.HandLandmark.PINKY_MCP].y

        if point_17_y > point_13_y:
            if point_13_y > point_9_y:
                if point_9_y > point_5_y:
                    if point_4_x <= point_6_x and point_3_x >= point_5_x or point_4_x >= point_6_x and point_3_x >= point_5_x:
                        self.pause_counter += 1
