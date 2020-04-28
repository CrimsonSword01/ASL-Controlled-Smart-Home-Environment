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
	NFR.9
	EIR.2
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

"""[Reference 'deprecated_socket.py' for the full socket class (if we were to 
implement the actual socket]"""


