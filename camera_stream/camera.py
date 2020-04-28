"""
CONTRIBUTORS:
    Mitchell Perez, Paul Durham, Omnia Awad

FILE CONTENT DESCRIPTION:
	The contents of the camera file are essential in retrieving the external camera feed that is to be processed by the 
	gesture classifier. Through utilization of methods from the cv2 and numpy libraries, the camera file 
	is responsible for capturing individual camera frames, calculating the frames per second at which the system is running, 
	and sending these aforementioned frames to the classifier when necessary. Additionally, SLISH is also repsonsible for 
	handling input to both Unix and Windows based operating systems as well as asserting that the required USB camera is being
	used to retrieve external input. 

REQUIREMENTS ADDRESSED:
    FR.1, 2.2 
	NFR.1, NFR.7
	EIR.1
LICENSE INFORMATION:
    Copyright (c) 2019, CSC 450 Group 1
    All rights reserved.
    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
    following conditions are met:
        * Redistributions of source code must retain the above copyright notice, this list of conditions and the
          following disclaimer.
        * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and
          the following disclaimer in the documentation and/or other materials provided with the distribution.
        * Neither the name of the CSC 450 Group 4 nor the names of its contributors may be used to endorse or
          promote products derived from this software without specific prior written permission.
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
    OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
    STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
    EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import time
import cv2
import numpy as np
import traceback
# from status_log import *
import keyboard
import pathlib
import pathlib
from sys import platform
import sys
import time
from datetime import datetime
from PIL import Image
current_time = datetime.now()


# The camera class allows streaming and image capturing from a usb/integrated camera on the system.
class Camera:

    def __init__(self):
        
        ### EDIT THIS VARIABLE TO CHANGE THE SPEED OF THE BACKGROUND REMOVER
        self.speed = .0005
        ### larger number = faster melting
        ### smaller number it will take longer
        
        print('camera')
        self.capture = self.getCamera()
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter('output.avid', self.fourcc, 20.0,
                      (640, 480))  # size of screen
        self.mask = None
        self.backSub = cv2.createBackgroundSubtractorMOG2()
        self.img_count = 0 # keep track of number of images saved
        self.gestures_per_second = self.set_gestures_per_second(1) # number of a gestures a second to be processed
        self.path = '../image_gathering/'  # folder files are being saved to
        self.gestures_per_second_time_check = time.time() # Used to determine if a gesture needs to be captured and processed
        self.last_second_duration = 0
        self.prior_total = 0 # Used to keep track of the last second's number of frames
        self.current_total = 0 # Used to keep track of the current second's number of frames
        self.begin_time = time.time()
        self.w = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.h = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print ("Camera resolution check:",self.w,self.h)

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
        # self.save_image(frame)

        self.mask = self.backSub.apply(frame,self.mask,self.speed)
        self.mask = cv2.merge((self.mask,self.mask,self.mask))
        dst = cv2.bitwise_and(self.mask,frame)
        
        return True,frame,dst
    # Uupdates the FPS if necessary
    def update_fps(self):
        self.current_total += 1
        # Sees if its been one seconds since FPS has been updated
        if time.time() - self.last_second_duration > 1:
            if self.last_second_duration != 0:
    	        self.prior_total = self.current_total # Updates the prior seconds total
    	        self.current_total = 0 # Sets the new seconds total to 0
            self.last_second_duration = time.time() # Starts the new second
    
	#log status function
    def logStatus(self, status):
        current_time = str(datetime.now())
        if status == True:  # if program is being opened, document that it's being opened
            print('writing to open')
            file = open('logHistory.txt', 'a')
            file.write('=========================================\n')
            file.write('program opened at: ' + current_time + '\n')
            file.close()
            return True
        elif status == 'closing':  # if program is being closed, document that it's being closed
            file = open('logHistory.txt', 'a')
            file.write('program closed at: ' + current_time + ', ' + str(numImgs) +' images recorded'+ '\n')
            file.close()
        elif status == 'clear':
            file = open('logHistory.txt', 'w')
            file.write('program cleared at: ' + current_time + '\n')
            file.close()
        else:
            print(status)
            print('invalid input')

    # Writes text to image
    def write_text(self,frame,text,x,y,font,size,color):
        return cv2.putText(frame, text, (x,y), font, size, color)
        

    # Sets the number of gestures per second
    def set_gestures_per_second(self,ges):
        return (60/ges)/1000

	#retrieve camera feed    
    def getCamera(self):
        ## Checks to see what operating system is being ran and knows if its a linux so the camera is created correctly
        if platform == "linux" or platform == "linux2":
            return cv2.VideoCapture(0)  # create video object
        else:
            return cv2.VideoCapture(0)  # create video object

    # returns FPS
    def getFPS(self):
        return self.prior_total
