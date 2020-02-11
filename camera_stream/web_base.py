


# EDIT BY PAUL DURHAM - SEE EDIT 1 - 2/10/2020

import time
import cv2
import numpy as numpy
import time
import traceback
from status_log import *

video = cv2.VideoCapture(0)  # create video object
# recorded video is created into avi files
# video file types (optional, if we ever need video for some reason)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avid', fourcc, 20.0,
                      (640, 480))  # size of screen

text = ''


def displayFrame():
    print('opening program')
    logStatus('opening')  # documenting that the program was opened
    img_counter = 0
    beginTime = time.time()
    # EDIT 1
    # EDIT BY PAUL DURHAM ON 2/10/2020
    # Added '..' to beginning of path to allow proper pathing in linux
    path = '../ImageGathering/'  # folder files are being saved to
    while True:
        ret, frame = video.read()  # retrieving the video frame
        cv2.imshow('frame', frame)  # displaying the frame
        # if the user presses a key (i.e "escape" retrieve this action)
        k = cv2.waitKey(1)
        # get the time to make every image name unique
        distinguishPath = str(time.time())
        if time.time() - beginTime >= 3:  # if it's been 3 seconds since the last image was taken
            logStatus('img')  # log that an image was taken
            # format path name
            img_name = path + "opencv_frame_{}.png".format(distinguishPath)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            beginTime = time.time()
        if k % 256 == 27:  # if escape if pressed, close the program
            print('closing program')
            logStatus('closing')  # log that the program was closed
            video.release()  # release video frames
            cv2.destroyAllWindows()  # close window


displayFrame()
video.release()
out.release()
cv2.destroyAllWindows()
