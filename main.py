import time
import cv2
import numpy as np
import traceback
# from status_log import *
import keyboard
import pathlib
from sys import platform
import sys
my_path = pathlib.Path('camera').parent.absolute()
my_path = str(my_path) + '/camera_stream'
sys.path.insert(0, my_path)
sys.path.append('../camera_stream/')
print(sys.path)
from camera import Camera
my_camera = Camera() 

my_path = pathlib.Path('classifier').parent.absolute()
my_path = str(my_path) + '/model_handler'
sys.path.insert(0, my_path)
sys.path.append('../model_handler/')
print(sys.path)
from classifier import Classifier

my_classifier = Classifier()

while True: # in place of 1:1? 
	Img = my_camera.capture_image()
	if my_camera.gesture_check(Img):
		Res = my_classifier(Img)
		my_camera.capture_image
