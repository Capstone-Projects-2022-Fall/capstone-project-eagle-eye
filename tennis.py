import os
import sys
from court_reference import CourtReference
from sport import Sport
import cv2 
from court_detector import CourtDetector
import torch
import math
import numpy as np
import copy

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
    bounce_thresh = 10
    custom_coordinates = None
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

    def get_video_properties(self, video):
        # Find OpenCV version
        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

        # get videos properties
        if int(major_ver) < 3:
            fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
            length = int(video.get(cv2.cv.CAP_PROP_FRAME_COUNT))
            v_width = int(video.get(cv2.cv.CAP_PROP_FRAME_WIDTH))
            v_height = int(video.get(cv2.cv.CAP_PROP_FRAME_HEIGHT))
        else:
            fps = video.get(cv2.CAP_PROP_FPS)
            length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            v_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            v_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return fps, length, v_width, v_height

    def detectCourt(self, frame):
        """Display any error that is raised in a pop up window and restart the main loop
        
        Args: 
            frame (Array): A frame or image that we want to detect court lines on
        """
        court_detector = CourtDetector()
        frame=frame
        lines = court_detector.detect(frame)
        # If no court is found lines will be none 
        if lines != None:
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
            print("NO COURT DETECTED!")
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
        if custom_flag:
            top_baseline = (court_lines[0][1] + court_lines[0][3]) / 2
            bottom_baseline = (court_lines[1][1] + court_lines[1][3]) / 2
        else:
            top_baseline = (court_lines.baseline_top[1] + court_lines.baseline_top[3]) / 2
            bottom_baseline = (court_lines.baseline_bottom[1] + court_lines.baseline_bottom[3]) / 2
        
        ball_x = xy_In[0]*1000
        ball_y = xy_In[1]*1000
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
                self.bounce_count += 1
                if (ball_y < top_baseline or ball_y > bottom_baseline): #if we are here the ball has "bounced"
                    cv2.putText(img=frame, text="OUT!", fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=10, color=(0,255,255), org=(500, 500))
                    print("OUT!!!")
        # update previous state trackers
        self.prev_est_vel = self.est_vel[:]
        self.prev_pos = ball_pos[:]
        return frame

    def userDefinedCoordinates(self, frame):
        if self.custom_coordinates is not None:
            pts_src = self.custom_coordinates
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

        print("Eagle Eye was unable to automatically detect your cour parameters.\nPlease select the four corners of either the singles court or doubles court starting at the top left corner and going counter clockwise.\nTo select a coordinate press the left mouse button. If you need to clear all the coordinates press the right mouse button.\nThe system will only allow you to select 4 coordinates so for best results all 4 corners of the court need to be within the frame.\n To exit press 0")
        cv2.setMouseCallback('select coordinates', self.click_event, param=param)
        # wait for a key to be pressed to exit
        cv2.waitKey(0)
        # close the window
        cv2.destroyAllWindows()
        return pts_src

    def click_event(self, event, x, y, flags, params):
        # checking for left mouse clicks
        frame =  params[1]

        if event == cv2.EVENT_LBUTTONDOWN:
            if params[2] == 4: #if we have 4 clicks thats the 4 corners of the court so dont accept any more
                return
            print(x, ', ', y)
            i = params[2]
            params[0][i] = [x, y]
            print(params[0][i])
            # display the coordinates on another image so the user knows where they clicked 
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, str(x) + ',' +
                        str(y), (x,y), font,
                        1, (255, 0, 0), 2)
            cv2.imshow('image', frame)
            params[2]+=1

        # checking for right mouse clicks, maybe clear the coordinates in case you mess up?
        if event==cv2.EVENT_RBUTTONDOWN:
            # reset the coordinates and i, user can do this if they mess up/want to redo 
            params[2] = 0
            params[0] = np.array([
                [0,0],    
                [0,0],  
                [0,0],  
                [0,0], 
                ])
            


# tennis = Tennis('tennis')

# tennis.printname()
# print(tennis.model)
# tennis.setmodeloptions(tennis.model)
# print(tennis.field)
# tennis.setfieldoptions(tennis.field)

