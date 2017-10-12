#!/usr/bin/python

"""
Abbe Experiment
Benedict Diederich, beniroquai	

Test code for using the Ivport camera multiplexer and switching between Raspberry Pi cameras.
View multiple cameras on the screen without the need to save them as jpgs.
Possible with the help of OpenCV for Raspi
"""

import picamera
import cv2
import imutils
import numpy as np
import threading
import time

from picamera.array import PiRGBArray
from picamera import PiCamera
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS

import sys
import RPi.GPIO as gp
import os

gp.setwarnings(False)
gp.setmode(gp.BOARD)

# See IvPort documentation for information on GPIO pins
gp.setup(7, gp.OUT)  # Selection pin
gp.setup(11, gp.OUT) # Enable1 pin
gp.setup(12, gp.OUT) # Enable2 pin

def set_camera(i):
    """
    Set which camera port on the multiplexer to use for image input.
    Assumes that the IvPort camera multiplexer is used with Jumper A soldered.

    Adapted from sample code provided on Ivport github repository.

    i : int
        camera number. Should be 1, 2, 3, or 4.
    """
    if i==1:
        gp.output(7, False)
        gp.output(11, False)
        gp.output(12, True)
    elif i==2:
        gp.output(7, True)
        gp.output(11, False)
        gp.output(12, True)
    elif i==3:
        gp.output(7, False)
        gp.output(11, True)
        gp.output(12, False)
    elif i==4:
        gp.output(7, True)
        gp.output(11, True)
        gp.output(12, False)
    else:
        print "set_camera: Invalid camera number given, active camera port was not changed."


def video_test(camera_list=[1, 3], frames_per_camera=10):
    """
    Tests displaying a video stream from the Raspberry Pi camera.

    Shows a video, cycling  between the cameras specified in the camera_list argument. 
    The number of frames to show from a camera before switching is determined by
    the frames_per_camera argument.
    """
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    res = (640, 480)
    camera.resolution = res
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=res)
     
    # allow the camera to warmup
    time.sleep(0.1)
     
    # capture frames from the camera
    i = 0
    current_camera_index = 0

    window_name = "Frame"+str(camera_list[current_camera_index])
    
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text

        image = frame.array
        
	# show the frame
	# print 'Show frame'
        cv2.imshow(window_name, image)
        key = cv2.waitKey(1) & 0xFF
 
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

        if i == frames_per_camera:
            i = 0
            
	    current_camera_index = (current_camera_index + 1) % (len(camera_list))
	    set_camera(camera_list[current_camera_index])
            # Brief sleep to prevent visual glitches when cameras are switched 
            time.sleep(0.01)
            
	    # Decide which window the frame should be displayed at 
            window_name = "Frame"+str(camera_list[current_camera_index])

            
        i += 1
        #print i

def main():
    set_camera(1)
    # decide which camera should be used for the experiment e.g. 1,3; how many images should be used after the camera is toggled? e.g. 1
    video_test([1,3], 1)

if __name__ == "__main__":
    main()

