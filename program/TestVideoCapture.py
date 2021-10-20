import cv2
import numpy as np
from connectedComponentsMethod import ConnectedComponentMethod


def videoTest(trackingMethod):
    # Video to test
    cap = cv2.VideoCapture('TestImages/greensmall.mp4')


    frameCount = 0 # Frame counter

    while True:
        # Capture frame-by-frame
        _, originalFrame = cap.read()
        frame = originalFrame.copy()

        frameCount += 1  # Skip frames

        # Manual color thresholding
        lower, upper = (53, 74, 68), (121, 255, 255)

        # Pick which blob detector method to use
        trackingMethod.runManualMethod(frame, lower, upper, frameCount)

        cv2.imshow(trackingMethod.window_name, frame)

        # Wait ms to simulate framerate
        if cv2.waitKey(15) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def main():
    CCM = ConnectedComponentMethod('TestVideoCapture')
    videoTest(CCM)


if __name__ == '__main__':
    main()
