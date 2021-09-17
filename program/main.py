import numpy as np
import cv2
import imageProcessing as ip

# https://docs.opencv.org/4.5.1/dd/d43/tutorial_py_video_display.html

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Image handling on "frame"
    frame = ip.cvtColor(frame, 'rgb')
    frame = ip.tresholdStretching(frame)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
frame.release()
cv2.destroyAllWindows()