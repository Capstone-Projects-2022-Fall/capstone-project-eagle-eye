# Created By : Tyler Hyde (1 July 2021)
 
import logging
import os
import sys
import tkinter as tk
from tkinter import Radiobutton, filedialog, messagebox, IntVar
from tkinter import *
import tkinter
from tkinter.constants import LEFT, W
from PIL import ImageTk, Image
from tkinter.simpledialog import askstring
# from tkinter.messagebox import showinfo
from pandas import *
import pandas
 
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
        self.rb_LIVE_mode = None
        self.rb_PRERECORDED_mode = None
 
        # Video input string -> For API
        self.video_infile_name = ""           
        
        # file type selected: 1 is live, 2 is prerecorded
        self.mode_checked = IntVar()
 
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
        video_infile_label = tk.Label(self.root, text = "Prerecorded Input File:", fg='#000000', font=('Arial', 12))                                  # Label
        self.tb_video_infile = tk.Entry(self.root, text = "Prerecorded Input File", width=40)                                      # Input Box
        video_infile_explore = tk.Button(self.root, text = "Browse", command = self.browse_infiles, fg='#000000', font=('Arial', 12))                          # Browse Button
        video_infile_label.config(bg='#ffffff')
       
        # radio buttons
        self.rb_LIVE_mode = Radiobutton(self.root, text="Live Mode", variable = self.mode_checked, value=1)
        self.rb_LIVE_mode.config(bg='#ffffff', fg='#000000', font=('Arial', 12))
        self.rb_PRERECORDED_mode = Radiobutton(self.root, text="Prerecorded Mode", variable = self.mode_checked, value=2)
        self.rb_PRERECORDED_mode.config(bg='#ffffff', fg='#000000', font=('Arial', 12))
 
        # Enter button
        button_enter = tk.Button(text = "Execute", command = self.enter, fg='#000000', font=('Arial', 12))
        # Exit button
        button_exit = tk.Button(self.root, text = "Exit", command = sys.exit, fg='#000000', font=('Arial', 12))
 
        # ---- Grid ---------------------------------------------------------------------------------------------------------------------------
        heading.grid(row=0, column=2)

        # add the label, textbox, and button for the input file 
        video_infile_label.grid(row=5, column=1)
        self.tb_video_infile.grid(row=5, column=2)
        video_infile_explore.grid (row = 5, column = 3)

        # add a label for the mode
        tk.Label(self.root, bg='#ffffff', text="Choose input type:", fg='#000000', font=('Arial', 12)).grid(row=7, column=1)
        self.rb_LIVE_mode.grid(row=7, column=2)
        self.rb_PRERECORDED_mode.grid(row=7, column=3)
 
        # add the buttons
        button_enter.grid(row=16, column=2)
        button_exit.grid(row = 17, column = 2)
 
        #set the defaults for the radio buttons 
        self.rb_LIVE_mode.select()

        # Start the main loop
        self.root.mainloop()
 
    def enter(self):
        '''
        Function that is triggered when "Enter" is pressed
        '''
        # check infile, if none was given restart
        if self.mode_checked == 2:
            self.check_infile()
            # run script with prerecorded video
        else:
            # run script with live feed
            pass
        
        # # otherwise the user gave a single file so just do that one
        # elif self.tb_video_infile:
        #     isdir = 0
        #     self.switch(logger, file, isdir, self.outputfileType_checked.get())
        # else:
        #     # something went wrong/general catch all (this should never happen but just in case restart the loop)
        #     messagebox.showerror(title='Input Error', message="You must provide either an input file or directory.")
        self.do_cleanup()
 
    # define the browse buttons and their actions when pressed (theyre set up in start())
    def browse_infiles(self):
        self.video_infile_name = filedialog.askopenfilename()
        self.tb_video_infile.insert(0, self.video_infile_name)

    # def switch(self, logger, file, isdir, outputfileType):
    #     # grab either the indir or infile based on the passed flag from earlier and set the infile_name accordingly
    #     if isdir == 0:
    #         self.video_infile_name = self.tb_video_infile.get()
    #     elif isdir ==1:
    #         self.video_infile_name = self.tb_indir.get()
    #     self.outfile_name = self.tb_outfile.get()
    #     if os.path.exists(self.outfile_name) and os.path.exists(self.video_infile_name): # if an outfile was given go down this path
    #         if self.mode_checked.get() ==1: # SE16 was checked
    #             table2csv(logger, outputfileType, self.writer, infile=self.video_infile_name,outfile=self.outfile_name, logDir=file).main()
    #         elif self.mode_checked.get() ==2: #STAD was checked
    #             stad2csv(logger, outputfileType, self.writer, infile=self.video_infile_name, outfile=self.outfile_name, logDir=file)
    #     elif os.path.exists(self.video_infile_name): #no outfile was given
    #         if self.mode_checked.get() ==1: # SE16 was checked
    #             table2csv(logger, outputfileType, self.writer, infile=self.video_infile_name, logDir=file).main()
    #         elif self.mode_checked.get() ==2: #STAD was checked
    #             stad2csv(logger, outputfileType, self.writer, infile=self.video_infile_name, logDir=file)   
              
    def check_infile(self):
        # check infile, if none was given restart
        print("you made it to check infile")
        if self.tb_video_infile.get() == "":
            messagebox.showerror(title='Input File', message="You must provide an input file.")
            self.root.mainloop()
 
    def do_cleanup(self):
        print("you made it to do_cleanup")
        # do a final sweep of the text boxes to make sure they are clear 
        self.tb_video_infile.delete(0, 'end') # deletes the text in each box



        self.video_infile_name = ''


        #reset stdout

        #reset the debug and workbook flags



 
 
App(700,400).start()