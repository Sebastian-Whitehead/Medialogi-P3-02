import cv2
import numpy as np
from connectedComponentsMethod import ConnectedComponentMethod

def nothing(value):
    pass

def videoTest(trackingMethod):
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
        trackingMethod.runManualMethod(frame, lower, upper)

        # Wait ms to simulate framerate
        if cv2.waitKey(15) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()

    cv2.destroyAllWindows()




def main():
    CCM = ConnectedComponentMethod()
    videoTest(CCM)

if __name__ == '__main__':
    main()