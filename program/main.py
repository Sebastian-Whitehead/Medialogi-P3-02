import cv2, TonkoUI
from connectedComponentsMethod import ConnectedComponentMethod


# Main function running the live video from standard camera in users computer
# Running image processing and movement and/or color detection.
# Counts the amount of squats made by the user and shows it in the display.
def main(video):
    # Make tracking methods
    trackingMethod = ConnectedComponentMethod(window_name='Training Assistant Computer - LAB')  # LAB method

    cap = cv2.VideoCapture(video)  # Get video data

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
        print('Dim:', frameWidth, 'x', frameHeight, 'fps:', int(frameFps))

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
        
        trackingMethod.runLABMasking(frameCopy, frameCount)  # Run tracking method


        # Lower bar UI
#        TonkoUI.showSquatCountVisual(media=frameCopy, squatCount=trackingMethod.blobTracking.calcSquat.squatCount, squatTotal=10)
#        TonkoUI.showSquatCountText(media=frameCopy, squatCount=trackingMethod.blobTracking.calcSquat.squatCount, squatTotal=10)

        # Write counter on image
        text = 'Count: ' + str(trackingMethod.blobTracking.calcSquat.squatCount)  # Get counter text
        # UI.writeText(frameCopy, text, (10, 50), 1, 'left')  # Write the current amount of squats made

        cv2.imshow(trackingMethod.window_name, frameCopy)  # Show frame to the user

        frameCount += 1  # Skip frames

        if cv2.waitKey(15) == ord('q'): break

    # When everything done, release the capture
    originalFrame.release()
    cv2.destroyAllWindows()


if __name__ == '__main__': main(0)
