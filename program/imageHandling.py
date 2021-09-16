import cv2

def cvtColor(frame, colScale):
    # Our operations on the frame come here
    colScale = colScale.lower()
    if colScale == 'rgb' or colScale == 'bgr':
        frame = frame
    elif colScale == 'grey' or colScale == 'gray':
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif colScale == 'hvs':
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    elif colScale == 'hls':
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    elif colScale == 'lab':
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    return frame