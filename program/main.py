import cv2, TonkoUI
from connectedComponentsMethod import ConnectedComponentMethod


# Main function running the live video from standard camera in users computer
# Running image processing and movement and/or color detection.
# Counts the amount of squats made by the user and shows it in the display.
def main(videoSource):

    # Get video data
    cap = cv2.VideoCapture(videoSource)

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

    # Lower bar UI
    squatTotal = 10
    TonkoUI.runLowerBarUI(cap, 0, squatTotal=squatTotal)

if __name__ == '__main__':
    main(0)
