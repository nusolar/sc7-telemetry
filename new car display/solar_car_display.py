#imports
#import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font as tkFont

#import gps frame that's in same folder
import gps_display

WIDTH = 500
HEIGHT = 300
BCK_COLOR = "#381b4d" #dark purple
FG_COLOR = "#ebebeb" #silver

class CarDisplay(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.title("NU Solar Car")
        self._frame = None
        self.switchFrame(HomeFrame)
        self.configure(background=BCK_COLOR, padx=15, pady=15)

        #Fullscreen
        self.fullScreen = True
        self.attributes("-fullscreen", self.fullScreen)
        self.bind('<Escape>', self.toggleFullscreen)

        #set center screen window with following coordinates
        #self is tk.Tk
        self.MyLeftPos = (self.winfo_screenwidth() - 500) / 2
        self.myTopPos = (self.winfo_screenheight() - 300) / 2
        self.geometry( "%dx%d+%d+%d" % (WIDTH, HEIGHT, self.MyLeftPos, self.myTopPos))
        
        #full screen button
        self.is_full = StringVar()
        self.is_full.set("Minimize") #initial text
        fullscreen_btn = Button(self, textvariable=self.is_full,
            command = self.toggleFullscreen, font=("Helvetica", 15), height=2)
        fullscreen_btn.pack(side=TOP, anchor=NW)
    
    #for toggling full screen with esc
    def toggleFullscreen(self, *args):
        self.fullScreen = not self.fullScreen
        self.attributes("-fullscreen", self.fullScreen)
        
        #set button text
        if self.fullScreen == True:
            self.is_full.set("Minimize")
        else:
            self.is_full.set("Full Screen")
        
        #center window
        self.geometry( "%dx%d+%d+%d" % (WIDTH, HEIGHT, self.MyLeftPos, self.myTopPos))
        
    #when gps button clicked, change frame
    def switchFrame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.configure(background=BCK_COLOR)
        self._frame.pack(side=BOTTOM, expand=True, fill=BOTH)
        



class HomeFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        parent.configure(background=BCK_COLOR)
        #frame that shows the velocity and buttons
        self.mainframe = Frame(self, bg=BCK_COLOR)
        
        #frame with all the deets
        self.info_frame = Frame(self, bg=BCK_COLOR)
        
        #font styles
        info_font = ("Helvetica", 20, "bold")
        vel_font = ("Helvetica", 160, "bold", "italic")
        gps_font = ("Helvetica", 20, "bold")
        
        #velocity label
        self.speed = StringVar()
        self.speed.set("28.6")
        speed_label = ttk.Label(self.mainframe, textvariable=self.speed,
            font=vel_font, background=BCK_COLOR, foreground=FG_COLOR)
        speed_label.grid(column=0, row=0, sticky=S)
        
        #mph label
        units_label = ttk.Label(self.mainframe, text="MPH", font=("Helvetica", 30, "bold", "italic"),
            background=BCK_COLOR, foreground=FG_COLOR)
        units_label.grid(column=0, row=1, sticky=N, padx=(0, 300))
        
        #gps button
        gps_btn = Button(self.mainframe, text="GPS", font=gps_font, width=10, height = 2,
            command= lambda : parent.switchFrame(gps_display.gps_display))
        gps_btn.grid(column=0, row=2, sticky=SW)
        
        
        #info labels
        cruise_label = ttk.Label(self.info_frame, text="Cruise Contol", font=info_font)
        cruise_label.grid(column=0, row=0, sticky=W)
        self.cruise_on = StringVar()
        self.cruise_on.set("Off")
        cruise_status = ttk.Label(self.info_frame, textvariable=self.cruise_on, font=info_font)
        cruise_status.grid(column=1, row=0, sticky=E)
        
        can_label = ttk.Label(self.info_frame, text="CAN Status", font=info_font)
        can_label.grid(column=0, row=1, sticky=W)
        self.can_on = StringVar()
        self.can_on.set("Connected")
        can_status = ttk.Label(self.info_frame, textvariable=self.can_on, font=info_font)
        can_status.grid(column=1, row=1, sticky=E)
        
        current_label = ttk.Label(self.info_frame, text="Main Current (A)", font=info_font)
        current_label.grid(column=0, row=2, sticky=W)
        self.current = StringVar()
        self.current.set(11.89)
        can_status = ttk.Label(self.info_frame, textvariable=self.current, font=info_font)
        can_status.grid(column=1, row=2, sticky=E)
        
        voltage_label = ttk.Label(self.info_frame, text="Main Voltage (V)", font=info_font)
        voltage_label.grid(column=0, row=3, sticky=W)
        self.voltage = StringVar()
        self.voltage.set(14.29)
        voltage_status = ttk.Label(self.info_frame, textvariable=self.voltage, font=info_font)
        voltage_status.grid(column=1, row=3, sticky=E)
        
        lowestV_label = ttk.Label(self.info_frame, text="Lowest Voltage (V)", font=info_font)
        lowestV_label.grid(column=0, row=4, sticky=W)
        self.lowestV = StringVar()
        self.lowestV.set(1.8)
        lowestV_status = ttk.Label(self.info_frame, textvariable=self.lowestV, font=info_font)
        lowestV_status.grid(column=1, row=4, sticky=E)
        
        #set color
        for child in self.info_frame.winfo_children():
            child.configure(background=BCK_COLOR, foreground=FG_COLOR)
        
        #space out columns
        for ii in range(2):
            self.info_frame.columnconfigure(ii, weight=2)
        
        self.mainframe.columnconfigure(0, weight=1)
            
        #space out rows
        for ii in range(5):
            self.info_frame.rowconfigure(ii, weight=1)
        
        self.mainframe.rowconfigure(0, weight=5) #make velocity box biggest
        self.mainframe.rowconfigure(1, weight=2) #make mph second biggest
        self.mainframe.rowconfigure(2, weight=1) #button is smallest
        
        #pack statements
        #expand - add extra available space
        #padx = (left, right)
        self.mainframe.pack(expand=True, fill=BOTH, side=LEFT)
        self.info_frame.pack(expand=False, fill=BOTH, side=RIGHT, padx=(0, 10))



def main():
    #if os.environ.get('DISPLAY', '') == '':
     #   os.environ.__setitem__('DISPLAY', ':0.0')
     
    root = CarDisplay()
    root.mainloop()

if __name__ == '__main__':
    main()