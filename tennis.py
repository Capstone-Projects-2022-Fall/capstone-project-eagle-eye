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

# REDU = 8
# def rgbh(xs, mask):
#     def normhist(x): return x / np.sum(x)
#     def h(rgb):
#         return cv2.calcHist([rgb], [0, 1, 2],mask, [256//REDU, 256//REDU, 256//REDU] , [0, 256] + [0, 256] + [0, 256])
#     return normhist(sum(map(h, xs)))

# def smooth(s,x):
#     return gaussian_filter(x,s,mode='constant')

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
    
    
    
    # # REDU = 8


    # # bgsub = cv2.createBackgroundSubtractorMOG2(500, 16, True) #The threshold value could vary(60)
    # bgsub = cv2.createBackgroundSubtractorMOG2(500, 60, True) #The threshold value could vary(60)

    # key = 0

    # kernel = np.ones((3,3),np.uint8)
    # crop = True
    # camshift = True
    # # crop = False
    # # camshift = False
    # termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # pause= False

    # pause= False
    # ###################### Kalman inicial ######################## 
    
    # degree = np.pi/180


    # fps = 30
    # # fps = 120
    # dt = 1/fps
    # # t = np.arange(0,2.01,dt)
    # noise = 3

    # A = np.array(
    #     [1, 0, dt, 0,
    #     0, 1, 0, dt,
    #     0, 0, 1, 0,
    #     0, 0, 0, 1 ]).reshape(4,4)

    # # 중력 조절 
    # u = np.array([0, 5])
    # B = np.array(
    #     [dt**2/2, 0,
    #     0, dt**2/2,
    #     dt, 0,
    #     0, dt ]).reshape(4,2)

    # H = np.array(
    #     [1,0,0,0,
    #     0,1,0,0]).reshape(2,4)

    # # x, y, vx, vy
    # mu = np.array([0,0,0,0])
    # # P = np.diag([1000,1000,1000,1000])**2
    # P = np.diag([10,10,10,10])**2
    # res=[]
    # N = 15
    # sigmaM = 0.0001
    # sigmaZ = 3*noise

    # Q = sigmaM**2 * np.eye(4)
    # R = sigmaZ**2 * np.eye(2)
    # listCenterX=[]
    # listCenterY=[]
    # kf = KalmanFilter()
    # add_count = 0
    # mm=False

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
                    cv2.putText(img=frame, text="OUT!!!", fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=10, color=(0,255,255), org=(0, 0))
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

        # this isnt working...
    # # def rgbh(xs, mask):
    # #     def normhist(x): return x / np.sum(x)
    # #     def h(rgb):
    # #         return cv2.calcHist([rgb], [0, 1, 2],mask, [256//REDU, 256//REDU, 256//REDU] , [0, 256] + [0, 256] + [0, 256])
    # #     return normhist(sum(map(h, xs)))

    # # def smooth(s,x):
    # #     return gaussian_filter(x,s,mode='constant')

    # def predictBallPath(self, frame, xy_In):
    #     # REDU = 8
    #     # frame = copy.copy(frame)
    #     # def rgbh(xs,mask):
    #     #     def normhist(x): return x / np.sum(x)
    #     #     def h(rgb): return cv2.calcHist([rgb], [0, 1, 2], mask, [256//REDU, 256//REDU, 256//REDU], [0, 256] + [0, 256] + [0, 256])
    #     #     return normhist(sum(map(h, xs)))

    #     # def smooth(s,x):
    #     #     return gaussian_filter(x,s,mode='constant')

    #     x1 = int(xy_In[0]*1000)
    #     y1 = int(xy_In[1]*1000)
    #     x2 = int(xy_In[2]*1000)
    #     y2 = int(xy_In[3]*1000)
    #     # x1 = int(xy_In[0])
    #     # y1 = int(xy_In[1])
    #     # x2 = int(xy_In[2])
    #     # y2 = int(xy_In[3])
    #     # bgsub = cv2.createBackgroundSubtractorMOG2(500, 16, True) #The threshold value could vary(60)
    #     # bgsub = cv2.createBackgroundSubtractorMOG2(500, 60, True) #The threshold value could vary(60)
    #     # key = 0
    #     # kernel = np.ones((3,3),np.uint8)
    #     # crop = True
    #     # camshift = True
    #     # # crop = False
    #     # # camshift = False
    #     # termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
    #     # font = cv2.FONT_HERSHEY_SIMPLEX
    #     # pause= False
    #     # ###################### Kalman inicial ######################## 
    #     # degree = np.pi/180
    #     # fps = 120
    #     # dt = 1/fps
    #     # # t = np.arange(0,2.01,dt)
    #     # noise = 3

    #     # A = np.array(
    #     #     [1, 0, dt, 0,
    #     #     0, 1, 0, dt,
    #     #     0, 0, 1, 0,
    #     #     0, 0, 0, 1 ]).reshape(4,4)

    #     # u = np.array([0, 5])
    #     # B = np.array(
    #     #     [dt**2/2, 0,
    #     #     0, dt**2/2,
    #     #     dt, 0,
    #     #     0, dt ]).reshape(4,2)

    #     # H = np.array(
    #     #     [1,0,0,0,
    #     #     0,1,0,0]).reshape(2,4)

    #     # # x, y, vx, vy
    #     # mu = np.array([0,0,0,0])
    #     # # P = np.diag([1000,1000,1000,1000])**2
    #     # P = np.diag([10,10,10,10])**2
    #     # res=[]
    #     # N = 15
    #     # sigmaM = 0.0001
    #     # sigmaZ = 3*noise

    #     # Q = sigmaM**2 * np.eye(4)
    #     # R = sigmaZ**2 * np.eye(2)
    #     # listCenterX=[]
    #     # listCenterY=[]
    #     # kf = KalmanFilter()
    #     # add_count = 0
    #     # mm=False

    #     # width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    #     # height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    #     # fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    #     # out = cv2.VideoWriter('demo.avi', fourcc, 30.0, (int(width), int(height)))

    #     # while(True):
    #     #     key = cv2.waitKey(30) & 0xFF
    #     #     if key== ord("c"): crop = True
    #     #     if key== ord("p"): P = np.diag([100,100,100,100])**2
    #     #     if key==27: break
    #     #     if key==ord(" "): pause =not pause
    #     #     if(pause): continue
            
    #         # ret, frame = cap.read()
    #         # # frame=cv2.resize(frame,(800,600))
    #         # if ret == False:
    #         #     break
            
    #     frame=cv2.resize(frame,(1366,768))
    #     bgs = self.bgsub.apply(frame)
    #     bgs = cv2.erode(bgs,self.kernel,iterations = 1)
    #     bgs = cv2.medianBlur(bgs,3)
    #     bgs = cv2.dilate(bgs,self.kernel,iterations=2)
    #     bgs = (bgs > 200).astype(np.uint8)*255
    #     colorMask = cv2.bitwise_and(frame,frame,mask = bgs)

    #     cv2.imshow("frame", frame)
    #     cv2.imshow("bgs", bgs)
    #     cv2.imshow("colorMask", colorMask)
    #     # cv2.waitKey(0)

    #     if(self.crop):
    #         fromCenter= False
    #         img = colorMask
    #         # r = cv2.selectROI(img, fromCenter) 
    #         # imCrop = img[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    #         imCrop = img[y1:(y1+y2), x1:(x1+x2)]
    #         # imCrop = img[x1:(x1+x2), y1:(y1+y2)]
    #         # cv2.imshow("cropped", imCrop)
    #         # cv2.waitKey(0)
    #         crop = False
    #         camshift = True
    #         imCropMask = cv2.cvtColor(imCrop, cv2.COLOR_BGR2GRAY)
    #         ret,imCropMask = cv2.threshold(imCropMask,30,255,cv2.THRESH_BINARY)
    #         his = smooth(1,rgbh([imCrop],imCropMask))
    #         # roiBox = (int(r[0]), int(r[1]),int(r[2]), int(r[3]))
    #         roiBox = (x1, y1, x2, y2)

    #         # cv2.destroyWindow("ROI selector")

    #     if(self.camshift):
    #         cv2.putText(frame,'Center roiBox',(0,10), self.font, 0.5,(0,255,0),2,cv2.LINE_AA)
    #         cv2.putText(frame,'Estimated position',(0,30), self.font,0.5,(255,255,0),2,cv2.LINE_AA)
    #         cv2.putText(frame,'Prediction',(0,50), self.font, 0.5,(0,0,255),2,cv2.LINE_AA)
    #         self.add_count += 1
    #         rgbr = np.floor_divide( colorMask , REDU)
    #         r,g,b = rgbr.transpose(2,0,1)
    #         l = his[r,g,b]
    #         maxl = l.max()

    #         aa=np.clip((1*l/maxl*255),0,255).astype(np.uint8)
    #         (rb, roiBox) = cv2.CamShift(l, roiBox, self.termination)

    #         cv2.ellipse(frame, rb, (0, 255, 0), 2)
    #         xo=int(roiBox[0]+roiBox[2]/2)
    #         yo=int(roiBox[1]+roiBox[3]/2)
    #         # predicted, statePre, statePost, errorCovPre = kf.predict(int(xo), int(yo))
    #         error=(roiBox[3])
    #         if(yo<error or bgs.sum()<50 ):
    #             predicted, mu, statePost, errorCovPre = self.kf.predict(int(xo), int(yo))
    #             mu,P = self.kf.kal(mu,P,self.B,self.u,z=None)
    #             #mu,P,pred= kalman(mu,P,A,Q,B,a,None,H,R)
    #             m="None"
    #             mm=False
    #         else:
    #             # mu,P,pred= kalman(mu,P,A,Q,B,a,np.array([xo,yo]),H,R)
    #             predicted, mu, statePost, errorCovPre = self.kf.predict(int(xo), int(yo))
    #             mu,P = self.kf.kal(mu,P,self.B,self.u,z=np.array([xo,yo]))
    #             m="normal"
    #         mm=True
    #         if(mm):
    #             listCenterX.append(xo)
    #             listCenterY.append(yo)

    #         if len(listCenterX) > 2:
    #             res += [(mu,P)]
    #             cv2.circle(frame, (predicted[0], predicted[1]), 10, (255, 0, 255),3)
    #             ##### Prediction #####
    #             mu2 = mu
    #             P2 = P
    #             res2 = []

    #             for _ in range(self.fps*2):
    #                 mu2,P2 = self.kf.kal(mu2,P2,self.B,self.u,z=None)
    #                 res2 += [(mu2,P2)]

                
    #             xe = [mu[0] for mu,_ in res]
    #             xu = [2*np.sqrt(P[0,0]) for _,P in res]
    #             ye = [mu[1] for mu,_ in res]
    #             yu = [2*np.sqrt(P[1,1]) for _,P in res]
                
    #             xp=[mu2[0] for mu2,_ in res2]               # The first res2 is unconditionally discarded.
    #             yp=[mu2[1] for mu2,_ in res2]

    #             xpu = [np.sqrt(P[0,0]) for _,P in res2]
    #             ypu = [np.sqrt(P[1,1]) for _,P in res2]

    #             # ball trance 
    #             for n in range(len(listCenterX)): # center of roibox
    #                 cv2.circle(frame,(int(listCenterX[n]),int(listCenterY[n])),3,(0, 255, 0),-1)

    #             # predict location
    #             for n in [-1]:
    #                 uncertainty=(xu[n]+yu[n])/2 # int(uncertainty)
    #                 cv2.circle(frame,(int(xe[n]),int(ye[n])),5,(255, 255, 0),3)


    #             for n in range(len(xp)): # x e y predicted
    #                 uncertaintyP=(xpu[n]+ypu[n])/2
    #                 cv2.circle(frame,(int(xp[n]),int(yp[n])),int(uncertaintyP),(0, 0, 255))

                

    #             if(len(listCenterY)>40):
    #                 # if((listCenterY[-5] < listCenterY[-4]) and(listCenterY[-4] < listCenterY[-3]) and (listCenterY[-3] > listCenterY[-2]) and (listCenterY[-2] > listCenterY[-1])):
    #                 print("Bounce")
    #                 listCenterY=[]
    #                 listCenterX=[]
    #                 res=[]

    #                 mu = np.array([0,0,0,0])
    #                 P = np.diag([100,100,100,100])**2

    #         cv2.imshow('ColorMask',colorMask)
    #         cv2.imshow('mask', bgs)
    #         cv2.imshow('Frame', frame)
    #     return frame


# tennis = Tennis('tennis')

# tennis.printname()
# print(tennis.model)
# tennis.setmodeloptions(tennis.model)
# print(tennis.field)
# tennis.setfieldoptions(tennis.field)

