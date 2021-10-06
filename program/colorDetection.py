import cv2
import numpy as np
from SimpleBlobDetector import SimpleBlobDetector, processImage
from connectedComponentsMethod import connectedComponentsMethod

def videoTest():
    cap = cv2.VideoCapture('TestImages/greensmall.mp4')

    frameCount = 0

    while True:
        # Capture frame-by-frame
        _, frame = cap.read()

        frameCount += 1

        # if frameCount % 5 == 0: # Skip frames

        blurLevel = 9

        lower = (48, 30, 104)
        upper = (78, 122, 255)

        lower = (53, 74, 68)
        upper = (121, 255, 255)
        type = 'greenGlove'
        lowerRes = 2

        # Pick which blob detector method to use
        # blobDetection(frame, blurLevel, lower, upper, type, lowerRes)
        processedImage = processImage(frame, lower, upper)
        #SimpleBlobDetector(frame, processedImage)
        connectedComponentsMethod(frame, processedImage)

        if cv2.waitKey(15) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()

    cv2.destroyAllWindows()


def nothing(value):
    pass


window_name = 'Window'
cv2.namedWindow(window_name)
cv2.createTrackbar('Lower threshold', window_name, 1, 255, nothing)
cv2.createTrackbar('Upper threshold', window_name, 1, 255, nothing)

videoTest()

while True:
    # Getting input from sliders
    lowerThresh = cv2.getTrackbarPos('Lower threshold', window_name)
    upperThresh = cv2.getTrackbarPos('Upper threshold', window_name)

    # blobDetection('pic', cv2.imread('TestImages/KingDomino1.jpg'), 9, (100, 154, 28), (158, 255, 215), 'Water', 1)
    # blobDetection('pic', cv2.imread('TestImages/KingDomino1.jpg'), 9, (40, 0, 104), (72, 255, 212), 'Grass', 1)
    # blobDetection('pic', cv2.imread('TestImages/KingDomino1.jpg'), 9, (43, 52, 12), (95, 238, 97), 'Forest', 1)
    # blobDetection('pic', cv2.imread('TestImages/KingDomino1.jpg'), 9, (24, 68, 95), (36, 139, 171), 'Dirt', 1)
    # blobDetection('pic', cv2.imread('TestImages/Gloves1.png'), 9, (48, 30, 104), (78, 122, 255), 'greenGlove', 1)
    SimpleBlobDetector(cv2.imread('TestImages/Gloves1.png'), 'pic', (48, 30, 104), (78, 122, 255))
