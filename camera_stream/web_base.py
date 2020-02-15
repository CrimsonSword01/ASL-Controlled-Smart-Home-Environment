
# EDIT BY PAUL DURHAM - SEE EDIT 1 - 2/10/2020 - edited path variable to work with linux
# EDIT BY PAUL DURHAM - SEE EDIT 2 - 2/14/2020 - added a FPS calculator 

import time
import cv2
import numpy as np
import traceback
from status_log import *
import keyboard
import pathlib
import sys
my_path = pathlib.Path('rec_test').parent.absolute()
my_path = str(my_path) + '/model_handler'
print(my_path)
sys.path.insert(0, my_path)
sys.path.append('../model_handler/')
import classifier

video = cv2.VideoCapture(0)  # create video object

# recorded video is created into avi files
# video file types (optional, if we ever need video for some reason)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avid', fourcc, 20.0,
                      (640, 480))  # size of screen

text = ''

def displayFrame():
    print('opening program')
    logStatus('opening', 0)  # documenting that the program was opened
    imgCount = 0
    beginTime = time.time()

    # EDIT 1
    # EDIT BY PAUL DURHAM ON 2/10/2020
    # Added '..' to beginning of path to allow proper pathing in linux
    path = '../image_gathering/'  # folder files are being saved to

    ## Creating classifier object
    gesture_recognizer = classifier.Classifier()

    # EDIT 2
    # EDIT BY PAUL DURHAM ON 2/14/2020
    # Created objects necessary to keep track of and display FPS
    ## Creating time object to keep track of FPS and int to keep track of number of frames shown
    one_second_duration = time.time()
    total = 0
    prior_total = 0
    while True:
        total = total + 1
        if time.time() - one_second_duration > 1:
            if one_second_duration != 0:
    	        prior_total = total
    	        total = 0
            one_second_duration = time.time()
        ret, frame = video.read()  # retrieving the video frame

	# EDIT 2
	# EDIT BY PAUL DURHAM ON 2/14/2020
        res = gesture_recognizer.classify(frame)
        if res != None:
            cv2.putText(frame, res, (200,300), cv2.FONT_HERSHEY_SIMPLEX, 5, (255,255,255), 2)	    
        cv2.putText(frame, "FPS : "+str(prior_total), (10,300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

        cv2.imshow('frame', frame)  # displaying the frame

        # if the user presses a key (i.e "escape" retrieve this action)
        k = cv2.waitKey(1)

        # get the time to make every image name unique
        distinguishPath = str(time.time())

        # if time.time() - beginTime >= 3:  # if it's been 3 seconds since the last image was taken
        imgCount = imgCount + 1 # log that an image was taken

        # format path name
        img_name = path + "opencv_frame_{}.png".format(distinguishPath)
        ##cv2.imwrite(img_name, frame)
        ##print("{} written!".format(img_name))
        img = cv2.imread(img_name)
        beginTime = time.time()
        if k % 256 == 27:  # if escape if pressed, close the program
            print('closing program')
            logStatus('closing', imgCount)  # log that the program was closed
            video.release()  # release video frames
            cv2.destroyAllWindows()  # close window
        if k % 256 == ord('c'):
            print('clearing log history')
            logStatus('clear', 0)


displayFrame()
video.release()
out.release()
cv2.destroyAllWindows()