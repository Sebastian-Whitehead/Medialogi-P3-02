import cv2
import numpy as np

def cvtColor(frame: np.ndarray, colScale: str) -> np.ndarray:
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

def thresholdStretching(frame: np.ndarray) -> np.ndarray:
    optimizedFrame = frame.copy()
    min = np.min(frame)
    max = np.max(frame)

    for x, rows in enumerate(frame):
        for y, cols in enumerate(rows):
            optimizedFrame[x][y] = 255/(max - min) * (frame[x][y] - min)

    return optimizedFrame