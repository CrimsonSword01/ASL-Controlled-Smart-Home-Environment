import time
import cv2
import numpy as np
import time
import traceback  # importing necessary modules (Mitch)
import os
from threading import Timer

video = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))


text = ''


def displayFrame():
    img_counter = 0
    beginTime = time.time()
    path = 'ImageGathering/'
    while True:
        # after 30 seconds, "hello, world" will be printed
        ret, frame = video.read()
        cv2.imshow('frame', frame)  # show the frame
        k = cv2.waitKey(1)
        if time.time() - beginTime >= 3:  # if 3 seconds have elapsed since the last img's capture
            img_name = path + "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1  # assuring images are labeled differently....
            beginTime = time.time()

        if k % 256 == 27:  # if the user presses the 'esc' key, end the program
            print('test')
            video.release()
            cv2.destroyAllWindows()


displayFrame()

video.release()
out.release()
cv2.destroyAllWindows()
