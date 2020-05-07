"""
MOTION DETECTION FEATURE

CONTRIBUTORS:
    Mitchell Perez

FILE CONTENT DESCRIPTION:
The contents of this file are used by SLISH to discern whether external motion was detected by the camera within the 
previous minute. If not, motion_detection.py indicates to SLISH that the system must enter
"sleep mode" where the system does not attempt to classify external camera frames until
motion is once again detected. The overall purpose of this file is to lessen the processing power that SLISH utilizes
in addition to making the software more usable. 
REQUIREMENTS ADDRESSED IN SRS:
   NFR.6

CORRESPONING SDD SECTIONS:
Processing detail for each operation of Camera Frame Retrieval Component - 3.2.3.5.A

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
import cv2
import numpy as np
import time
import imutils




class Frame_Comparison():
    def __init__(self):
        self.execution_time = time.time()
    
    def processCurrentFrame(self, current_frame):
        # self.current_frame = cv2.resize(current_frame, (400, 266), interpolation=cv2.INTER_AREA)
        self.current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        self.current_frame = cv2.GaussianBlur(self.current_frame, (21, 21), 0)
        return self.current_frame

    def checkPixelDiff(self, img_disparity):
		#take the absolute value of the corresponding pixel disparities
        self.dissimilar_pixels = np.count_nonzero(self.img_disparity)
        return self.dissimilar_pixels

    def subtractFrames(self, current_frame, background):
        self.img_disparity = cv2.absdiff(background, self.current_frame)
        return self.img_disparity
    
    def boundingBox(self, img_disparity, frame):
        self.change_threshold = self.setChangeThreshold(self.img_disparity)
        contour_count = self.getContours(self.change_threshold)
        for contour in contour_count:
            # print(cv2.contourArea(contour))
            # <----- critera for valid bounding box contours ------>
            if cv2.contourArea(contour) < 600:
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			# 	return dissimilar_pixels
		# return self.dissimilar_pixels

    def setChangeThreshold(self, img_disparity):
        #turns the areas where motion is detected completely white, allowing for easier motion detection
        change_threshold = cv2.threshold(img_disparity, 25, 255, cv2.THRESH_BINARY)[1]
        change_threshold = cv2.dilate(change_threshold, None, iterations=2)
        return change_threshold
    
    def getContours(self, threshold):
        contours = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        return contours

    def getNumPixels(self, background):
        height, width = background.shape[:2]
        return height * width
