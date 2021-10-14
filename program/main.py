import cv2
from connectedComponentsMethod import ConnectedComponentMethod

# For handling the sliders.
# This should stay as it is ..
def nothing(x):
    pass


# Main function running the live video from standard camera in users computer
# Running image processing and movement and/or color detection.
# Counts the amount of squats made by the user and shows it in the display.
def main(trackingMethod):
    # Name of window name pop-up
    window_name = 'Training Assistent Computer'

    # Get video data
    cap = cv2.VideoCapture(0)

    # Check if the camera is open on the users computer
    if not cap.isOpened():
        print("Cannot open camera")
        # Exit program on error
        exit()
    else:
        # Get vcap property
        frameWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float width
        frameHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float height
        frameFps = cap.get(cv2.CAP_PROP_FPS)  # float fps

        # Print camera information
        print('Camera connected:')
        print('Dim:', frameWidth, 'x', frameHeight, 'fps:', frameFps)

    # Make and append slider to window frame
    cv2.namedWindow(window_name)
    cv2.createTrackbar('Lower threshold', window_name, 1, 10, nothing)
    cv2.createTrackbar('Upper threshold', window_name, 1, 10, nothing)

    # Run video
    while True:
        # Capture frame-by-frame
        ret, originalFrame = cap.read()

        # Flip frame to make it seem like a mirror
        originalFrame = cv2.flip(originalFrame, 1)

        # Make a copy of the originalFrame
        frameCopy = originalFrame.copy()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame. Exiting ...")
            break

        # Manual color thresholding
        # Manual Thresholding 1
        lower = (48, 30, 104)
        upper = (78, 122, 255)
        # Manual Thresholding 2
        lower = (53, 74, 68)
        upper = (121, 255, 255)

        # Color Selector type to automatic color masking
        colSelector = 'greenGlove'

        # Pick which blob detector method to use
        trackingMethod.runManualMethod(frameCopy, lower, upper)

        # Write counter on image
        # Get counter text
        feedbackText = 'Count: ' + str(0)
        # Make new attributes for background of the text
        textPosition, fontFace, fontScale, fontColor, thickness = (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 0, 0), 2
        # Write the background of the text on frame
        cv2.putText(frameCopy, feedbackText, textPosition, fontFace, fontScale, fontColor, thickness, cv2.LINE_AA)
        # Change attributes to front view of text
        fontColor, thickness = (255, 255, 255), 1
        # Write front view of text on frame
        cv2.putText(frameCopy, feedbackText, textPosition, fontFace, fontScale, fontColor, thickness, cv2.LINE_AA)

        # Display the resulting frame
        cv2.imshow(window_name, frameCopy)
        if cv2.waitKey(15) == ord('q'):
            break

    # When everything done, release the capture
    originalFrame.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    CCM = ConnectedComponentMethod()
    main(CCM)
