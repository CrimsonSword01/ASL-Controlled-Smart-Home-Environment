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
