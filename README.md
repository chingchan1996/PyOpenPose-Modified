# PyOpenPose-Modified

This project is based on OpenPose by CMU as well as PyOpenPose by FORTH-ModelBasedTracker/PyOpenPose.

# Dockerfile
The file builds the required environment for developing PyOpenPose-Modified.
OS Version:Ubuntu16.04
CUDA Version:8.0
cuDNN Version:6.0
OpenCV Version:3.2.0

# OpenPoseWrapper.cpp
A modified version of the source code from FORTH-ModelBasedTracker/PyOpenPose. After cloning the original version of PyOpenPose, replace this file with the one in /PyOpenPose/PyOpenPoseLib/

# outputkeypoint.py
A python script that output the 18-key points of each person.
Ex."python3 outputkeypoint.py test2.mp4 False 0.5"
