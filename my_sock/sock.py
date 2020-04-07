import time                 # I dont think we need these for the class
import cv2                  # I dont think we need these for the class
import numpy as np          # I dont think we need these for the class
import traceback            # I dont think we need these for the class
# from status_log import *  # I dont think we need these for the class
import keyboard             # I dont think we need these for the class
import pathlib              # I dont think we need these for the class 
from sys import platform    # I dont think we need these for the class
import sys                  # I dont think we need these for the class
from pyHS100 import Discover as ds
from pyHS100 import SmartPlug, SmartBulb

class Socket:
    def __init__(self,name):
        print("\n\n\nCREATING PLUG\n\n\n")
        dev_ip = None
        for dev in ds.discover().values():
            if dev.alias.lower() == name: # <--- need the hard code the name of the plug to find IP
                dev_ip = dev.host
                break
        #checking if we are finding the IP address
        self.plug = SmartPlug(dev_ip)
    #confused what is going on here
    def validCmdCheck(self, cmd):
        cmd in self.commandsDict.values()
        self.portAvail = isPortFree(commandsDict[cmd])
        self.activateSocket(commandsDict[cmd], self.portAvail)

    def turn_on(self):
        self.plug.turn_on()
        print("TURNED ON")
    def turn_off(self):
        self.plug.turn_off()
        print("TURNED off")

    def status(self):
        #asking the user if they want the plug to turn or off
        #this would be changed to tell the user at the start of the program 
        self.state = input("Is the plug suppose to be on or off")
        #hopefully i dont have to comment on this
        #also this would be changes with the multipul other commands that we will have for this project
        if state.lower() == "on":
            self.plug.turn_on()
            print("current status of "+ self.plug.state)
        #hopefully i dont have to comment on this x2
        elif state.lower() == "off":
            self.plug.turn_off()
            print("current status of "+ self.plug.state)
        #hopefully i dont have to comment on this x3
        else:
            print("You have input the wrong status")

    #confused what is going on here
