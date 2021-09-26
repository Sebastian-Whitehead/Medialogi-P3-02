import numpy as np
import cv2
import imageProcessing as IP
from imageProcessing.colorDetection import colorDetection as colorDetection

window_name = 'Training Assistent Computer'
cap = cv2.VideoCapture(0)

def nothing(x):
    pass

if not cap.isOpened():
    print("Cannot open camera")
    exit()
else:
    # get vcap property
    frameWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float width
    frameHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float height
    frameFps = cap.get(cv2.CAP_PROP_FPS) # float fps
    print('Camera connected:')
    print('Dim:', frameWidth, 'x', frameHeight, 'fps:', frameFps)

cv2.namedWindow(window_name)
cv2.createTrackbar('Lower threshold', window_name, 1, 10, nothing)
cv2.createTrackbar('Upper threshold', window_name, 1, 10, nothing)

def imageProcessing(originalFrame, frameCopy):
    frames = {'originalFrame': originalFrame, 'frameCopy': frameCopy}

    # Getting input from sliders
    lowerThresh = cv2.getTrackbarPos('Lower threshold', window_name)
    upperThresh = cv2.getTrackbarPos('Upper threshold', window_name)

    #frame = IP.cvtColor(frame, 'rgb')
    frames['blured'] = cv2.GaussianBlur(frameCopy, (3, 3), 0)
    #frame = IP.thresholdStretching(frame)

    originalFrameBlured = cv2.GaussianBlur(originalFrame, (7, 7), 0)
    frames['greenGloveMask'] = IP.threshold(originalFrameBlured, (0, 0, 0), (48, 30, 104), (78, 122, 255)) # Mask green gloves
    frames['greenGloveMask'] = cv2.cvtColor(frames['greenGloveMask'], cv2.COLOR_BGR2GRAY)
    #originalFrame = blobDetection(frames['greenGloveMask'], originalFrame)

    frames['edges'] = cv2.Canny(image=originalFrame, threshold1=100, threshold2=200)  # Canny Edge Detection

    # Show all available frames
    if False:
        for frame in frames:
            cv2.imshow(frame, frames[frame])
    return frames

while True:
    # Capture frame-by-frame
    ret, originalFrame = cap.read()
    originalFrame = cv2.flip(originalFrame, 1)
    frameCopy = originalFrame.copy()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame. Exiting ...")
        break

    #frames = imageProcessing(originalFrame, frameCopy)
    #originalFrame = frames['originalFrame']
    #frame = frameCopy
    frames = {}

    # print(blob.name)
    frames['colorDetected'] = colorDetection(originalFrame, 7, (0, 0, 0), (48, 30, 104), (78, 122, 255), 'greenGlove')
    #frame = cv2.rectangle(frame, (100, 100), (200, 150), (0, 0, 255), 1)

    # Write counter on image
    feedbackText = 'Count: ' + str(0)
    textPosition, fontFace, fontScale, fontColor, thickness = (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 0, 0), 2
    frame = cv2.putText(frame, feedbackText, textPosition, fontFace, fontScale, fontColor, thickness, cv2.LINE_AA)
    textPosition, fontFace, fontScale, fontColor, thickness = (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1.5, (255, 255, 255), 1
    frame = cv2.putText(frame, feedbackText, textPosition, fontFace, fontScale, fontColor, thickness, cv2.LINE_AA)

    # Display the resulting frame
   # cv2.imshow(window_name, frame)
    cv2.imshow(window_name, frames['colorDetected'])
    if cv2.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
frame.release()
cv2.destroyAllWindows()