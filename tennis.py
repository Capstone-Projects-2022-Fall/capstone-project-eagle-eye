import os
import time
import sys
from court_reference import CourtReference
from sport import Sport
import cv2 
from court_detector import CourtDetector
import torch
import math
import numpy as np
import copy
from scipy.ndimage import gaussian_filter
from predictionKalmanfilter import KalmanFilter
from pygame import mixer 

class Tennis(Sport):
    """Override superclass model with the path to actual sport model"""
    @property
    def model(self):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        relative_path = os.path.join('models', 'tennis', 'tennisModel.pt')
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    
    # public var for lines reference to use with ball detection
    court_lines = None
    court_reference = None
    prev_pos = [0, 0]
    est_vel = [0,0]
    prev_est_vel = [0,0]
    bounce_count = 0
    bounce_thresh = 30
    custom_coordinates = None
    # for testing
    # custom_coordinates = np.array([
    #     [761,536],     # top left corner
    #     [28,849],     # bottom left
    #     [1918,868],    # bottom right
    #     [1178,540],     # top right rorner
    #     ])  

    custom_lines = None
   
    def __init__(self, sportname):
        super().__init__(sportname)

    def printname(self):
        return self.sportname
    
    def setmodeloptions(self,model):
        return f"changing model options with {model}"

    def setfieldoptions(self,field):
        return f"changing field options with {field}"
        
    def sendscript(self, model):
        return model

    def get_dtype(self):
        dev = 'cuda' if torch.cuda.is_available() else 'cpu'
        device = torch.device(dev)
        if dev == 'cuda':
            dtype = torch.cuda.FloatTensor
        else:
            dtype = torch.FloatTensor
        print(f'Using device {device}')
        return dtype

    def detectCourt(self, frame):
        """Display any error that is raised in a pop up window and restart the main loop
        
        Args: 
            frame (Array): A frame or image that we want to detect court lines on
        """
        court_detector = CourtDetector()
        frame=frame
        lines = court_detector.detect(frame)
        # If no court is found lines will be none 
        if lines != []:
            for i in range(0, len(lines), 4):
                x1, y1, x2, y2 = lines[i],lines[i+1], lines[i+2], lines[i+3]
                cv2.line(frame, (int(x1),int(y1)),(int(x2),int(y2)), (0,0,255), 5)
            #set the court refereence variable with the object with filled lines 
            self.court_reference = court_detector
            return frame
        else:
            # trigger a function to have the user pick the court 
            print("NO COURT DETECTED!")
            return self.userDefinedCoordinates(frame=frame)
    
    def trackCourt(self, frame):
        if self.court_reference != None:
            lines = self.court_reference.track_court(frame)
            for i in range(0, len(lines), 4):
                x1, y1, x2, y2 = lines[i],lines[i+1], lines[i+2], lines[i+3]
                cv2.line(frame, (int(x1),int(y1)),(int(x2),int(y2)), (0,0,255), 5) 
            return frame
        else:
            # trigger a function to have the user pick the court 
            return self.userDefinedCoordinates(frame=frame)

    def lineCall(self, xy_In, frame):
        if self.court_reference is not None:
            return self.computeLineCall(xy_In=xy_In, frame=frame, court_lines = self.court_reference, custom_flag=0)
        elif self.custom_lines is not None:
            # use the custom lines...
            return self.computeLineCall(xy_In=xy_In, frame=frame, court_lines = self.custom_lines, custom_flag=1)
        # return the frame no matter what, if niether condition wasnt met then its just the same frame that came in
        return frame

    def computeLineCall(self, xy_In, frame, court_lines, custom_flag):
        # Read destination image.
        
        img_dst = os.path.join(os.getcwd(), 'court_configurations', 'court_reference.png')
        # img_dst = cv2.imread('/Users/tyler/Documents/GitHub/basketballVideoAnalysis/court-detection/court_configurations/court_reference.png')

        # Four corners of the court + mid-court circle point in destination image 
        # Start top-left corner and go anti-clock wise + mid-court circle point
        pts_dst = np.array([
            [421, 559],     # top left corner
            [421, 2937],     # bottom left
            [1244, 2937],    # bottom right
            [1244, 559],     # top right corner
            ])   

        if custom_flag:
            top_baseline = (court_lines[0][1] + court_lines[0][3]) / 2
            bottom_baseline = (court_lines[1][1] + court_lines[1][3]) / 2
        else:
            top_baseline = (court_lines.baseline_top[1] + court_lines.baseline_top[3]) / 2
            bottom_baseline = (court_lines.baseline_bottom[1] + court_lines.baseline_bottom[3]) / 2

        ball_x = xy_In[0]
        ball_y = xy_In[1]
        ball_pos = [ball_x, ball_y]

        self.est_vel[0] = (ball_pos[0] - self.prev_pos[0])
        self.est_vel[1] = (ball_pos[1] - self.prev_pos[1])

        # check if the sign of the velocity has changed
        if math.copysign(1, self.est_vel[0]) != math.copysign(1, self.est_vel[1]) or math.copysign(1,self.est_vel[1]) != math.copysign(1, self.prev_est_vel[1]):
            # check for bounces from large change in velocity
            dvx = abs(self.est_vel[0] - self.prev_est_vel[0])
            dvy = abs(self.est_vel[1] - self.prev_est_vel[1])
            change_vel = math.sqrt(dvx*dvx + dvy*dvy)
            if change_vel > self.bounce_thresh:
                print(f"change is: {change_vel}, threshold is {self.bounce_thresh}")
                self.bounce_count += 1
                # add ball bounce circle
                center_coordinates = int(ball_x), int(ball_y)
                color = (255, 0, 0)
                thickness = -1
                cv2.circle(frame, center_coordinates, 10, color, thickness)
                if (ball_y < top_baseline or ball_y > bottom_baseline): #if we are here the ball has "bounced"
                    cv2.putText(img=frame, text="OUT!!!", fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,255,255), org=(ball_x, ball_y))
                    self.playSound()
                    print("OUT!!!")
        # update previous state trackers
        self.prev_est_vel = self.est_vel[:]
        self.prev_pos = ball_pos[:]
        return frame

    def playSound(self):
        # need this check for windows, doesnt seem to want to work with just the relative path on my machine
        if os.getcwd().endswith('yolov5'):
            os.chdir("..")
            file = os.path.join(os.getcwd(), 'sound', 'outCall.mp3')
            os.chdir("yolov5")
        else:
            file = os.path.join(os.getcwd(), 'sound', 'outCall.mp3')
        mixer.init()
        mixer.music.load(file)
        mixer.music.play()
        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(1)

    def userDefinedCoordinates(self, frame):
        if self.custom_coordinates is not None:
            frame = cv2.polylines(frame, [self.custom_coordinates], isClosed=True, color=[255,0,0], thickness=2)
        else: 
            pts_src = self.selectCoordinates(frame=frame)
            self.custom_coordinates = pts_src
            self.custom_lines = np.array([
                np.concatenate([pts_src[0], pts_src[3]]),     # top baseline
                np.concatenate([pts_src[1], pts_src[2]]),     # bottom baseline
                np.concatenate([pts_src[0], pts_src[1]]),    # left line
                np.concatenate([pts_src[3], pts_src[2]]),     # right line
                ]) 
            frame = cv2.polylines(frame, [pts_src], isClosed=True, color=[255,0,0], thickness=2)
        return frame

    def selectCoordinates(self, frame):
        # displaying the image
        frameCopy = copy.copy(frame) 
        cv2.imshow('select coordinates', frameCopy)

        # setting mouse handler for the image
        # and calling the click_event() function
        pts_src = np.array([
            [0,0],     # top left corner
            [0,0],     # bottom left
            [0,0],    # bottom right
            [0,0],     # top right rorner
            ]) 
        i=0
        param = [pts_src, frameCopy, i]

        print("Eagle Eye was unable to automatically detect your cour parameters.\nPlease select the four corners of either the singles court or doubles court starting at the top left corner and going counter clockwise.\nTo select a coordinate press the left mouse button. If you need to clear all the coordinates press the right mouse button.\n Note that the old coordinates will remain on the screen but just ignore them.\nThe system will only allow you to select 4 coordinates so for best results all 4 corners of the court need to be within the frame.\n To exit press 0")
        cv2.setMouseCallback('select coordinates', self.click_event, param=param)
        # wait for a key to be pressed to exit
        cv2.waitKey(0)
        # close the window
        cv2.destroyAllWindows()
        return param[0] #the pts_src that we passed to the callback function

    def click_event(self, event, x, y, flags, param):
        # checking for left mouse clicks
        frame =  param[1]

        if event == cv2.EVENT_LBUTTONDOWN:
            if param[2] == 4: #if we have 4 clicks thats the 4 corners of the court so dont accept any more
                return
            i = param[2]
            param[0][i] = [x, y]
            print(param[0][i])
            # display the coordinates on another image so the user knows where they clicked 
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, str(x) + ',' +
                        str(y), (x,y), font,
                        1, (255, 0, 0), 2)
            param[2]+=1
            cv2.imshow('image', frame)

        # checking for right mouse clicks, maybe clear the coordinates in case you mess up?
        if event==cv2.EVENT_RBUTTONDOWN:
            # reset the coordinates and i, user can do this if they mess up/want to redo 
            param[2] = 0
            param[0] = np.array([
                [0,0],    
                [0,0],  
                [0,0],  
                [0,0], 
                ])
            print("cleared coordinates")
            
# tennis = Tennis('tennis')

# tennis.printname()
# print(tennis.model)
# tennis.setmodeloptions(tennis.model)
# print(tennis.field)
# tennis.setfieldoptions(tennis.field)

