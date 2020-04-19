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
	## Create tkinter window object
        self.log_info("program opened at: {0} ".format(datetime.now()))
        
        ## Creating a TKINTER window
        self.window = tkinter.Tk()
        
        ## Changing the shape of the window
        self.window.geometry("1000x800")
        self.window.title("Slish")
        self.window.config(background='#c9e4ff')

        ## Creating camera object
        self.vid = Camera()
        self.success, self.background_image,_ = self.vid.capture_image()
        self.background_image = cv2.cvtColor(self.background_image, cv2.COLOR_BGR2GRAY)

	## Creating a classifier object
        self.classifier = Classifier()

        ## Creating a motion detection object
        self.checkformotion = Frame_Comparison()
        
        ## Creating variables used to keep track of predictions
        self.last_pred = None;
        self.recent_img = False
        self.frames_to_display_pred = 6
        self.show_pred = False
        self.pred_queue = deque([])
        self.sequence_of_gestures = [None,None]
        self.sequence_of_gestures_backup = [None,None]
        self.pred_queue_last_gesture = None
        self.recognized_sequence = False
        self.camera_status = self.vid.logStatus(True)
        
        ## Variables for timing the functions
        self.timing_list = set()
        self.time = {}

        ## Create mappings for plugs
        self.plug_mappings = {'C':'SLISH'}

	## Ccreate tkinter Frame and widgets
        self.header_frame= tkinter.Frame(self.window, bg='#c9e4ff')
        self.header_frame.pack(fill='x')
        self.middle_frame= tkinter.Frame(self.window)
        self.middle_frame.pack()
        self.stream_display= tkinter.Frame(self.middle_frame)
        self.stream_display.pack(fill='both')
        self.text_display= tkinter.Frame(self.middle_frame)
        self.text_display.pack(fill='both')
        self.btn =ttk.Button(self.header_frame, text='HELP', command=self.open_help)
        self.btn.pack(padx=10, pady=10, side='bottom')

        ## Create tkinter log/logo
        self.log_frame= tkinter.Frame(self.window, padx=5, pady=5, borderwidth=2, bg='#c9e4ff')
        self.log_frame.pack(side='bottom', fill='both')
        self.logBtn_frame=tkinter.Frame(self.log_frame,padx=5,pady=5,borderwidth=2, bg='#c9e4ff')
        self.logBtn_frame.pack(side='top', fill='y')
        self.btn2 =ttk.Button(self.logBtn_frame, text='Clear Log', command = self.clear_log)
        self.btn2.grid(row=0,column=0,padx=2, pady=2)
        self.btn3 =ttk.Button(self.logBtn_frame, text = 'Save Log', command = self.save) 
        self.btn3.grid(row=0,column=1, pady = 2, padx = 2)
        self.log=tkinter.Text(self.log_frame)
        self.S = tkinter.Scrollbar(self.log_frame)
        self.S.config(command=self.log.yview)
        self.S.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.logo = ImageTk.PhotoImage(Image.open('pic.png'))
        self.label = tkinter.Label(self.header_frame, image=self.logo)
        self.label.image= self.logo
        self.label.pack(padx=5, pady=5)
        
        self.fps_text_label = tkinter.Label(self.text_display,text="FPS ->", padx=10, pady=10, bg='#c9e4ff')
        self.fps_text_label.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.fps_text = tkinter.Label(self.text_display,text="None", padx=10, pady=10)
        self.fps_text.grid(row=0, column=1, padx=1, pady=1)
        
        self.last_gesture_label = tkinter.Label(self.text_display,text="Gesture ->", padx=10, pady=10, bg='#c9e4ff')
        self.last_gesture_label.grid(row=0, column=2, padx=10, pady=10,sticky='nsew')
        self.last_gesture = tkinter.Label(self.text_display,text="None", padx=10, pady=10)
        self.last_gesture.grid(row=0, column=3, padx=1, pady=1)

        self.last_sequence_of_gestures_label = tkinter.Label(self.text_display, text="Sequence of Gestures ->", padx=10, pady=10, bg='#c9e4ff')
        self.last_sequence_of_gestures_label.grid(row=1, column=0, padx=10, pady=10,sticky='nsew')
        self.last_sequence_of_gestures = tkinter.Label(self.text_display, text="None", padx=10, pady=10)
        self.last_sequence_of_gestures.grid(row=1, column=1, padx=1, pady=1)

        self.last_command_label = tkinter.Label(self.text_display,text="Command ->", padx=10, pady=10, bg='#c9e4ff')
        self.last_command_label.grid(row=1, column=2, padx=10, pady=10,sticky='nsew')
        self.last_command = tkinter.Label(self.text_display, text="None", padx=10, pady=10)
        self.last_command.grid(row=1, column=3, padx=1, pady=1)

        ## Creating text output fields
        self.display_image_bool = tkinter.IntVar()
        self.display_image = tkinter.Checkbutton(self.stream_display, text="Display Camera Feed",variable=self.display_image_bool, padx=10, pady=10, bg='#568c96')
        self.display_image.grid(row=0, column=0, padx=10, pady=10)
        self.display_classified_image_bool = tkinter.IntVar()
        self.display_classified_image = tkinter.Checkbutton(self.stream_display, text="Display Classified Feed",variable=self.display_classified_image_bool, padx=10, pady=10, bg='#568c96')
        self.display_classified_image.grid(row=0, column=1, padx=10, pady=10)
        self.stream_display.grid_columnconfigure(0, weight=1)
        self.stream_display.grid_columnconfigure(1, weight=1)
        self.sequence_of_gestures_backup = []        

        ## Updating the log with entries
        self.displayProgramAction(self.camera_status)
        self.displayProgramAction(self.camera_status)
        self.window.protocol("WM_DELETE_WINDOW", self.displayProgramClosing)
        self.recently_executed = False

        ## Begin main loop
        self.ten_sec_window = 0
        self.delay = 5
        self.update()
        self.window.mainloop()

    ## Function to open help document on github    
    def open_help(self): 
        webbrowser.open('https://github.com/mjp1997/ASL-Controlled-Smart-Home-Environment/blob/master/help.txt')
        # button that calls open_help()

    ## Clears the log history
    def clear_log(self):
        f = open('logHistory.txt', 'r+')
        f.truncate(0)

    ## Saves the logHistory as a copy
    def save(self): 
        new_file = open("LogHistoryCopy.txt", "w")
        with open("LogHistory.txt", "r") as f:
            new_file.write(f.read())
        new_file.close()

    ## Reads the log history from the text file named logHistory.txt
    def displayProgramAction(self, cam_is_open):
        if cam_is_open:
            with open('logHistory.txt','r') as file_data:
                history = list(file_data)
                for x in history:
                    self.log.insert(tkinter.INSERT, x)
                self.log.config(state='disabled',width=640)
                self.log.pack(fill='x')
        else:
            self.log.insert(tkinter.INSERT, "{0}".format(history))

    ## Writes log history to the log widget
    def displayProgramClosing(self):
        current_time = datetime.now()
        file = open('logHistory.txt', 'a')
        file.write('=========================================\n')
        file.write("program closed at: {0} ".format(current_time) + '\n')
        file.close()
        self.log.insert(tkinter.INSERT, "=========================================\n'")
        self.log.insert(tkinter.INSERT, "program closed at: {0} ".format(current_time))
        self.window.destroy()

    ## The update function that is called each iteration
    def update(self):
        #@ Success means that a valid image came back as the image will be an array and will not equal None
        success, frame, no_background = self.vid.capture_image()
        self.modif_frame = self.checkformotion.processCurrentFrame(frame)
        self.frame_difference = self.checkformotion.subtractFrames(self.modif_frame, self.background_image)
        
	## Quantify the number of pixels that have changed
        changedPixels = self.checkformotion.checkPixelDiff(self.frame_difference)
        
	## Quanity the total number of pixels
        totalPixels = self.checkformotion.getNumPixels(self.background_image)

        ## Wasn't enough movement
        if changedPixels/totalPixels < .10:
            self.window.after(self.delay, self.update)
        ## Program will continue past this section if the threshold is met        

        ## If there has been a recent classified image and doesnt need to run
        if self.recent_image():
            self.window.after(self.delay, self.update)

        ## We need to reclassify an image
        else:
            ##pred = self.classifier.classify(no_background)

            ## Classify the frame from the camera
            pred = self.classifier.classify(frame)

            ## We process the prediction queue
            self.processPred(pred)

            ## Display images if needed based on checkbuttons
            if self.display_image_bool.get() == 1:
                cv2.imshow("Camera Image",frame)
            if self.display_classified_image_bool.get() == 1:
                cv2.imshow("Classified Image",no_background)

            ## Update text fields
            self.fps_text.config(text=self.vid.getFPS())
            self.last_command.config(text="WE NEED TO INSERT LAST COMMAND")
            self.last_sequence_of_gestures.config(text=str(self.sequence_of_gestures_backup[0])+" : "+str(self.sequence_of_gestures_backup[1]))
            self.last_gesture.config(text=self.pred_queue_last_gesture)

            self.window.after(self.delay, self.update)

            
#frames are classified and the classification is sent to a queue > 60% = valid cmd
    
    ## This method takes a prediction and pushes it to the queue
    def processPred(self,pred):
        ## If the queue is 6 then its full
        if len(self.pred_queue) == 6:
            print(self.pred_queue)
            ## res is the highest percentage item in the queue and the if statement will run if that percentage is over .6
            res = Counter(self.pred_queue).most_common(1)

            ## If res percentage is .6 and it is not None
            if res[0][1]/6 > .6 and res[0][0] != None:
                self.pred_queue_last_gesture = res[0][0]
                self.cmd_execution_time = time.time()                
                ## This will push the gesture to the gesture list as a gesture has been recognized
                self.processQueue(res[0][0])
                
            ## The most common item in the pred queue is None clear and reset the queue variables
            elif res[0][0] == None:
                self.last_pred = None;
                self.frames_to_display_pred = 6
                self.show_pred = False
                self.pred_queue = deque([])
                #only clear gesture queue if the user's been given 10 secs to provide a valid gesture
                if len(self.sequence_of_gestures) > 0 and time.time() - self.ten_sec_window > 10: 					
                    self.sequence_of_gestures = []
                    self.recognized_sequence = False
					
                
            ## The gesture isnt recognized so we pop and push a new prediction
            else:
                self.pred_queue.popleft()
                self.pred_queue.append(pred)
                
        ## The queue isnt full so we push the prediction
        else:
            self.pred_queue.append(pred)
            if len(self.sequence_of_gestures_backup) == 0:
                self.sequence_of_gestures_backup = [None,None]
            
    ## Processing the queue means that we have 2 items in the gesture queue so we want to see if they map to something
    def processQueue(self, label):
        ## The pred queue needs to be reset
        self.pred_queue *= 0 #clear pred_queue
        self.last_pred = label
        ## We will push the gesture and if there are 2 items in the list then we will need to process it and find the mapping.
        if self.last_pred.isalpha() and len(self.sequence_of_gestures) == 0: #assures 1st gesture is alphabetic
            self.sequence_of_gestures.append(label)
            self.ten_sec_window = time.time()
            print(self.sequence_of_gestures)

        elif self.last_pred.isnumeric() and len(self.sequence_of_gestures) ==1:#assures 2nd gesture is numeric
            self.sequence_of_gestures.append(label)
        else:
            pass #simply keep looking for more gestures

        ## We need to show the prediction for 6 frames
        self.show_pred = True
        self.frames_to_display_pred = 6
        self.recognized_sequence = True  #if it's being processed isn't it recognized?

        ## If the gestures list is more than 2 we need to clear it
        if len(self.sequence_of_gestures) > 1:
            self.sequence_of_gestures_backup =list(self.sequence_of_gestures)
            if self.sequence_of_gestures[0] in self.plug_mappings.keys():
                ges = list(self.plug_mappings.keys())[0]
                plug = Socket(self.plug_mappings[ges])
                second = self.sequence_of_gestures[1]
                if second == '1':
                    print('plug turned on')
                if second == '2':
                    print('plug turned off')
            self.sequence_of_gestures *= 0
            self.recently_executed = True

            



    ## Chcecks to see if we have classified a recent image
    def recent_image(self):
        if(self.recently_executed and time.time() - self.cmd_execution_time < 1):
            return True
        else:
            self.recently_executed = False
            self.cmd_execution_time = 0
            return False


    def log_info(self,text):
        with open('logHistory.txt', 'a') as file:
            file.write(text+'\n')
      

    ## Used to time functions
    def add_start(self,string):
        self.time[string+"start"] = time.time()
        self.timing_list.add(string)

    ## Used to time functions
    def add_stop(self,string):
        self.time[string+"stop"] = time.time()
        self.timing_list.add(string)

    ## Used to time functions
    def get_times(self):
        for x in self.timing_list:
            print(str(x)+" = "+str(self.time[str(x)+"stop"]-self.time[str(x)+"start"]))


#beginning of program
Slish()
