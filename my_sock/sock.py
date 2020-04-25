"""
CONTRIBUTORS:
    Joseph Proctor

FILE CONTENT DESCRIPTION: 
    The contents of the socket.py is essential in retreiving the gesture taken from the classifier to turn on/off the WIFI plug.
    With using pyHS100 we were able to be able to discover the IP address using the naming feature that the app the plug uses.
    After getting the IP address we look for a gesture being found and with that we can turn on and off the plug 
    and output the status of the plug.

REQUIREMENTS ADDRESSED:
    FR.5
"""
from pyHS100 import Discover as ds
from pyHS100 import SmartPlug, SmartBulb

class Socket:
    def __init__(self,name):
        print("\n\n\nCREATING PLUG\n\n\n") # Showing that when a gesture is picked up being able to see that it works
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
        #also this would be changes with the multipule other commands that we will have for this project
        if self.state.lower() == "on":
            self.plug.turn_on()
            print("current status of "+ self.plug.state)
        elif self.state.lower() == "off":
            self.plug.turn_off()
            print("current status of "+ self.plug.state)
        #hopefully i dont have to comment on this x3
        else:
            print("You have input the wrong status")
