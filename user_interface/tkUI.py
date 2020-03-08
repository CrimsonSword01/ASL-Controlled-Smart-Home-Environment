import webbrowser
from tkinter import *
import time
from PIL import ImageTk, Image
from tkinter import Label
from tkinter import LabelFrame
from tkinter import Frame
from tkinter import ttk

self = Tk()

#turned into a class by Allison
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
        photo = ImageTk.PhotoImage(Image.open('pic.png'))
        label = Label(header_frame, image=photo)
        label.image= photo
        label.pack(padx=5, pady=5)
        
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

        # function that opens the help documentation link
        def open_help():
            webbrowser.open('https://github.com/mjp1997/ASL-Controlled-Smart-Home-Environment/blob/master/help.txt')
        
        #FPS space
        btn4 =Button(log_frame, text='FPS space to be filled later',padx=20, pady=10)
        btn4.pack(padx=10, pady=10, side='left')

        # button that calls open_help()
        btn =ttk.Button(log_frame, text='HELP', command=open_help)
        btn.pack(padx=20, pady=20, side='right')

        


def main():
    SLISH().mainloop()
main()