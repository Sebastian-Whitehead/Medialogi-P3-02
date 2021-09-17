import cv2
import numpy as np

def cvtColor(frame, colScale):
    # Our operations on the frame come here
    colScale = colScale.lower()
    if colScale == 'rgb' or colScale == 'bgr':
        frame = frame
    elif colScale == 'grey' or colScale == 'gray':
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif colScale == 'hvs':
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    elif colScale == 'hls':
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    elif colScale == 'lab':
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    return frame

def tresholdStretching(frame):
    optimizedFrame = frame.copy()
    min = np.min(frame)
    max = np.max(frame)

    for x, rows in enumerate(frame):
        for y, cols in enumerate(rows):
            optimizedFrame[x][y] = 255/(max - min) * (frame[x][y] - min)

    return optimizedFrame

def threshold(img, offset, lower, upper):
    ## convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.subtract(lower, offset), np.add(upper, offset))

    ## slice the color
    imask = mask > 0
    maskedImg = np.zeros_like(img, np.uint8)
    maskedImg[imask] = img[imask]

    return maskedImg