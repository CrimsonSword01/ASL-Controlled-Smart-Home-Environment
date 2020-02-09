import time
import cv2
import numpy as np
import time
import traceback  # importing necessary modules (Mitch)
from threading import Timer

video = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))


def hello():
    print("hello, world")


img_counter = 0
while True:
    # after 30 seconds, "hello, world" will be printed
    ret, frame = video.read()
    cv2.imshow('frame', frame)  # show the frame
    k = cv2.waitKey(1)

    if k % 256 == 32:
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

    if k % 256 == 27:  # if the key pressed = 'q' break loop
        video.release()
        cv2.destroyAllWindows()
        break


video.release()
out.release()
cv2.destroyAllWindows()
