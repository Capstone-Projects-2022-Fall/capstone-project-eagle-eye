# System Overview
Eagle Eye is a simple, easy to use tennis line call system that is deployed while playing to track the ball and make automated line calls. The Eagle Eye system consists of a camera or recording device and the application installed on a laptop. The camera can be mounted on one end of the court on either a tripod or a mount attached to the surrounding fence of a tennis court. Connected to the camera is an HDMI to USB capture card which converts the cameras HDMI signal to a USB signal that the laptop can use. The laptop is running the Eagle Eye program and serves as both the live feed monitor that displays what it is seeing and the speed of each shot and the audio output device for the audible cues for when a ball is determined to be out. The Eagle Eye app will handle the flight tracking and speed calculations for the ball, make judgements on whether the ball flies out-of-bounds, and present the video feed and calculations for the user. Additionally Eagle Eye can identify and track balls in other sports including soccer, basketball, and baseball. 

# Installation
To install Eagle Eye clone the main branch from git as you would with any other git repo. Next you will need to clone our fork of the YOLO repo. First run the command `https://github.com/tyler3490/yolov5.git`, then you will need to install the requirements 
to your local virtual environment so activate it and run the command `pip install -r requirements.txt`. The Eagle Eye gui should now work on your machine. 

# Instructions For Use

**Windows Instructions**
Download and unzip the [Windows EagleEye zip file](https://tuprd.sharepoint.com/:u:/s/EagleEye/EZhImvRwypJAlZ20L79xuSwBwV6Gj6-kyhjjL553XWDvUQ?e=4rELO8) file and navigate to the EagleEye.exe file. Double click the .exe and a terminal window will appear. Windows my alert you that the exe is dangerous and if so click `run anyway`. Choose the mode and desired sport and click execute. 

**Mac Instructions**
Download and unzip the [Mac EagleEye zip file](https://tuprd.sharepoint.com/:u:/s/EagleEye/EcaPaMtU6-hAmJg1mORujowBKVDLetoLan7Z6HjQLirF_Q?e=bwGqeC). Before you can run an unknown application you may need to disable Gatekeeper in MacOS. To do so open a new terminal and type `sudo spctl --master-disable`. You will then be prompted for your password, enter it and press enter. Gatekeeper is now disabled across all of MacOS (to re enable it simply run the command `spctl --enable`). Navigate to the EagleEye folder, right click on it and select `New terminal at folder`. To execute the program run the command `./EagleEye`. Choose the mode and desired sport and click execute.

**General Instructions**

Eagle Eye has two main modes: Live and Prerecorded. There are also several sports to select from including Default, Tennis, Soccer, Basketball, and Baseball. To use the system select the mode and sport you desire and select execute. In live mode the system will use whatever camera is set as the default web cam on your computer and detect whatever object you selected from the sport menu (i.e. tennis balls, basketballs, etc.) and continue to run until you press the `q` key. Prerecorded mode will prompt you for a video file and analyze that file using whatever sport model you chose. After the analysis it will open the resulting file allowing you to watch it in full speed and save it wherever you would like. When you are done with the program simply press `Exit` and Eagle Eye will close. 

**Tennis Instructions**

Select either prerecorded or live option from the gui and select execute. Eagle Eye will attempt to automatically find the lines on the court. If it cannot you will be prompted to select the four corners of the court (either including or excluding the doubles alley depending on whether you are playing singles or doubles.). It is essential that you select the corners starting in the top left corner and moving counter clockwise (top left, bottom left, bottom right, top right) otherwise the system will not porperly lay out the court. Eagle Eye will only allow you to input 4 coordinates so if you mistakenly click you can clear the saved coordinates from the back end by pressing the right mouse button. Note that the old coordinates will remain on the screen but they can be ignored. Once you are satisfied with your selection press the 0 key and they will be saved. You will now have automated line calls for balls that are over either base line. 

**Acceptance Tests**

Any Temple University member should have access to these documents through these links:
- [Accuracy Acceptance Test](https://tuprd.sharepoint.com/:x:/s/EagleEye/EWdHx1v9BtlFtRsry1cyuTQBJgaHO0FFUWlDnYv1JoK5iQ?e=4JadFO)
- [GUI Acceptance Test](https://tuprd.sharepoint.com/:x:/s/EagleEye/EYXqKU9iX8BMiINHc47md6kBV9MAz1nlXfk62hJFckyXQg?e=BbGhvO)

Contact Tyler Hyde at tuj66923@temple.edu for technical questions

**Notes**

- To exit live view make sure that the window displaying the video is active (i.e. click on it) and press and hold the `q` key until the window closes, you can then continue to use Eagle Eye as you normally would.
- When using live view Eagle Eye will use whatever camera is set as your default web cam. For windows users you can connect whatever camera you wish and select it as your default. On macOS whatever camera was most recently used will be automatically set as your primary camera but if you encounter a problem open the facetime app and in the video menu select the camera you wnat to use. This will set it as the primary camera and Eagle Eye should detect it. 
- Every time you run Eagle Eye the results will be saved to a folder in your executable. They will be located in `../dist/EagleEye/yolov5/runs/detect` under a folder called expXX where xx is an incrementing number so the highest number is the most recent file. 
- The `Default` sport option uses the default YOLOv5s model. 

# Team Members
- Athena Evans
- Chase Donovan Glasper
- Liam Hart
- Robert Stachurski
- Thien H Le
- Tyler Hyde
