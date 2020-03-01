import time
import cv2
import numpy as np
import traceback
# from status_log import *
import keyboard
import pathlib
from sys import platform
import sys

#set paths for the modules being imported
cam_path = str(pathlib.Path('camera').parent.absolute())
cam_path = cam_path + '/camera_stream'

classifier_path = str(pathlib.Path('classifier').parent.absolute())
classifier_path = classifier_path + '/model_handler'

interface_path = str(pathlib.Path('interface').parent.absolute())
interface_path = interface_path + '/user_interface'

socket_path = str(pathlib.Path('socket').parent.absolute())
socket_path = socket_path + '/sockets'

sys.path += [cam_path, classifier_path, interface_path, socket_path]

#import the 4 core modules (camera, classifier, UI and sockets)
from camera import Camera
my_camera = Camera() 

from classifier import Classifier
my_classifier = Classifier()

from interface import UI
my_interface = UI()

from socket import Sockets
my_socket = Sockets()

#loop that detects and sends imgs to classifier
while True: # in place of 1:1? 
	Img = my_camera.capture_image()
	if my_camera.gesture_check():
		Res = my_classifier.classify(Img)
		#will finish....



