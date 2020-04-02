'''
This module contains the Camera class for the SLISH application
'''
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
current_time = datetime.now()


# The camera class allows streaming and image capturing from a usb/integrated camera on the system.
class Camera:

    def __init__(self):
        print('camera')
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
        return True,frame
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


if __name__ == "__main__":
    sb = 'MOG2'
    if sb == 'MOG2':
        backSub = cv2.createBackgroundSubtractorMOG2()
    else:
        backSub = cv2.createBackgroundSubtractorKNN()
    capture = Camera()
    while True:
        ret, frame = capture.capture.read()
        if frame is None:
            break
        fgMask = backSub.apply(frame)
        

        
        cv2.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
        cv2.putText(frame, str(capture.capture.get(cv2.CAP_PROP_POS_FRAMES)), (15, 15),cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
        cv2.imshow('Frame', frame)
        cv2.imshow('FG Mask', fgMask)
        keyboard = cv2.waitKey(30)
        if keyboard == 'q' or keyboard == 27:
            break

def get_background():
    cap = Camera()
    first_iter = True
    result = None
    frame = None
    while True:
        ret, frame = cap.capture.read()
        if frame is None:
            break
        if first_iter:
            avg = np.float32(frame)
            first_iter = False
        cv2.accumulateWeighted(frame, avg, 0.005)
        result = cv2.convertScaleAbs(avg)
        cv2.imshow("result", result)
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break
        
    cv2.imwrite("result", result)
    cv2.imwrite("unmodified", frame)
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
