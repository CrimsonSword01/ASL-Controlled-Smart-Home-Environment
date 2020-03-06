import time
import cv2
import numpy as np
import traceback
from status_log import *
import keyboard
import pathlib
from sys import platform
import sys

class Sockets:

    def __init__(self):
		self.commandsDict = {
			"A": "PortNumXXXXX", #placeholder for actual socket port
		    "B": "PortNumYYYYY"
		}

	# def validCmdCheck(self, cmd)
	# 	cmd in self.commandsDict.values() == true:
	# 		self.portAvail = isPortFree(commandsDict[cmd])
	# 	    self.activateSocket(commandsDict[cmd], self.portAvail)
    
    # def isPortFree(self, portNum):
	# 	#if port is free return true, else false
	# 	return True 

	# def activateSocket(self, portNum):
	# 	placeholderOutputMsg = 'Connecting to port: ' + portNum
	# 	return placeholderOutputMsg

