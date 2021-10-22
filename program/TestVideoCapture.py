import cv2
import numpy as np
from connectedComponentsMethod import ConnectedComponentMethod


def main():
    # Video to test
    cap = cv2.VideoCapture('TestImages/greensmall.mp4')

    # Make tracking methods
    trackingMethod1 = ConnectedComponentMethod(window_name='Training Assistant Computer - HSV')
    trackingMethod2 = ConnectedComponentMethod(window_name='Training Assistant Computer - LAB')
    trackingMethod3 = ConnectedComponentMethod(window_name='Training Assistant Computer - Both')

    frameCount = 0  # Frame counter

    while True:
        # Capture frame-by-frame
        _, originalFrame = cap.read()
        frame = originalFrame.copy()

        frameCount += 1  # Skip frames

        # Manual color thresholding
        lower, upper = (53, 74, 68), (121, 255, 255)

        # Pick which blob detector method to use
        # trackingMethod1.runManualMethod(frame, (40, 75, 120), (75, 190, 250), frameCount)
        # cv2.imshow(trackingMethod1.window_name, frame)

        trackingMethod2.runLABMasking(frame, frameCount)
        cv2.imshow(trackingMethod2.window_name, frame)

        #trackingMethod3.runBoth(frame, (40, 75, 120), (75, 190, 250), frameCount)
        #cv2.imshow(trackingMethod3.window_name, frame)

        # Wait ms to simulate framerate
        if cv2.waitKey(15) & 0xFF == ord('q'): break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
