import time
import webbrowser
import cv2
import numpy as np
import traceback
import tkinter as tkinter
# from status_log import *
import keyboard
import pathlib
from sys import platform
import sys
from tkinter import *
from multiprocessing import Process
from tkinter import *
from PIL import Image, ImageTk#from PIL import ImageTk
from threading import Thread
import time
import PIL.Image, PIL.ImageTk
from collections import deque, Counter  
try:
    from tkinter import ttk   
except ImportError:
    from tkinter import ttk
import time
from datetime import datetime
from my_sock.sock import Socket
from model_handler.classifier import Classifier
from camera_stream.camera import Camera

class Slish:
    def __init__(self):
		#create tkinter window object
        self.window = tkinter.Tk()
        self.window.geometry("1000x800")
        self.window.title("Slish")
        self.window.config(background='#c9e4ff')

		#create objects from the various class modules
        self.vid = Camera()
        self.classifier = Classifier()

        self.pred_queue = deque([])
        self.camera_status = self.vid.logStatus(True)
        
		#create frame 
        self.header_frame= tkinter.Frame(self.window,bg='#c9e4ff')
        self.header_frame.pack(fill='x')
        self.btn =ttk.Button(self.header_frame, text='HELP', command=self.open_help)
        self.btn.pack(padx=1, pady=1, side='bottom')

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(self.window, width = 640, height = 400)
        self.canvas.pack(padx=10, pady=10, side='top')

        #create tkinter log/logo
        self.log_frame= tkinter.Frame(self.window, padx=5, pady=5, borderwidth=2)
        self.log_frame.pack(side='left', fill='both')
        self.log=tkinter.Text(self.log_frame)
        self.logo = ImageTk.PhotoImage(Image.open('pic.png'))
        self.label = tkinter.Label(self.header_frame, image=self.logo)
        self.label.image= self.logo
        self.label.pack(padx=5, pady=5)

		#display the last time SLISH was operated within the gui log
        self.loadLogHistory()
		
		#update log with current use time 
        self.displayProgramAction(self.camera_status, None)
		#update log when user closes SLISH GUI
        self.window.protocol("WM_DELETE_WINDOW", self.displayProgramClosing)

		#delay to prevent the code from blocking
        self.delay = 5
        self.update()
        self.window.mainloop()

        #function that loads the SLISH use history into the log
    def loadLogHistory(self):
        file = open('logHistory.txt', 'r')
        file = file.readlines()
        print('entering')
        self.displayProgramAction(False, file[len(file) -5])
        self.displayProgramAction(False, file[len(file) -4])
        self.displayProgramAction(False, file[len(file) -3])
        self.displayProgramAction(False, file[len(file) -2])


#button allowing the user to access help documentation within the github repo
    def open_help(self): 
        webbrowser.open('https://github.com/mjp1997/ASL-Controlled-Smart-Home-Environment/blob/master/help.txt')
        # button that calls open_help()

#Display the action being executed (will be finished once model is optimized)
    def displayProgramAction(self, cam_is_open, history):
        if cam_is_open:
            current_time = datetime.now()
            self.log.insert(tkinter.INSERT, "program opened at: {0} ".format(current_time))
            self.log.config(state='disabled',width=640)
            self.log.pack(fill='x')
        else:
            print(history)
            self.log.insert(tkinter.INSERT, "{0}".format(history))

    def displayProgramClosing(self):
        current_time = datetime.now()
        print('test 5')
        file = open('logHistory.txt', 'a')
        file.write('=========================================\n')
        file.write("program closed at: {0} ".format(current_time) + '\n')
        file.close()
        self.log.insert(tkinter.INSERT, "==================================")
        self.log.insert(tkinter.INSERT, "program closed at: {0} ".format(current_time))
        self.window.destroy()

#retrieve video frame, send to classifier and then sent to queue
    def update(self):
        success, frame = self.vid.capture_image()
        if success:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        pred = self.classifier.classify(frame)
        test = self.processPred(pred)
        self.window.after(self.delay, self.update)
		
#frames are classified and the classification is sent to a queue > 60% = valid cmd
    def processPred(self,pred):
        if len(self.pred_queue) >= 6:
            res = Counter(self.pred_queue).most_common(1)
            if res[0][1]/6 > .6 and res[0][0] != None:
               self.processQueue(res[0][0]) 
            else:
                self.pred_queue.popleft()
                self.pred_queue.append(pred)
        else:
            self.pred_queue.append(pred)

    #clear queue once the image has been detected        
    def processQueue(self, label):
        print(self.pred_queue)
        self.pred_queue.clear()
        print("OH MY GOSH IT WORKED")

#beginning of program
Slish()
