import cv2, UI
from connectedComponentsMethod import ConnectedComponentMethod

# Main function running the live video from standard camera in users computer
# Running image processing and movement and/or color detection.
# Counts the amount of squats made by the user and shows it in the display.
def main(trackingMethod):

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

        # Manual color thresholding
        lower = (40, 75, 120)
        upper = (75, 190, 250)

        # Pick which blob detector method to use
        trackingMethod.runManualMethod(frameCopy, lower, upper, frameCount)

        # Write counter on image
        # Get counter text
        text = 'Count: ' + str(trackingMethod.blobTracking.calcSquat.squatCount)
        UI.writeText(frameCopy, text, (10, 50), 1, 'left')

        # Display the resulting frame
        cv2.imshow(trackingMethod.window_name, frameCopy)

        frameCount += 1  # Skip frames

        if cv2.waitKey(15) == ord('q'):
            break

    # When everything done, release the capture
    originalFrame.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    
    window_name = 'Training Assistant Computer'  # Name of window name pop-up
    CCM = ConnectedComponentMethod(window_name)
    main(CCM)
