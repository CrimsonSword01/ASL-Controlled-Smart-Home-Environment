import cv2
import numpy as np
import time





class Frame_Comparison():
    def __init__(self):
        self.execution_time = time.time()
    
    def compareImgs(self, background, current_frame):
        self.current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        self.img_disparity = cv2.absdiff(background, self.current_frame)
        self.dissimilar_pixels = np.count_nonzero(self.img_disparity)
        cv2.imshow("test", self.img_disparity)
        return self.dissimilar_pixels

    def getNumPixels(self, background):
        height, width = background.shape[:2]
        return height * width
		