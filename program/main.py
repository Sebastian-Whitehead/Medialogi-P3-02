import cv2, UI
from connectedComponentsMethod import ConnectedComponentMethod


# Main function running the live video from standard camera in users computer
# Running image processing and movement and/or color detection.
# Counts the amount of squats made by the user and shows it in the display.
def main():

    # Make tracking methods
    trackingMethod1 = ConnectedComponentMethod(window_name='Training Assistant Computer - HSV')
    trackingMethod2 = ConnectedComponentMethod(window_name='Training Assistant Computer - LAB')
    trackingMethod3 = ConnectedComponentMethod(window_name='Training Assistant Computer - Both')

    cap = cv2.VideoCapture(0)  # Get video data

    # Check if the camera is open on the users computer
    if not cap.isOpened():
        print("Cannot open camera")
        exit()  # Exit program on error
    else:
        # Get vcap property
        frameWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float width
        frameHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float height
        frameFps = cap.get(cv2.CAP_PROP_FPS)  # float fps

        # Print camera information
        print('Camera connected:')
        print('Dim:', frameWidth, 'x', frameHeight, 'fps:', frameFps)

    frameCount = 0  # Frame counter

    # Run video
    while True:
        ret, originalFrame = cap.read()  # Capture frame-by-frame
        originalFrame = cv2.flip(originalFrame, 1)  # Flip frame to make it seem like a mirror
        frameCopy = originalFrame.copy()  # Make a copy of the originalFrame

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame. Exiting ...")
            break

        # Pick which blob detector method to use
        #trackingMethod1.runManualMethod(frameCopy, (40, 75, 120), (75, 190, 250), frameCount)
        #trackingMethod1.runManualMethod(frameCopy, (40, 6, 145), (125, 174, 255), frameCount)
        #trackingMethod1.runManualMethod(frameCopy, (40, 6, 55), (125, 222, 255), frameCount)
        #trackingMethod1.runManualMethod(frameCopy, (40, 6, 47), (125, 222, 255), frameCount)
        #trackingMethod1.runManualMethod(frameCopy, (40, 75, 120), (75, 190, 250), frameCount)

        trackingMethod2.runLABMasking(frameCopy, frameCount)
        # Write counter on image
        text = 'Count: ' + str(trackingMethod2.blobTracking.calcSquat.squatCount)  # Get counter text
        UI.writeText(frameCopy, text, (10, 50), 1, 'left')
        cv2.imshow(trackingMethod2.window_name, frameCopy)
        """

        trackingMethod3.runBoth(frameCopy, (40, 75, 120), (75, 190, 250), frameCount)
        # Write counter on image
        text = 'Count: ' + str(trackingMethod3.blobTracking.calcSquat.squatCount)  # Get counter text
        UI.writeText(frameCopy, text, (10, 50), 1, 'left')
        cv2.imshow(trackingMethod3.window_name, frameCopy)

        trackingMethod1.runManualMethod(frameCopy, (40, 75, 120), (75, 190, 250), frameCount)

        # Write counter on image
        text = 'Count: ' + str(trackingMethod1.blobTracking.calcSquat.squatCount)  # Get counter text
        UI.writeText(frameCopy, text, (10, 50), 1, 'left')

        cv2.imshow(trackingMethod1.window_name, frameCopy)  # Display the resulting frame
        """

        frameCount += 1  # Skip frames

        if cv2.waitKey(15) == ord('q'): break

    # When everything done, release the capture
    originalFrame.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
