import argparse
import queue
import imutils
import cv2 
from court_detector import CourtDetector
import torch
import numpy as np
# from c ourtUtils import get_video_properties, get_dtype

def get_dtype():
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    device = torch.device(dev)
    if dev == 'cuda':
        dtype = torch.cuda.FloatTensor
    else:
        dtype = torch.FloatTensor
    print(f'Using device {device}')
    return dtype


def get_video_properties(video):
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

# # parse parameters
# parser = argparse.ArgumentParser()

# parser.add_argument("--input_video_path", type=str)
# parser.add_argument("--output_video_path", type=str, default="")


# args = parser.parse_args()

# input_video_path = args.input_video_path
# output_video_path = args.output_video_path

#  python only_court_and_ball.py --input_video_path=/Users/tyler/Documents/GitHub/tennis-tracking/1secQatar.mp4 --output_video_path=VideoOutput/test_video_output.mp4 --minimap=1 --bounce=0
# input_video_path = '/Users/tyler/Documents/GitHub/tennis-tracking/VideoInput/PaulVThiem.mp4'
input_video_path = '/Users/tyler/Documents/GitHub/capstone-project-eagle-eye/shortQatar.mp4'
output_video_path = '/Users/tyler/Documents/GitHub/capstone-project-eagle-eye/test_video_output.mp4'


n_classes = 256

if output_video_path == "":
    # output video in same path
    output_video_path = input_video_path.split('.')[0] + "VideoOutput/video_output.mp4"

# get video fps&video size
video = cv2.VideoCapture(input_video_path)
fps = int(video.get(cv2.CAP_PROP_FPS))
print('fps : {}'.format(fps))
output_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
output_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# try to determine the total number of frames in the video file
if imutils.is_cv2() is True :
    prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT
else : 
    prop = cv2.CAP_PROP_FRAME_COUNT
total = int(video.get(prop))

# start from first frame
currentFrame = 0

# In order to draw the trajectory of tennis, we need to save the coordinate of previous 7 frames
q = queue.deque()
for i in range(0, 8):
    q.appendleft(None)

# save prediction images as videos
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_video = cv2.VideoWriter(output_video_path, fourcc, fps, (output_width, output_height))

# court
court_detector = CourtDetector()

# players tracker
dtype = get_dtype()

# get videos properties
fps, length, v_width, v_height = get_video_properties(video)

coords = []
frame_i = 0
frames = []
t = []

while True:
  ret, frame = video.read()
  frame_i += 1

  if ret:
    if frame_i == 1:
      print(f'Detecting the court and the players, frame {frame_i}')
      lines = court_detector.detect(frame)
    else: # then track it
      print(f'Tracking the court and the players, frame {frame_i}')
      lines = court_detector.track_court(frame)    
    for i in range(0, len(lines), 4):
      x1, y1, x2, y2 = lines[i],lines[i+1], lines[i+2], lines[i+3]
      cv2.line(frame, (int(x1),int(y1)),(int(x2),int(y2)), (0,0,255), 5)
    new_frame = cv2.resize(frame, (v_width, v_height))
    output_video.write(new_frame)
    frames.append(new_frame)
  else:
    break
video.release()
print('Finished!')

