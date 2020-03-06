'''
This module contains the Camera class for the SLISH application
'''
import time
import cv2
import numpy as np
import traceback
from status_log import *
import keyboard
import pathlib
import pathlib
from sys import platform
import sys
# The camera class allows streaming and image capturing from a usb/integrated camera on the system.
class Camera:

    def __init__(self):
        self.capture = self.getCamera()
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter('output.avid', self.fourcc, 20.0,
                      (640, 480))  # size of screen

        self.img_count = 0 # keep track of number of images saved
        self.gestures_per_second = self.set_gestures_per_second(1) # number of a gestures a second to be processed
        self.path = '../image_gathering/'  # folder files are being saved to
        self.gestures_per_second_time_check = time.time() # Used to determine if a gesture needs to be captured and processed
        self.last_second_duration = 0
        self.prior_total = 0 # Used to keep track of the last second's number of frames
        self.current_total = 0 # Used to keep track of the current second's number of frames
        self.begin_time = time.time()

        self.capturing_video = True
    # Checks to see if frame needs to be saved and saves items
    def save_image(self,frame):
        if time.time() - self.begin_time >= 3:  # if it's been 3 seconds since the last image was taken    
            img_name = self.path + "opencv_frame_{}.png".format(str(time.time()))
            cv2.imwrite(img_name, frame)
			
    # Closes the camera
    def close(self):
        self.capture.release()
        self.out.release()
        cv2.destroyAllWindows()
    # Checks to see if a gesture needs to be processed
    def gesture_check(self):
        if time.time() - self.gestures_per_second_time_check > self.gestures_per_second:
            return True
        return False
        
    # Returns one frame to the SLISH application
    def capture_image(self):
        # Sees if the FPS needs to be updated
        self.update_fps()
        ret, frame = self.capture.read()  # retrieving the video frame
        frame = self.write_text(frame,"FPS :" + str(self.prior_total), 50,50, cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255))
        # self.save_image(frame)
        cv2.imshow('frame', frame)  # displaying the frame
        return frame
    # Uupdates the FPS if necessary
    def update_fps(self):
        self.current_total +=1
        print('update fps')
        # Sees if its been one seconds since FPS has been updated
        if time.time() - self.last_second_duration > 1:
            if self.last_second_duration != 0:
    	        self.prior_total = self.current_total # Updates the prior seconds total
    	        self.current_total = 0 # Sets the new seconds total to 0
            self.last_second_duration = time.time() # Starts the new second

    # Writes text to image
    def write_text(self,frame,text,x,y,font,size,color):
        return cv2.putText(frame, text, (x,y), font, size, color)
        

    # Sets the number of gestures per second
    def set_gestures_per_second(self,ges):
        return (60/ges)/1000
        
    def getCamera(self):
        ## Checks to see what operating system is being ran and knows if its a linux so the camera is created correctly
        if platform == "linux" or platform == "linux2":
            return cv2.VideoCapture(0)  # create video object
        else:
            print('test')
            print('displaying camera')
            return cv2.VideoCapture(0)  # create video object
