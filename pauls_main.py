import time
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

from my_sock.sock import Socket
from model_handler.classifier import Classifier
from camera_stream.camera import Camera

class Slish:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.geometry("1000x800")
        self.window.title("Slish")
        self.vid = Camera()
        self.classifier = Classifier()
        self.pred_queue = deque([])
        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(self.window, width = 640, height = 480)
        self.canvas.pack()
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 1
        self.update()
        self.window.mainloop()
        
 
    def update(self):
        # we need success
        success, frame = self.vid.capture_image()
        if success:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        pred = self.classifier.classify(frame)
        self.processPred(pred)
        self.window.after(self.delay, self.update)

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
            
    def processQueue(self, label):

        print(self.pred_queue)
        
        self.pred_queue.clear()
        print("OH MY GOSH IT WORKED")

        
 

#beginning of program
Slish()
