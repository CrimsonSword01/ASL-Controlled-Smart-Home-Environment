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
from camera_stream.motion_detection import Frame_Comparison


class Slish:
    def __init__(self):
	#create tkinter window object
        self.log_info("program opened at: {0} ".format(datetime.now()))
        ## Creating a TKINTER window
        self.window = tkinter.Tk()
        ## Changing the shape of the window
        self.window.geometry("1000x800")
        self.window.title("Slish")
        self.window.config(background='#c9e4ff')

		#create objects from the various class modules
        ## Creating camera object
        self.vid = Camera()
        self.success, self.background_image = self.vid.capture_image()
        self.background_image = cv2.cvtColor(self.background_image, cv2.COLOR_BGR2GRAY)
		## Creating a classifier object
        self.classifier = Classifier()
        self.checkformotion = Frame_Comparison()
        ## Creating variables used to keep track of predictions
        self.last_pred = None;
        self.frames_to_display_pred = 6
        self.show_pred = False
        self.pred_queue = deque([])
        self.sequence_of_gestures = []
        self.recognized_sequence = False
        self.camera_status = self.vid.logStatus(True)
        
        ## Variables for timing the functions
        self.timing_list = set()
        self.time = {}

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
	#display the last time SLISH was operated within the gui lo
	#update log with current use time 
        self.displayProgramAction(self.camera_status)
	#update log when user closes SLISH GUI
        self.displayProgramAction(self.camera_status)
        self.window.protocol("WM_DELETE_WINDOW", self.displayProgramClosing)
	#delay to prevent the code from blocking
        self.recently_executed = False
        self.delay = 5
        self.update()
        self.window.mainloop()
        #function that loads the SLISH use history into the log
        #button allowing the user to access help documentation within the github repo
        # self.logo = ImageTk0.PhotoImage(Image.open('pic.png'))
        # self.label = tkinter.Label(self.header_frame, image=self.logo)
        # self.label.image= self.logo
        # self.label.pack(padx=5, pady=5)
        # function that opens the help documentation link
        
    def open_help(self): 
        webbrowser.open('https://github.com/mjp1997/ASL-Controlled-Smart-Home-Environment/blob/master/help.txt')
        # button that calls open_help()

    def displayProgramAction(self, cam_is_open):
        if cam_is_open:
            with open('logHistory.txt','r') as file_data:
                history = list(file_data)
                for x in history:
                    self.log.insert(tkinter.INSERT, x)
                self.log.config(state='disabled',width=640)
                self.log.pack(fill='x')
        else:
            print(history)
            self.log.insert(tkinter.INSERT, "{0}".format(history))

    def displayProgramClosing(self):
        current_time = datetime.now()
        print('test 5')
        file = open('logHistory.txt', 'a')
        file.write('======\n')
        file.write("program closed at: {0} ".format(current_time) + '\n')
        file.close()
        self.log.insert(tkinter.INSERT, "======")
        self.log.insert(tkinter.INSERT, "program closed at: {0} ".format(current_time))
        self.window.destroy()

#retrieve video frame, send to classifier and then sent to queue
    def update(self):
        #@ Success means that a valid image came back as the image will be an array and will not equal None
        success, frame = self.vid.capture_image()
        changedPixels = self.checkformotion.compareImgs(self.background_image, frame)
        totalPixels = self.checkformotion.getNumPixels(self.background_image)
        # print(changedPixels)
        # print(changedPixels/totalPixels)
        if changedPixels/totalPixels < .10:
            sleep(20)
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
            self.window.after(self.delay, self.update)

        if self.recent_image():
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
            print('frame recently classified (< 5 secs), not classifying current frame')
            self.window.after(self.delay, self.update)
        else:
            print('no cmds recently executed, continuing to classify')
            pred = self.classifier.classify(frame)
            test = self.processPred(pred)
            frame = self.vid.write_text(frame,"FPS :" + str(self.vid.getFPS()), 50,50, cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255))
            if success:
                ## IF we need to display the pred
                if self.show_pred and self.frames_to_display_pred >= 0:
                    ## We are decreasing the number of frames we need to display this in
                    self.frames_to_display_pred -= 1
                    ## Adding text to the frame
                    frame = self.vid.write_text(frame,self.last_pred, 400,50, cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255))
                    ## If we need to show the gestures recognized
                    if self.recognized_sequence and len(self.sequence_of_gestures) == 2:
                        frame = self.vid.write_text(frame,self.sequence_of_gestures[0]+':'+self.sequence_of_gestures[1], 500,50, cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255))
                        self.log.insert(tkinter.INSERT, self.sequence_of_gestures[0]) 
					    # +") at: {0} ".format(datetime.now()))

                self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
                self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
            self.window.after(self.delay, self.update)

		
#frames are classified and the classification is sent to a queue > 60% = valid cmd

    ## This method takes a prediction and pushes it to hte queue
    def processPred(self,pred):
        ## If the queue is greater than 6 then its full
        if len(self.pred_queue) >= 6:
            ## res is the highest percentage item in the queue and the if statement will run if that percentage is over .6
            res = Counter(self.pred_queue).most_common(1)
            if res[0][1]/6 > .6 and res[0][0] != None:
                self.recently_executed = True
                self.cmd_execution_time = time.time()
                ## This will push the gesture to the gesture list as a gesture has been recognized
                self.processQueue(res[0][0])
            ## The most common item in the pred queue is None clear and reset the queue variables
            elif res[0][0] == None:
                self.last_pred = None;
                self.frames_to_display_pred = 6
                self.show_pred = False
                self.pred_queue = deque([])
                self.sequence_of_gestures = []
                self.recognized_sequence = False
            ## The gesture isnt recognized so we pop and push a new prediction
            else:
                self.pred_queue.popleft()
                self.pred_queue.append(pred)
        ## The queue isnt full so we push the prediction
        else:
            self.pred_queue.append(pred)


    #clear queue once the image has been detected        

    ## Processing the queue means that we have 2 items in the gesture queue so we want to see if they map to something
    def processQueue(self, label):
        print(self.pred_queue)
        ## The pred queue needs to be reste
        self.pred_queue.clear()
        self.last_pred = label
        ## We need to show the prediction for 6 frames
        self.show_pred = True
        self.frames_to_display_pred = 6
        ## If the gestures list is more than 2 we need to clear it
        if len(self.sequence_of_gestures) >=2:
            self.sequence_of_gestures.clear()
        ## We will push the gesture and if there are 2 items in the list then we will need to process it and find the mapping.
        self.sequence_of_gestures.append(label)
        if len(self.sequence_of_gestures) <= 1:
            self.recognized_sequence = True
    
    def recent_image(self):
        if(self.recently_executed and time.time() - self.cmd_execution_time < 5):
            return True
        else:
            print('img not recently detected')
            self.recently_executed = False
            self.cmd_execution_time = 0
            return False


    def log_info(self,text):
        with open('logHistory.txt', 'a') as file:
            file.write(text+'\n')
      

    def add_start(self,string):
        self.time[string+"start"] = time.time()
        self.timing_list.add(string)

    def add_stop(self,string):
        self.time[string+"stop"] = time.time()
        self.timing_list.add(string)

    def get_times(self):
        for x in self.timing_list:
            print(str(x)+" = "+str(self.time[str(x)+"stop"]-self.time[str(x)+"start"]))


#beginning of program
Slish()
