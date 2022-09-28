# Created By : Tyler Hyde (26 September 2022)
import os
import glob
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import *
from tkinter.constants import LEFT, W
from yolov5 import detect
 
class App():

    def __init__(self, width, height):
        # Tkinter root
        self.root = tk.Tk()
        # Define the width and height
        self.width = width
        self.height = height
 
        # define background color
        self.root.config(bg='#ffffff')
 
        # Tkinter objects
        # Infile textbox object
        self.tb_video_infile = None

        # mode radio buttons
        # self.rb_LIVE_mode = None
        # self.rb_PRERECORDED_mode = None
        self.dd_mode_options = [
            "Live",
            "Prerecorded"
        ]
        self.dd_sports_options = [
            "Tennis",
            "Soccer",
            "Basketball",
            "Baseball",
            "Hockey",
            "Ping Pong"
        ]
 
        # Video input string -> For API
        self.video_infile_name = StringVar()           
        
        # file type selected: 1 is live, 2 is prerecorded
        # self.mode_checked = IntVar()
        self.mode_checked = StringVar()
        self.mode_checked.set("Live")
        self.sport_checked = StringVar()
        self.sport_checked.set("Tennis")
 
    def start(self):
        '''
        Main starter function that handles all processes
        '''
        # Set window size
        g = "{width}x{height}".format(width=self.width, height=self.height)
        self.root.geometry(g)
 
        # Set window title
        self.root.title('')
 
        # Heading
        heading = tk.Label(self.root, text = "Eagle Eye")
        heading.config(font = ('Arial', 14), bg='#ffffff', fg='#000000')
 
        # Infile
        # video_infile_label = tk.Label(self.root, text = "Prerecorded Input File:", fg='#000000', font=('Arial', 12))                                  # Label
        # self.tb_video_infile = tk.Entry(self.root, text = "Prerecorded Input File", width=40)                                      # Input Box
        # video_infile_explore = tk.Button(self.root, text = "Browse", command = self.browse_infiles, fg='#000000', font=('Arial', 12))                          # Browse Button
        # video_infile_label.config(bg='#ffffff')
       
        # radio buttons
        # self.rb_LIVE_mode = Radiobutton(self.root, text="Live Mode", variable = self.mode_checked, value=1)
        # self.rb_LIVE_mode.config(bg='#ffffff', fg='#000000', font=('Arial', 12))
        # self.rb_PRERECORDED_mode = Radiobutton(self.root, text="Prerecorded Mode", variable = self.mode_checked, value=2)
        # self.rb_PRERECORDED_mode.config(bg='#ffffff', fg='#000000', font=('Arial', 12))
        self.mode_dropdown = OptionMenu( self.root, self.mode_checked, *self.dd_mode_options)
        self.sport_dropdown = OptionMenu( self.root, self.sport_checked, *self.dd_sports_options)
 
        # Enter button
        button_enter = tk.Button(text = "Execute", command = self.enter, fg='#000000', font=('Arial', 12))
        # Exit button
        button_exit = tk.Button(self.root, text = "Exit", command = sys.exit, fg='#000000', font=('Arial', 12))
 
        # ---- Grid ---------------------------------------------------------------------------------------------------------------------------
        heading.grid(row=0, column=2)

        # add the label, textbox, and button for the input file 
        # video_infile_label.grid(row=5, column=1)
        # self.tb_video_infile.grid(row=5, column=2)
        # video_infile_explore.grid (row = 5, column = 3)

        # add a label for the mode
        tk.Label(self.root, bg='#ffffff', text="Choose input type:", fg='#000000', font=('Arial', 12)).grid(row=7, column=1)
        # self.rb_LIVE_mode.grid(row=7, column=2)
        # self.rb_PRERECORDED_mode.grid(row=7, column=3)
        self.mode_dropdown.grid(row=7, column=2)

        tk.Label(self.root, bg='#ffffff', text="Choose Sport:", fg='#000000', font=('Arial', 12)).grid(row=8, column=1)
        self.sport_dropdown.grid(row=8, column=2)
 
        # add the buttons
        button_enter.grid(row=16, column=2)
        button_exit.grid(row = 17, column = 2)

        # Start the main loop
        self.root.mainloop()
 
    def enter(self):
        '''
        Function that is triggered when "Enter" is pressed
        '''
        # check infile, if none was given restart
        if self.mode_checked.get() == "Prerecorded":
            # get the file from the user
            self.get_infile()
            # run script with prerecorded video
            detect.run(source=self.video_infile_name, view_img=True)
            # open the video we just ran, it will be in ../yolov5/runs/detect/* (* means all if need specific format then *.csv)
            list_of_files = glob.glob("/Users/tyler/Documents/GitHub/capstone-project-eagle-eye/yolov5/runs/detect/*") 
            latest_file = max(list_of_files, key=os.path.getctime)
            try:
                # try to open the file in windows
                os.startfile(latest_file)
            except AttributeError:
                # else we try a unix os command for linux and mac
                os.system(f"open {latest_file}")
            else:
                messagebox.showerror(title='Could not open video file', message="Could not open video file.")
                self.root.mainloop()
            
        else:
            # run script with live feed
            detect.run(source=0)
            pass
        self.do_cleanup()
             
    def get_infile(self):
        # ask the user to provide a prerecorded video
        self.video_infile_name = filedialog.askopenfilename()
        # check that they actually chose one, if not restart 
        if self.video_infile_name == "":
            messagebox.showerror(title='Input File', message="You must provide an input file.")
            self.root.mainloop()
        else:
            # check if its a valid file
            if os.path.exists(self.video_infile_name):
                # file is good
                pass
            else: 
                messagebox.showerror(title='Invalid File', message="Invalid filename, please choose another input file.")
                self.root.mainloop()
            print(self.video_infile_name)
            pass
 
    def do_cleanup(self):
        # clear any variables that were filled 
        self.video_infile_name = "" 
 
App(290,200).start()