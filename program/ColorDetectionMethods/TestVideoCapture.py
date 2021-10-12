import cv2
import numpy as np
from SimpleBlobDetector import *
from connectedComponentsMethod import *
from SelfmadeBlobDetection import *


def videoTest():
    # Video to test
    cap = cv2.VideoCapture('TestImages/greensmall.mp4')

    # Frame counter
    frameCount = 0

    while True:
        # Capture frame-by-frame
        _, frame = cap.read()


        # Skip frames
        frameCount += 1
        # if frameCount % 5 == 0:

        # Manual color thresholding
        # 1
        lower = (48, 30, 104)
        upper = (78, 122, 255)
        # 2
        lower = (53, 74, 68)
        upper = (121, 255, 255)

        # Color Selector type
        colSelector = 'greenGlove'

        # Pick which blob detector method to use
        #blobDetectionManual(frame, lower, upper)
        SimpleBlobDetectorManual(frame, lower, upper)
        connectedComponentsMethodManual(frame, lower, upper)

        # Wait ms to simulate framerate
        if cv2.waitKey(15) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()

    cv2.destroyAllWindows()


def nothing(value):
    pass


def main():
    window_name = 'Window'
    cv2.namedWindow(window_name)
    cv2.createTrackbar('Lower threshold', window_name, 1, 255, nothing)
    cv2.createTrackbar('Upper threshold', window_name, 1, 255, nothing)

    videoTest()

    while True:
        # Getting input from sliders
        lowerThresh = cv2.getTrackbarPos('Lower threshold', window_name)
        upperThresh = cv2.getTrackbarPos('Upper threshold', window_name)

        # blobDetection('pic', cv2.imread('TestImages/Gloves1.png'), 9, (48, 30, 104), (78, 122, 255), 'greenGlove', 1)
        SimpleBlobDetectorManual(cv2.imread('../TestImages/Gloves1.png'), (48, 30, 104), (78, 122, 255))


if __name__ == '__main__':
    main()
