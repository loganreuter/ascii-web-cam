'''
ASCII Web Cam Project

By Logan Reuter

This project will capture the video stream from the webcam 
and turn it into a string of ASCII characters. The string of
characters are printed to the console.
'''

# used for image processing
import cv2 as cv

# used to clear the console before the new string is rewritten
from console.utils import cls

# used to find the size of the terminal
import os

# used for quick processing
import numpy as np

# A gray scale of ASCII characters
CHAR = " .'`^\",:;!i><~+_-?][}{1)(|/*#&8%B@$"
NUM_SYM = len(CHAR)

# determine the width and height of the terminal in use
WIDTH = os.get_terminal_size().columns
HEIGHT = os.get_terminal_size().lines

# connect to web cam
cap = cv.VideoCapture(0)

# receive a frame from the camera
_, frame = cap.read()

# determine the width and height of the frame
# then calculate the aspect ratio
VID_WIDTH = frame.shape[1]
VID_HEIGHT = frame.shape[0]

VID_RATIO = VID_HEIGHT / VID_WIDTH

# Determine how many lines and columns of the terminal to use
# use the smaller of the two values as baseline and use it to find
# the other value

Y = HEIGHT
X = int(HEIGHT / VID_RATIO)

if WIDTH < HEIGHT:
    X = WIDTH
    Y = int(WIDTH * VID_RATIO)

# in order to get a comparable image
# the frame needs to be simplified by taking a block of pixels
# and average the color values to assign it an ascii value 

# ncols and nrows are the number of pixels in the x and y directions
# in each of those blocks

nrows = int(VID_HEIGHT / Y)
ncols = int(VID_WIDTH / X)

while True:
    cls() # clear the console

    # capture a frame from the camera
    _, frame = cap.read()

    # convert frame to grayscale
    gray = np.array(cv.cvtColor(frame, cv.COLOR_BGR2GRAY))

    # empty string to store all the ascii characters
    symbols = ""

    # loop through each of the blocks
    # going in a left to right and top to bottom pattern
    for j in range(Y):
        for i in range(X):
            
            # determine the range of pixels in the block
            # for both the horizontal and vertical direction
            # check if the end of the block overflows the edge of the pixel
            start_col = i * ncols
            end_col = start_col + ncols

            if end_col > gray.shape[1] or end_col + ncols > gray.shape[1]:
                end_col = gray.shape[1]

            start_row = j * nrows
            end_row = start_row + nrows

            if end_row > gray.shape[0] or end_row + nrows > gray.shape[0]:
                end_row = gray.shape[0]

            # select the block from the frame
            selection = gray[start_row:end_row, start_col:end_col]

            # calculate the average value
            avg = np.mean(selection)
            
            # find a value 0-1 to represent how dark the pixel is
            # multiply that value by the number of characters in gradient
            # to get a corresponding index for the character string
            # make sure it is an int, so it can be used to index
            idx = int((avg / 255) * NUM_SYM)

            # add the character to the symbol string
            symbols += CHAR[idx]

        # after each row add a new line for formatting
        symbols += '\n'
    
    # print the symbols to the terminal after looping through all blocks
    print(symbols)