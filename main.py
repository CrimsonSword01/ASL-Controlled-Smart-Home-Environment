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

sock_path = str(pathlib.Path('sock').parent.absolute())
sock_path = sock_path + '/my_sock'

sys.path += [cam_path, classifier_path, sock_path, interface_path]

#import the 4 core modules (camera, classifier, UI and sockets)
from camera import Camera
my_camera = Camera() 

from classifier import Classifier
my_classifier = Classifier()

from interface import UI
my_interface = UI()

from sock import Socket 
my_socket = Socket()

while my_camera.capture.isOpened():
    my_camera.capture_image() #erroring out (showing gray screen)....
#loop that detects and sends imgs to classifier
my_camera.close()



