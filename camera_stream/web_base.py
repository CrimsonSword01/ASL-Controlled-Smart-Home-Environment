import time
import cv2
import numpy as numpy
import time
import traceback
from status_log import *

video = cv2.VideoCapture(0)  # create video object
# recorded video is created into avi files
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avid', fourcc, 20.0, (640, 480))

text = ''


def displayFrame():
    print('opening program')
    logStatus('opening')
    img_counter = 0
    beginTime = time.time()
    path = 'ImageGathering/'
    while True:
        ret, frame = video.read()
        cv2.imshow('frame', frame)
        k = cv2.waitKey(1)
        distinguishPath = str(time.time())
        if time.time() - beginTime >= 3:
            logStatus('img')
            img_name = path + "opencv_frame_{}.png".format(distinguishPath)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            beginTime = time.time()
        if k % 256 == 27:
            print('closing program')
            logStatus('closing')
            video.release()
            cv2.destroyAllWindows()


displayFrame()
video.release()
out.release()
cv2.destroyAllWindows()
