import os
import sys
from court_reference import CourtReference
from sport import Sport
import cv2 
from court_detector import CourtDetector
import torch
import math
import numpy as np

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

    def detectCourt(self, frame_in):
        """Display any error that is raised in a pop up window and restart the main loop
        
        Args: 
            frame_in (Array): A frame or image that we want to detect court lines on
        """
        court_detector = CourtDetector()
        frame=frame_in
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
            print("NO COURT DETECTED!!!")
            return frame
    
    def trackCourt(self, frame_in):
        if self.court_reference != None:
            lines = self.court_reference.track_court(frame_in)
            for i in range(0, len(lines), 4):
                x1, y1, x2, y2 = lines[i],lines[i+1], lines[i+2], lines[i+3]
                cv2.line(frame_in, (int(x1),int(y1)),(int(x2),int(y2)), (0,0,255), 5) 
            return frame_in
        else:
            # trigger a function to have the user pick the court 
            print("NO COURT DETECTED!!!")
            return frame_in

    def lineCall(self, xy_In, frame_in):
        if self.court_reference is not None:
            court_lines = self.court_reference
        
            top_baseline = (court_lines.baseline_top[1] + court_lines.baseline_top[3]) / 2
            bottom_baseline = (court_lines.baseline_bottom[2] + court_lines.baseline_bottom[2]) / 2
            
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
                        cv2.putText(img=frame_in, text="OUT!", fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=10, color=(0,255,255), org=(500, 500))
                        print("OUT!!!")
            # update previous state trackers
            self.prev_est_vel = self.est_vel[:]
            self.prev_pos = ball_pos[:]
        # return the frame no matter what, if the condition wasnt met then its just the same frame that came in
        return frame_in

    def warpCourt(self, frame_in):
        ogFrame = frame_in
        # bBaseline = self.court_reference.baseline_bottom
        # tBaseline= self.court_reference.baseline_top
        # Linner = self.court_reference.left_inner_line
        # Rinner = self.court_reference.right_inner_line
        # print(bBaseline)
        # print(tBaseline)
        # print(Linner)
        # print(f"{int(Linner[0])}, {int(Linner[1])}")
        # print(f"{Linner[2]}, {Linner[3]}")
        # print(f"{Rinner[2]}, {Rinner[3]}")
        # print(f"{Rinner[0]}, {Rinner[1]}")
        # print(Rinner)
        # pts_src = np.array([
        #     [int(Linner[0]),int(Linner[1])],     # top left corner
        #     [int(Linner[2]),int(Linner[3])],     # bottom left
        #     [int(Rinner[2]),int(Rinner[3])],    # bottom right
        #     [int(Rinner[0]),int(Rinner[1])],     # top right rorner
        #     ])   

        # 3secQatarTest.mp4 coordinates
        # pts_src = np.array([
        #     [642,212],     # top left corner
        #     [392,712],     # bottom left
        #     [1321,708],    # bottom right
        #     [1069,210],     # top right rorner
        #     ])   

        # swingvisionmed1
        # pts_src = np.array([
        #     [816,291],     # top left corner
        #     [124,867],     # bottom left
        #     [1946,877],    # bottom right
        #     [1235,293],     # top right rorner
        #     ])   

        # swingvisionmed2
        pts_src = np.array([
            [918,305],     # top left corner
            [440,678],     # bottom left
            [1668,718],    # bottom right
            [1219,308],     # top right rorner
            ]) 
  
        frame_in = cv2.polylines(frame_in, [pts_src], isClosed=True, color=[255,0,0], thickness=2)
        # Read destination image.
        img_dst = cv2.imread('/Users/tyler/Documents/GitHub/capstone-project-eagle-eye/court_configurations/court_reference.png')

        # reference image points
        pts_dst = np.array([
            [421, 559],     # top left corner
            [421, 2937],     # bottom left
            [1244, 2937],    # bottom right
            [1244, 559],     # top right corner
            ])   

        # Calculate Homography
        h, status = cv2.findHomography(pts_src, pts_dst)
        
        # Warp source image to destination based on homography
        img_src2 = ogFrame
        img_out = cv2.warpPerspective(frame_in, h, (img_dst.shape[1], img_dst.shape[0]))
        # cv2.imshow("Warped", img_out)
        # cv2.waitKey(0)
        # cv2.imshow("lines", frame_in)
        return img_out

# tennis = Tennis('tennis')

# tennis.printname()
# print(tennis.model)
# tennis.setmodeloptions(tennis.model)
# print(tennis.field)
# tennis.setfieldoptions(tennis.field)

