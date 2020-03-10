import time
import cv2
import numpy as np
import traceback
import tkinter as tk
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
try:
    from tkinter import ttk   
except ImportError:
    from tkinter import ttk

from my_sock.sock import Socket
from model_handler.classifier import Classifier
from camera_stream.camera import Camera


class SLISH(Frame):
    def __init__(self):
        Frame.__init__(self)
        #parent frame 
        self.master.title('SLISH')
        mainframe= Frame(self.master, bg='#c9e4ff')
        mainframe.pack(fill='both', expand=True)
        #Full screen window 
        self.master.geometry("{0}x{1}+1+1".format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        
        # displaying the title/logo of SLISH
        header_frame= Frame(mainframe,bg='#c9e4ff')
        header_frame.pack(fill='x')
        # photo = ImageTk.PhotoImage(Image.open('pic.png'))
        # label = Label(header_frame, image=photo)
        # label.image= photo
        # label.pack(padx=5, pady=5)
        
        # horizontal frame for camera stream and log
        center_frame= Frame(mainframe)
        center_frame.pack(fill='both')
        center_frame.grid_columnconfigure(0,weight=1)
        center_frame.grid_columnconfigure(1,weight=1)

        #space for camera_stream
        camera_frame= Frame(center_frame, padx=5, pady=5, borderwidth=2,bg='#c9e4ff')
        camera_frame.grid(row=0,column=0, sticky='nsew')
        #fill in code for video stream
        btn2 =Button(camera_frame, text='camera space to be filled later',padx=1, pady=1, width=40, height=35)
        btn2.pack( padx=2, pady=2, fill='both')

        #space for log
        log_frame= Frame(center_frame, padx=5, pady=5, borderwidth=2,bg='#c9e4ff')
        log_frame.grid(row=0,column=1, sticky='nsew')
        #fill in code 
        btn3 =Button(log_frame, text='log space to be filled later', width=40, height=20)
        btn3.pack(padx=2, pady=2, fill='both')
        self.my_camera = Camera()
        self.my_socket = Socket()
        self.my_classifier = Classifier()
        # self.displayFrame()gi
        # function that opens the help documentation link
        def open_help():
            webbrowser.open('https://github.com/mjp1997/ASL-Controlled-Smart-Home-Environment/blob/master/help.txt')
        
        #FPS space
        btn4 =Button(log_frame, text='FPS space to be filled later',padx=20, pady=10)
        btn4.pack(padx=10, pady=10, side='left')

        # button that calls open_help()
        btn =ttk.Button(log_frame, text='HELP', command=open_help)
        btn.pack(padx=20, pady=20, side='right')

    def displayFrame(self):
        while True:
            self.image_frame = self.my_camera.capture_image() #erroring out (showing gray screen)....
            # self.update_frame(self.image_frame)
            # self.classification = self.my_classifier.classify(self.image_frame)
            k = cv2.waitKey(1)
            if k % 256 == 27:  # if escape if pressed, close the program
                self.my_camera.close(self)

    def update_frame(self, frame):
        self.frame = frame
        # self.modif_image = self.convert_frame(self.frame)
        print("updating frame..")
        self.frame = create_image(0, 0, image=self.modif, anchor=tkinter.NW)
        # modif_frame = Image.fromarray(frame)   
        # self.imgtk = ImageTk.PhotoImage(image=modif_frame)
        # self.mainLabel.imgtk = self.imgtk
        # self.mainLabel.configure(image= self.imgtk)
        # self.mainLabel.after(10, show_frame)     

    def convert_frame(self, frame):
        return PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))

    def open_help(self):
        webbrowser.open('https://github.com/mjp1997/ASL-Controlled-Smart-Home-Environment/blob/master/help.txt')
      
        #button container
        button_frame= LabelFrame(self.master, text='Help Documentation:', padx=20, pady=20,bg='#f0f4fa')
        button_frame.pack(padx=10, pady=10, side='bottom')

        # button that calls open_help()
        btn =ttk.Button(button_frame, text='Help', command=open_help)
        btn.grid(row=0, column=0, padx=10, pady=10,sticky='w')
        #btn.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)      

    def classifyFrame(self):
        print("classifying frame..")
def main():
    SLISH().mainloop()
main()