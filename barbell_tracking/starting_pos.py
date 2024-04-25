'''
This script is used by the contour_track.py script to keep track of the initial coordinates of the barbell
'''

import cv2
import numpy as np

def find_initial_coordinates(video_path):
    '''
    This function returns to the primary tracker a purple bounding box around the starting position of the barbell,
    whilst this functionality could be kept in the same script, it is easier to track while separated.
    '''
    lower_blue = np.array([90, 120, 120])
    upper_blue = np.array([100, 255, 255])
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()

    if not success:
        print("Failed to read video")
        cap.release()
        return None

    # Convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create a mask for the specified color
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cap.release()

    # If contours are found, return the coordinates of the first detected object
    if contours:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        return (x, y, w, h)
    
    return None
