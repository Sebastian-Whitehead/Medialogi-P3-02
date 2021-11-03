import cv2
import time



def motion_detection():
    count = 0  # count squats
    direction = True
    start = (0, 307)  # line start pos
    end = (360, 307)  # line end pos
    liney = 1  # set line for squat acceptance
    linecheck = 1  # check how deep the squat is on the first squat (calibration)

    font = cv2.FONT_HERSHEY_SIMPLEX

    # Read frames
    cap = cv2.VideoCapture(0)
    _, frame1 = _, frame2 = cap.read()

    while cap.isOpened():
        cv2.putText(frame1, str(count), (10, 600), font, 1, (255, 255, 255), 2) # Write amount of squats

        diff = cv2.absdiff(frame1, frame2)  # find difference between first frame and 2nd frame
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)  # easier to find contours in gray
        blur = cv2.GaussianBlur(gray, (5, 5), 0)  # blur to remove noise, this line might not matter for our purpose.
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)  # ignore black parts with thresholding

        # Dilates image, fill small holes. Three params (img, kernel, iterations)
        # None in kernels, means default 3x3 matrix, iterations, doing it three times, so 7x7
        dilated = cv2.dilate(thresh, None, iterations=7)

        # find contours er lidt mere kompleks og der kan man komme ud for kun at skulle forklare grass fire
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # cv2.line(frame1, start, end, (0, 0, 255), 2)  # draws the line which the persons head has to go under

        for contour in contours:
            # save all coordinates of found contours
            (x, y, w, h) = cv2.boundingRect(contour)
            # if area is less than, then do nothing #6000ish if video, 16000 ish if webcam.
            # Jo tættere på man er på kameraet jo større skal det tal være. IKKE?
            if cv2.contourArea(contour) < 11000: continue

            # Draws line above users head
            left = (int(x + (w / 2) - 100), y)
            right = (int(x + (w / 2) + 100), y)
            cv2.line(frame1, left, right, (0, 0, 255), 2)
            # cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)  # draw the rectangle
            text = "status: {}".format("Movement")
            cv2.putText(frame1, text, (10, 50), font, 1, (255, 0, 0), 2)  # Text to show if we detect movement

            # Makes bottom line
            if y > linecheck and count == 0:
                linecheck = y  # make linecheck same as y
                liney = y - 20  # set the line a less than y,
                start1 = (0, liney)  # line1 start pos
                end1 = (frame1.shape[1], liney)  # line1 end pos

            # Checks if youre below the bottom line
            if y > liney and direction == False:
                direction = True
                print(direction)

            # Checks if youre above the top line
            if y < liney and direction == True:
                direction = False
                count += 1
                print(count)
                print(direction)

        # Draws bottom line
        # draws the line which the persons head has to go under
        if "start1" and "end1" in locals(): cv2.line(frame1, start1, end1, (255, 255, 0), 2)

        cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)  # draws contours around moving object

        cv2.imshow('feed', frame1)  # show the frame
        # cv2.imshow('dil', dilated)

        frame1 = frame2
        # frame will get the next frame in the video (via "cap").
        # "Ret" will obtain return value from getting the video frame.
        _, frame2 = cap.read()

        if cv2.waitKey(15) == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    for i in range(5, 0, -1):
        time.sleep(1)
        print(f'Start in {i}')
    motion_detection()
