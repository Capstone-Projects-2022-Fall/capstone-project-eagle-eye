# System Overview
Eagle Eye is a simple, easy to use tennis line call system that is deployed while playing to track the ball and make automated line calls. The Eagle Eye system consists of a camera or recording device and the application installed on a laptop. The camera can be mounted on one end of the court on either a tripod or a mount attached to the surrounding fence of a tennis court. Connected to the camera is an HDMI to USB capture card which converts the cameras HDMI signal to a USB signal that the laptop can use. The laptop is running the Eagle Eye program and serves as both the live feed monitor that displays what it is seeing and the speed of each shot and the audio output device for the audible cues for when a ball is determined to be out. The Eagle Eye app will handle the flight tracking and speed calculations for the ball, make judgements on whether the ball flies out-of-bounds, and present the video feed and calculations for the user.

# Installation
To install Eagle Eye clone the main branch from git as you would with any other git repo. Next you will need to clone our fork of the YOLO repo. First run the command `https://github.com/tyler3490/yolov5.git`, then you will need to install the requirements 
to your local virtual environment so activate it and run the command `pip install -r requirements.txt`. The Eagle Eye gui should now work on your machine. 

# Instructions For Use

**Windows Instructions**
Unzip the included WindowsEagleEye.zip file and navigate to the EagleEye.exe file. Double click the .exe and a terminal window will appear. Windows my alert you that the exe is dangerous and if so click `run anyway`. Choose the mode and desired sport and click execute. 

**Mac Instructions**
Unzip the included MacEagleEye.zip. Before you can run an unknown application you may need to disable Gatekeeper in MacOS. To do so open a new terminal and type `sudo spctl --master-disable`. You will then be prompted for your password, enter it and press enter. Gatekeeper is now disabled across all of MacOS (to re enable it simply run the command `spctl --enable`). Navigate to the EagleEye folder, right click on it and select `New terminal at folder`. To execute the program run the command `./EagleEye`. Choose the mode and desired sport and click execute.

**Notes**
To exit live view make sure that the window displaying the video is active (i.e. click on it) and press and hold the 'Q' key until the window closes, you can then continue to use Eagle Eye as you normally would.

# Team Members
- Athena Evans
- Chase Donovan Glasper
- Liam Hart
- Robert Stachurski
- Thien H Le
- Tyler Hyde
