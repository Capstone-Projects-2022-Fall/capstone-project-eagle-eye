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
 
        self.root = tk.Tk()         # Tkinter root
       

       
        # Define the width and height
        self.width = width
        self.height = height
 
        # define background color
        self.root.config(bg='#ceddea')
 
        # Tkinter objects
        self.tb_video_infile = None           # Infile textbox object


       


 
        self.rb_LIVE_mode = None        # STAD type radiobutton
        self.rb_PRERECORDED_mode = None        # SE16 type radiobutton
 


 
        self.video_infile_name = ""           # Video input string -> For API


 

        self.mode_checked = IntVar()      # file type selected: 1 is SE16, 2 is STAD

LEFT OFF HERE, CONTINUE TO GO THROUGH AND DELETE ANYTHING YOU DONT NEED!!!!
 

 
        # flag for debug mode
        self.debug_flag = 0
 
        # flag for workbook mode
        self.workbook_flag = 0
 
        #menu
        self.menubar = Menu(self.root)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Activate Debug Mode", command=self.check_debug)
        filemenu.add_command(label="Activate Workbook Mode", command=self.check_workbook)
        self.root.config(menu=self.menubar)
        self.menubar.add_cascade(label='File', menu=filemenu)
 
        #degug label
        self.debug_label = ""
 
        #workbook name
        self.workbookname = ''
 
        # writer
        self.writer = None
 
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
        heading = tk.Label(self.root, text = "SAP Log File Converter")
        heading.config(font = ('helvetica', 14), bg='#ceddea', fg='#325876')
        separator = tk.Label(self.root, text = " ", bg='#ceddea')
 
        # Infile
        in_label = tk.Label(self.root, text = "Single SAP Log File:"+" "*23, fg='#325876', font=('helvetica', 11))                                  # Label
        self.tb_video_infile = tk.Entry(self.root, text = "Single SAP Log File", width=40)                                      # Input Box
        button_explore1 = tk.Button(self.root, text = "Browse", command = self.browse_infiles, fg='#325876', font=('helvetica', 11))                          # Browse Button
        in_label.config(bg='#ceddea')
       
        # indir
        indir_label = tk.Label(self.root, text = "Directory of SAP Log Files:" + " "*13, fg='#325876', font=('helvetica', 11))                                  # Label
        self.tb_video_infile = tk.Entry(self.root, text = "Directory of SAP Log Files", width=40)                                      # Input Box
        button_exploreindir = tk.Button(self.root, text = "Browse", command = self.browse_indirectory, fg='#325876', font=('helvetica', 11))                          # Browse Button
        indir_label.config(bg='#ceddea')
 
        # radio buttons
        self.rb_PRERECORDED_mode = Radiobutton(self.root, text="SE16 (SAP table)", variable = self.mode_checked, value=1)
        self.rb_LIVE_mode = Radiobutton(self.root, text="STAD (STAD table)", variable = self.mode_checked, value=2)
        self.rb_LIVE_mode.config(bg='#ceddea', fg='#325876', font=('helvetica', 11))
        self.rb_PRERECORDED_mode.config(bg='#ceddea', fg='#325876', font=('helvetica', 11))
 

 

 

 
        separator2 = tk.Label(self.root, text = " ", bg='#ceddea')
 
        # Enter button
        enter = tk.Button(text = "Execute", command = self.enter, fg='#325876', font=('helvetica', 11))
        # Exit button
        button_exit = tk.Button(self.root, text = "Exit", command = sys.exit, fg='#325876', font=('helvetica', 11))
       

 
        #debug label
        self.debug_label = tk.Label(self.root, text = "", bg='#ceddea')
       
        #workbook label
        self.workbook_label = tk.Label(self.root, text = "", bg='#ceddea')
 
        # ---- Grid ---------------------------------------------------------------------------------------------------------------------------
        heading.grid(row=0, column=2)
        separator.grid(row=1, column=2)
       
        in_label.grid(row=5, column=1)
        self.tb_video_infile.grid(row=5, column=2)
        button_explore1.grid (row = 5, column = 3)
       
        indir_label.grid(row=6, column=1)

        button_exploreindir.grid (row = 6, column = 3)
        # add a label for the file type and output buttons
        tk.Label(self.root, bg='#ceddea', text="Choose input table type:", anchor='w', width=25, fg='#325876', font=('helvetica', 11)).grid(row=7, column=1)
        self.rb_PRERECORDED_mode.grid(row=7, column=2)
        self.rb_LIVE_mode.grid(row=7, column=3)
 

 
 

 

 
        logfile_label.grid(row=14, column=1)

        button_explore3.grid(row =14, column = 3)
 
        separator2.grid(row=15, column=2)
 
        enter.grid(row=16, column=2)
        button_exit.grid(row = 17, column = 2)
 

 
        self.debug_label.grid(row=20, column=1)
        self.workbook_label.grid(row=20, column=3)
 
        #set the defaults for the radio buttons (se16, csv, and console logging)
        self.rb_PRERECORDED_mode.select()


       
        # Start the main loop
        self.root.mainloop()
 
    def enter(self):
        '''
        Function that is triggered when "Enter" is pressed
        '''

       

 
        # reset the writer before the run
        self.writer = None
 
        # set up the logging, first do the standard set up. the goal of this code is to set up all logging here and pass a logger to the subsequent functions
        # that way you only need to call either table2csv or stad2csv with the in, out, and log 
        logDir = None
        file = None
        logger_format = logging.Formatter('[%(asctime)s] %(name)s-%(funcName)s-%(levelname)s : %(message)s')
        logger = logging.getLogger(__name__)
        stream_handler = logging.StreamHandler(sys.stdout) # sysout is standard
        stream_handler.setFormatter(logger_format)
        logger.addHandler(stream_handler)
        if self.debug_flag:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
 

 
        # check infile, if none was given restart
        self.check_infile()
        if self.tb_indir.get():
            # set the flag for the switch if the user provided a directory and hit the workbook function to
            # see is the user has asked for a workbook, if they have create a writer. this will be sent in the switch
            isdir = 1
            self.try_workbook(isdir, logger)
            self.convert_directory(isdir, logger, file)
        # otherwise the user gave a single file so just do that one
        elif self.tb_video_infile:
            isdir = 0
            self.switch(logger, file, isdir, self.outputfileType_checked.get())
        else:
            # something went wrong/general catch all (this should never happen but just in case restart the loop)
            messagebox.showerror(title='Input Error', message="You must provide either an input file or directory.")
        self.do_cleanup(file, logger)
 
    # define the browse buttons and their actions when pressed (theyre set up in start())
    def browse_infiles(self):
        self.video_infile_name = filedialog.askopenfilename()
        self.tb_video_infile.insert(0, self.video_infile_name)
        if self.tb_indir.get() != '' or None:
            messagebox.showerror(title='Single File', message="You may select a single file or a directory, not both, please try again.")
            self.tb_indir.delete(0, 'end') # deletes the text in the indir, you can only select one
            self.video_infile_name = ''
   
    def browse_indirectory(self):
        # if there is a single file already selected tell the user they can only have one or the other
        self.video_infile_name = filedialog.askdirectory()
        self.tb_indir.insert(0, self.video_infile_name)       
        if self.tb_video_infile.get() != '' or None:
            messagebox.showerror(title='Directory', message="You may select a single file or a directory, not both, please try again.")
            self.tb_video_infile.delete(0, 'end') # deletes the text in the infile, you can only select one
            self.video_infile_name = ''
 

 
    def browse_logfiles(self):
        # if you try to put a file in the logging section without the file logging radio button pressed throw an error
        if not self.logType_checked.get()==2:
            messagebox.showerror(title='File Logging', message="Please check the 'File Logging' Box if you want to proceed")
        else:
            self.logfile_name = filedialog.askdirectory()
            self.tb_logfile.insert(0, self.logfile_name)
 
    def check_debug(self):
        if self.debug_flag == 1:
            self.debug_label.config(text="")
            self.debug_flag = 0
            self.debug_label.update()
        else:
            self.debug_flag = 1
            self.debug_label.config(text="Debug mode active", fg='#325876', font=('helvetica', 11))
            self.debug_label.update()
   
    def check_workbook(self):
        if self.workbook_flag == 1:
            self.workbook_label.config(text="")
            self.workbook_flag = 0
            self.workbook_label.update()
        else:
            self.workbook_flag = 1
            self.workbook_label.config(text="Workbook Mode Active", fg='#325876', font=('helvetica', 11))
            self.workbook_label.update()
 
    def switch(self, logger, file, isdir, outputfileType):
        # grab either the indir or infile based on the passed flag from earlier and set the infile_name accordingly
        if isdir == 0:
            self.video_infile_name = self.tb_video_infile.get()
        elif isdir ==1:
            self.video_infile_name = self.tb_indir.get()
        self.outfile_name = self.tb_outfile.get()
        if os.path.exists(self.outfile_name) and os.path.exists(self.video_infile_name): # if an outfile was given go down this path
            if self.mode_checked.get() ==1: # SE16 was checked
                table2csv(logger, outputfileType, self.writer, infile=self.video_infile_name,outfile=self.outfile_name, logDir=file).main()
            elif self.mode_checked.get() ==2: #STAD was checked
                stad2csv(logger, outputfileType, self.writer, infile=self.video_infile_name, outfile=self.outfile_name, logDir=file)
        elif os.path.exists(self.video_infile_name): #no outfile was given
            if self.mode_checked.get() ==1: # SE16 was checked
                table2csv(logger, outputfileType, self.writer, infile=self.video_infile_name, logDir=file).main()
            elif self.mode_checked.get() ==2: #STAD was checked
                stad2csv(logger, outputfileType, self.writer, infile=self.video_infile_name, logDir=file)           
 
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
 
 
    def try_workbook(self, isdir, logger):
        # if we got a diectory, .xlsx is checked, AND workbook mode is active then we need to add the excel writer
        if isdir == 1 and (self.mode_checked.get() ==2 or self.mode_checked.get() ==1) and self.workbook_flag == 1:
            # check if there is already a directory, if so we dont need to ask for one
            if self.tb_outfile.get():
                self.workbookname = self.tb_outfile.get()
            else:
                messagebox.showinfo(title= "Workbook Directory", message = "Please select a directory to place your workbook.")
                self.workbookname = tkinter.filedialog.askdirectory()
            askworkbookname = askstring('Workbook Name', 'Enter a name for your workbook.')
            self.workbookname += ("/" + askworkbookname + ".xlsx")
            try:
                self.writer = pandas.ExcelWriter(self.workbookname)
            except Exception:
                logger.critical("Invalid workbook file name.")
                messagebox.showerror(title='Workbook File', message="Invalid workbook file name.")
                self.root.mainloop()
   
    def convert_directory(self, isdir, logger, file):
        # if the user provided a directory loop through all of the files making sure to skip anything thats
        # not a .txt file (for example if the user didnt provide any output directory there may be a bunch of .csv files in there)
        for (root, dirs, files) in os.walk(self.video_infile_name, topdown=True):
            for x in files:
                self.video_infile_name = ''
                self.tb_indir.delete(0, 'end')
                self.tb_indir.insert(0, os.path.join(root, x))
                # grab the extension and skip any that arent .txt files
                ext = os.path.splitext(self.tb_indir.get())
                if ext[1] != '.txt':
                    continue
                self.switch(logger, file, isdir, self.outputfileType_checked.get())
                # reset the file paths once youve called the function (otherwise they will remain and affect the next run)
                self.tb_indir.delete(0, 'end') # deletes the text in each box
                self.video_infile_name = ''
   
    def check_infile(self):
        # check infile, if none was given restart
        if self.tb_video_infile.get() == "" and self.tb_indir.get() == "":
            messagebox.showerror(title='Input File', message="You must provide either an input file or directory of tables.")
            self.root.mainloop()
 
    def do_cleanup(self, file, logger):
        # close the log file if one is still open
        if file != None:
            file.close()
        # save the and close the writer if one was created
        if self.writer != None:
            self.writer.close()
        # do a final sweep of the text boxes to make sure they are clear 
        self.tb_video_infile.delete(0, 'end') # deletes the text in each box
        self.tb_indir.delete(0, 'end')


        self.video_infile_name = ''


        #reset stdout
        sys.stdout = sys.__stdout__
        #reset the debug and workbook flags
        self.debug_flag = 0
        self.debug_label.config(text="")
        self.workbook_flag = 0
        self.workbook_label.config(text="")
        #reset the stream handler
        while logger.hasHandlers():
            logger.handlers.pop()

 
 
App(700,620).start()