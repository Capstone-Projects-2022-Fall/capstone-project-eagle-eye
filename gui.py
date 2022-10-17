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
from soccer import Soccer
from tennis import Tennis
from basketball import BasketBall

class App():
    """GUI class

    This class gives the user a GUI which offers an easy way to interact with the detect
    script and our custom trained models. 
    
    Attributes:
        root: Tkinter instance
        dd_mode_options (list): List of mode options available 
        dd_sports_options (list): List of sports options available 
        video_infile_name (StringVar): String variable for the pre recorded file name. Defaults to ""
        mode_checked (StringVar): String variable for the selected mode. Defaults to ""
        path_to_runs (StringVar): String variable for the path to the runs folder. Defaults to ""
        sport_checked (StringVar): String variable for the selected sport. Defaults to ""
        mode_dropdown (OptionMenu): Drop down menu that contians the dd_mode_options
        sport_dropdown (OptionMenu): Drop down menu that contians the dd_sports_options
        tennis_class (Sport): Instance of tennis class
        soccer_class (Sport): Instance of soccer class
        basketball_class (Sport): Instance of basketball class
    """
    root = tkinter.Tk()
    dd_mode_options = [
        "Live",
        "Prerecorded"
    ]
    dd_sports_options = [
        "Default",
        "Tennis",
        "Soccer",
        "Basketball",
        "Baseball",
        "Hockey",
        "Ping Pong"
    ]
    video_infile_name = StringVar()           
    mode_checked = StringVar()
    sport_checked = StringVar()
    path_to_runs = StringVar()
    mode_dropdown = OptionMenu(root, mode_checked, *dd_mode_options)
    sport_dropdown = OptionMenu(root, sport_checked, *dd_sports_options)
    tennis_class= Tennis("Tennis")
    soccer_class = Soccer("Soccer")
    basketball_class = BasketBall("Basketball")

    def __init__(self, width, height):
        """Sets up instance variables

        Attributes: 
            button_enter (tk.Button): Button to initiate program
            button_exit (tk.Button): Button to exit program

        Args:
            width (int): Width of the GUI window 
            height (int): Height of the GUI window 
        """
        # Set window size
        g = "{width}x{height}".format(width=width, height=height)
        self.root.geometry(g)
        # Define the background color
        self.root.config(bg='#ffffff')
        # set defaults for the dropdown menus 
        self.mode_checked.set("Live")
        self.sport_checked.set("Default")
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
        # add buttons to grid
        button_enter.grid(row=16, column=2)
        button_exit.grid(row = 17, column = 2)

    def start(self):
        """Start the mainloop of the tkinter instance i.e. start the GUI"""
        self.root.mainloop()

    def enter(self):
        """Executes when the enter button is pressed

        We check what the mode is and based on that wither start the detect script accordingly. 
        """
        if self.mode_checked.get() == "Prerecorded":
            self.run_prerecorded()
        else:
            self.run_live()
        self.do_cleanup()

    def run_live(self):
        """Run the detect script in live mode"""
        weights = self.sport_selector()
        try:
            detect.run(source=0, weights=weights)
        except Exception as e:
            self.error_message(e)

    def run_prerecorded(self):
        """Run the detect script in prerecorded mode"""
        # get the file from the user
        self.get_infile()
        # get the current sport selected
        weights = self.sport_selector()
        # run script with prerecorded video
        weights = self.resource_path(weights)
        try:
            detect.run(source=self.video_infile_name, view_img=True, weights=weights)
        except Exception as e:
            self.error_message(e)
        latest_file = self.get_latest_file()
        try:
            # try to open the file in windows
            os.startfile(latest_file)
        except AttributeError:
            # else we try a unix os command for linux and mac
            os.system(f"open {latest_file}")
        except Exception as e:
            self.error_message(e)

    def get_infile(self):
        """Get the file to analyze from the user using a dialog box pop up"""
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
        """Resets any variables that have been set"""
        self.video_infile_name == ""
    
    def error_message(self, error):
        """Display any error that is raised in a pop up window and restart the main loop
        
        Args: 
            error (Exception): The error that was raised or a string. 
        """
        messagebox.showerror(title='Error Message', message=f"{error}")
        self.root.mainloop()

    def sport_selector(self):
        """Get the current sports model and other data. 

        Args: sport (StringVar)
        """
        mode = self.sport_checked.get()
        if mode == "Tennis":
            return self.tennis_class.model
        elif mode == "Soccer":
            return self.soccer_class.model
        elif mode == "Basketball":
            return self.basketball_class.model
        elif mode == "Default":
            return 'yolov5s.pt'

    def get_latest_file(self):
        """Returns the latest file from the runs folder in yolo, if that doesnt exist ask the user to provide its location.

        Open the video we just ran, it will be in ../yolov5/runs/detect/* (* means all if need specific format then *.csv)
        setting the root dir to ../ is basically the same as calling `cd ..` before looking for the pathname
        using the join to ensure its os agnostic, on a mac it puts '/' on windows it uses '\' to build the path      

        Returns:
            path latest_file: the path to the latest file in the yolo runs folder
        """
        path_to_runs = self.path_to_runs.get()
        if path_to_runs == "": # if we dont have a stored path look for one
            pathname = os.path.join(os.getcwd(), 'yolov5', 'runs', 'detect', '*' )
            print(pathname)
            # list_of_files = glob.glob(pathname=pathname, root_dir=os.getcwd())
            list_of_files = glob.glob(pathname=pathname)
            if not list_of_files: #if we cant find the default run location look in the root 
                pathname = os.path.join(os.getcwd(), 'runs', 'detect', '*' )
                list_of_files = glob.glob(pathname=pathname, root_dir="../")
                if not list_of_files:
                    pathname = filedialog.askdirectory(message = "Please select the most recent directory in the run folder")
                    list_of_files = glob.glob(pathname=pathname)
            self.path_to_runs.set(pathname)
        else: # we already have a path stored 
            list_of_files = glob.glob(pathname=self.path_to_runs.get(), root_dir="../")
        return max(list_of_files, key=os.path.getctime)

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

# App(290,200).start()
if __name__ == '__main__':
    App(290,200).start()