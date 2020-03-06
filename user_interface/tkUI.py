import webbrowser
import cv2
from tkinter import *
from PIL import Image, ImageTk
#from PIL import ImageTk
import time
try:
    from tkinter import ttk   
except ImportError:
    from tkinter import ttk

self = Tk()

class SLISH(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title('SLISH')
        self.master.config(bg='#c9e4ff')

        #picture didn't work without the full path - will change later
        photo = PhotoImage(file='/Users/ANDor/OneDrive/Desktop/pic.png')
        label = Label(self.master, image=photo)
        label.pack()
        
        #centering the page- draft
        window_height = 900
        window_width = 1000

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        self.master.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        #space for camera_stream
        camera_frame= LabelFrame(self.master, text='Stream:', padx=10, pady=10,bg='#f0f4fa')
        camera_frame.pack(padx=10, pady=10,expand='yes', fill='both')

        btn2 =ttk.Button(camera_frame, text='camera space to be filled later')
        btn2.grid(row=0, column=0, padx=40, pady=20,sticky='w')

        #space for log
        log_frame= LabelFrame(self.master, text='Log:', padx=10, pady=10,bg='#f0f4fa')
        log_frame.pack(padx=10, pady=10,expand='yes', fill='both')

        btn3 =ttk.Button(log_frame, text='log space to be filled later')
        btn3.grid(row=0, column=0, padx=40, pady=20,sticky='w')

        # function that opens the link
        def open_help():
            webbrowser.open('https://github.com/mjp1997/ASL-Controlled-Smart-Home-Environment/blob/master/help.txt')

        #button container
        button_frame= LabelFrame(self.master, text='Help Documentation:', padx=20, pady=20,bg='#f0f4fa')
        button_frame.pack(padx=10, pady=10, side='bottom')

        # button that calls open_help()
        btn =ttk.Button(button_frame, text='Help', command=open_help)
        btn.grid(row=0, column=0, padx=10, pady=10,sticky='w')
        #btn.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)


def main():
    SLISH().mainloop()
main()