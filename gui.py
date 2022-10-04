# Created By : Tyler Hyde (27 September 2022)
from logging import error
import os
import glob
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import *
import tkinter
from tkinter.constants import LEFT, W
from yolov5 import detect
 
class App():
    # Class variables
    # Tkinter root
    root = tkinter.Tk()
    # drop down options
    dd_mode_options = [
        "Live",
        "Prerecorded"
    ]
    dd_sports_options = [
        "Tennis",
        "Soccer",
        "Basketball",
        "Baseball",
        "Hockey",
        "Ping Pong"
    ]
    # Variables for the input file name, mode, and sport
    video_infile_name = StringVar()           
    mode_checked = StringVar()
    sport_checked = StringVar()
    # dropdown menus
    mode_dropdown = OptionMenu(root, mode_checked, *dd_mode_options)
    sport_dropdown = OptionMenu(root, sport_checked, *dd_sports_options)

    # Instance variables
    def __init__(self, width, height):
        # Set window size
        g = "{width}x{height}".format(width=width, height=height)
        self.root.geometry(g)
        # Define the background color
        self.root.config(bg='#ffffff')
        # set defaults for the dropdown menus 
        self.mode_checked.set("Live")
        self.sport_checked.set("Tennis")
        # Set window title
        self.root.title('Eagle Eye')
        # Enter button
        button_enter = tk.Button(self.root, text = "Execute", command = self.enter, fg='#000000', font=('Arial', 12))
        # Exit button
        button_exit = tk.Button(self.root, text = "Exit", command = sys.exit, fg='#000000', font=('Arial', 12))
        # ---- Grid -----------
        # add mode and sports selection dropdown and labels
        tk.Label(self.root, bg='#ffffff', text="Choose input type:", fg='#000000', font=('Arial', 12)).grid(row=7, column=1)
        self.mode_dropdown.grid(row=7, column=2)
        tk.Label(self.root, bg='#ffffff', text="Choose Sport:", fg='#000000', font=('Arial', 12)).grid(row=8, column=1)
        self.sport_dropdown.grid(row=8, column=2)
        # add buttons
        button_enter.grid(row=16, column=2)
        button_exit.grid(row = 17, column = 2)

    def start(self):
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
            try:
                detect.run(source=self.video_infile_name, view_img=True)
            except Exception as e:
                self.error_message(e)
            # open the video we just ran, it will be in ../yolov5/runs/detect/* (* means all if need specific format then *.csv)
            # setting the root dir to ../ is basically the same as calling `cd ..` before looking for the pathname
            # using the join to ensure its os agnostic, on a mac it puts '/' on windows it uses '\' to build the path
            pathname = os.path.join(os.getcwd(), 'yolov5', 'runs', 'detect', '*' )  
            list_of_files = glob.glob(pathname=pathname, root_dir="../")
            latest_file = max(list_of_files, key=os.path.getctime)
            try:
                # try to open the file in windows
                os.startfile(latest_file)
            except AttributeError:
                # else we try a unix os command for linux and mac
                os.system(f"open {latest_file}")
            except Exception as e:
                self.error_message(e)
        else:
            # run script with live feed
            try:
                detect.run(source=0)
            except Exception as e:
                self.error_message(e)
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
            try:
                os.path.exists(self.video_infile_name)
            except Exception as e:
                self.error_message(e)
 
    def do_cleanup(self):
        # clear any variables that were filled 
        self.video_infile_name = "" 
    
    def error_message(self, error):
        messagebox.showerror(title='Error Message', message=f"{error}")
        self.root.mainloop()
 
# App(290,200).start()
if __name__ == '__main__':
    App(290,200).start()