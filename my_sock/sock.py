"""
PLUG SIMULATOR COMPONENT

CONTRIBUTORS:
    Joseph Proctor, Mitchell Perez, Paul Durham

FILE CONTENT DESCRIPTION: 
    The following contents of sock.py consist of the necessary methods, attributes
	and algorithms to control the corresponding smart plug after a valid command is recognized.
	Though numerous features have been deprecated as a result of smart plug inaccessibility, the following
	methods are used to simulate the actions that would take place if the sockets were to be readily available. 
	
REQUIREMENTS ADDRESSED IN SRS:
    FR.5
	NFR.9
	EIR.2

CORRESPONDING SDD SECTIONS:
Processing Narrative for Plug Component - 3.2.1.D
Plug Object Interface Description - 3.2.2.D
Plug Component Processing Detail  - 3.2.3.D
Design Constraints for Plug Components - 3.2.3.4.D
Processing Detail for each operation of Plug Component - 3.2.3.5.D
Processing Narrative for each operation - 3.2.3.5.1.D
Algorithmic Model for each operation - 3.2.3.5.2.D
"""
"""LICENSE INFORMATION:
    Copyright (c) 2019, CSC 450 Group 1
    All rights reserved.
    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
    following conditions are met:
        * Redistributions of source code must retain the above copyright notice, this list of conditions and the
          following disclaimer.
        * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and
          the following disclaimer in the documentation and/or other materials provided with the distribution.
        * Neither the name of the CSC 450 Group 1 nor the names of its contributors may be used to endorse or
          promote products derived from this software without specific prior written permission.
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
    OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
    STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
    EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from pyHS100 import Discover as ds
from pyHS100 import SmartPlug, SmartBulb

class Socket:
    def __init__(self):
        self.plug_mappings = {'A': 'Fan', 'B' : 'Music', 'C': 'Lights'}
    #returns true if the gesture presented is valid
    def isGestureValid(self, gesture):
        if gesture in self.plug_mappings.keys():
            return True
        else: 
            return False
    #returns appliance that corresponds to the gesture presented
    def getAppliance(self, gesture):
        return self.plug_mappings[gesture]

"""[Reference 'deprecated_socket.py' for the full socket class (if we were to 
implement the actual socket]"""


