"""
CONTRIBUTORS:
    Joseph Proctor, Mitchell Perez, Paul Durham

FILE CONTENT DESCRIPTION: 
    The following contents of sock.py consist of the necessary methods, attributes
	and algorithms to control the corresponding smart plug after a valid command is recognized.
	Though numerous features have been deprecated as a result of smart plug inaccessibility, the following
	methods are used to simulate the actions that would take place if the sockets were to be readily available. 
	
REQUIREMENTS ADDRESSED:
    FR.5
"""
from pyHS100 import Discover as ds
from pyHS100 import SmartPlug, SmartBulb

class Socket:
    def __init__(self):
        self.plug_mappings = {'A': 'Fan', 'B' : 'Music', 'C': 'Lights'}

    def isGestureValid(self, gesture):
        if gesture in self.plug_mappings.keys():
            return True
        else: 
            return False

    def getAppliance(self, gesture):
        return self.plug_mappings[gesture]

"""[Joseph's code] All code below is deprecated due to the inability to demo the sockets..."""
    # def turn_on(self):
    #     self.plug.turn_on()
    #     print("TURNED ON")
    # def turn_off(self):
    #     self.plug.turn_off()
    #     print("TURNED off")

    # def status(self):
    #     #asking the user if they want the plug to turn or off
    #     #this would be changed to tell the user at the start of the program 
    #     self.state = input("Is the plug suppose to be on or off")
    #     #hopefully i dont have to comment on this
    #     #also this would be changes with the multipule other commands that we will have for this project
    #     if self.state.lower() == "on":
    #         self.plug.turn_on()
    #         print("current status of "+ self.plug.state)
    #     elif self.state.lower() == "off":
    #         self.plug.turn_off()
    #         print("current status of "+ self.plug.state)
    #     #hopefully i dont have to comment on this x3
    #     else:
    #         print("You have input the wrong status")
