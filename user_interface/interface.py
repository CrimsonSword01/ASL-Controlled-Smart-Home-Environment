import time
import cv2
import numpy as np
import traceback
from status_log import *
import keyboard
import pathlib
from sys import platform
import sys

class UI:

	def __init__(self):
		self.load_user_interface()
		self.retrieveLogInfo()
	
	def load_user_interface(self):
		outputString = 'loading the user interface (placeholder)'
		return outputString

	def retrieveLogInfo(self):
		logString = 'retrieving log'
		return logString