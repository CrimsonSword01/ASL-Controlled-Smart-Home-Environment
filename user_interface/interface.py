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
		self.logInfo = self.retrieveLogInfo()
		self.writeLogToUI(self.logInfo)
	
	def load_user_interface(self):
		print('loading the user interface (placeholder)')
		

	def retrieveLogInfo(self):
		logString = 'simulation of updated log'
		return logString
    
	def writeLogToUI(self, logInfo):
		print('updated log: {}'.format(logInfo))
		print('display log to UI here...')