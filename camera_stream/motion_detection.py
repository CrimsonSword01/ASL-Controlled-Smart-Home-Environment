import cv2
import numpy as np
import time





class Frame_Comparison():
    def __init__(self):
        self.execution_time = time.time()
    
    def processCurrentFrame(self, current_frame):
        self.current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        self.current_frame = cv2.GaussianBlur(self.current_frame, (21, 21), 0)
        return self.current_frame

    def checkPixelDiff(self, current_frame, background):
		#take the absolute value of the corresponding pixel disparities
        self.img_disparity = cv2.absdiff(background, self.current_frame)
        self.dissimilar_pixels = np.count_nonzero(self.img_disparity)
        self.setChangeThreshold(self.img_disparity)
        return self.dissimilar_pixels

    def setChangeThreshold(self, img_disparity):
        #turns the areas where motion is detected completely white, allowing for easier motion detection
        change_threshold = cv2.threshold(img_disparity, 25, 255, cv2.THRESH_BINARY)[1]
        change_threshold = cv2.dilate(change_threshold, None, iterations=2)
        return change_threshold

    def getNumPixels(self, background):
        height, width = background.shape[:2]
        return height * width
