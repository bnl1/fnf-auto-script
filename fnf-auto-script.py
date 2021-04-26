import numpy as np
import cv2
from mss import mss
from PIL import Image
from pynput.keyboard import Key, Controller, Listener
from time import sleep

# Position of the scanned window
bounding_box = {'top': 128, 'left': 1000, 'width': 596, 'height': 185}

# The number here is the height in which the script detects arrows
row = 210 - bounding_box['top']

# Global coordinates for x 
arrows = {'left': 1075, 'down': 1227, 'up': 1372, 'right': 1527}

# Calculating local coordinations
for key in arrows:
    arrows[key] -= bounding_box['left']

# Default grey RGB (as [G, B, R])
grey = [173, 163, 135]
# Default grey in senpai level
grey_senpai = [200, 186, 162]

# Inicialization of screen grabber and virtual keyboard
sct = mss()
keyboard = Controller()

# Arrow keys
keys = {'left': Key.left, 'down': Key.down, 'up': Key.up, 'right': Key.right}


input("Ready?")

# Waits for the grey arrows to appear
while True:
    sct_img = sct.grab(bounding_box)
    arr = np.array(sct_img)
    if(list(arr[row][arrows['right']][:3]) == grey or list(arr[row][arrows['right']][:3]) == grey_senpai):
        break

# Main loop
while True:
    while True:
        # Grabs image
        sct_img = sct.grab(bounding_box)
        
        # Converts the image into numpy array
        arr = np.array(sct_img)
        
        # Shows it on screen (mainly for debugging)
        cv2.imshow('screen', arr)
        
        # Goes trough all positions to test if key should be pressed 
        for key in arrows:
            # Tests for not grey
            if(list(arr[row][arrows[key]][:3]) != grey and list(arr[row][arrows[key]][:3]) != grey_senpai):
                keyboard.press(keys[key])
                print(key)   
                sleep(0.04)
                break
           
        # Releases all keys
        for k in arrows:
            keyboard.release(keys[k]) 
        
        # Pressing q when focused on the 'camera' screen will end the loop (sometimes)
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break
    # For repeat
    input("Wanna continue?")


