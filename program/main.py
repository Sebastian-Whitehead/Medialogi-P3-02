import numpy as np
from PIL import ImageFont, ImageDraw, Image
import cv2
import imageProcessing as IP

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

if cap.isOpened():
    # get vcap property
    frameWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float width
    frameHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float height
    frameFps = cap.get(cv2.CAP_PROP_FPS) # float fps

    print('Dim:', frameWidth, 'x', frameHeight, 'fps:', frameFps)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Image handling on "frame"
    frame = IP.cvtColor(frame, 'rgb')
    #frame = IP.thresholdStretching(frame)
    #frame = IP.threshold(frame, (20, 0, 0), (52, 9, 30), (89, 191, 255)) # Mask green color

    # Write counter on image
    feedbackText = 'Count: ' + str(0)
    textPosition, fontFace, fontScale, fontColor, thickness = (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 0, 0), 1
    #textPosition -= cv2.getTextSize(feedbackText, fontFace, fontScale, thickness)
    frame = cv2.putText(frame, feedbackText, textPosition, fontFace, fontScale, (0, 0, 0), thickness, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
frame.release()
cv2.destroyAllWindows()