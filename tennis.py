import os
import sys
from sport import Sport
import queue
import imutils
import cv2 
from court_detector import CourtDetector
import torch

class Tennis(Sport):
    """Override superclass model with the path to actual sport model"""
    @property
    def model(self):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        relative_path = os.path.join('models', 'tennis', 'tennisModel.pt')
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

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


    def detectCourt(frame_in, frame_num):
        # input_video_path = '/Users/tyler/Documents/GitHub/capstone-project-eagle-eye/shortQatar.mp4'
        # output_video_path = '/Users/tyler/Documents/GitHub/capstone-project-eagle-eye/test_video_output.mp4'

        # if output_video_path == "":
        #     # output video in same path
        #     output_video_path = input_video_path.split('.')[0] + "VideoOutput/video_output.mp4"

        # get video fps&video size
        # video = cv2.VideoCapture(input_video_path)
        # fps = int(video.get(cv2.CAP_PROP_FPS))
        # print('fps : {}'.format(fps))
        # output_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        # output_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # try to determine the total number of frames in the video file
        # if imutils.is_cv2() is True :
        #     prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT
        # else : 
        #     prop = cv2.CAP_PROP_FRAME_COUNT
        # total = int(video.get(prop))

        # start from first frame
        # currentFrame = 0

        # In order to draw the trajectory of tennis, we need to save the coordinate of previous 7 frames
        # q = queue.deque()
        # for i in range(0, 8):
        #     q.appendleft(None)

        # save prediction images as videos
        # fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # output_video = cv2.VideoWriter(output_video_path, fourcc, fps, (output_width, output_height))

        # court
        court_detector = CourtDetector()

        # players tracker
        # dtype = self.get_dtype()

        # get videos properties
        # fps, length, v_width, v_height = self.get_video_properties(video)

        # frame_i = 0
        # frames = []

        frame_i=frame_num
        frame=frame_in

        # while True:
        #     ret, frame = video.read()
        #     frame_i += 1

        #     if ret:
        # if frame_i == 0:
            # print(f'Detecting the court and the players, frame {frame_i}')
        lines = court_detector.detect(frame)
        # else: # then track it
        #     print(f'Tracking the court and the players, frame {frame_i}')
        #     lines = court_detector.track_court(frame)    
        for i in range(0, len(lines), 4):
            x1, y1, x2, y2 = lines[i],lines[i+1], lines[i+2], lines[i+3]
            cv2.line(frame, (int(x1),int(y1)),(int(x2),int(y2)), (0,0,255), 5)
        return frame
        new_frame = cv2.resize(frame, (v_width, v_height))
        output_video.write(new_frame)
        frames.append(new_frame)
        #     else:
        #         break
        # video.release()
        # print('Finished!')
        return 1
  
# tennis = Tennis('tennis')

# tennis.printname()
# print(tennis.model)
# tennis.setmodeloptions(tennis.model)
# print(tennis.field)
# tennis.setfieldoptions(tennis.field)

