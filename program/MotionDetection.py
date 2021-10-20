import cv2
import time

clip = cv2.VideoCapture(0)


def motion_detection(cap):
    count = 0  # count squats
    flag = 0
    start = (0, 307)  # line start pos
    end = (360, 307)  # line end pos
    liney = 1 #set line for squat acceptance
    linecheck = 1 #check how deep the squat is on the first squat (calibration)


    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    while cap.isOpened():
        cv2.putText(frame1, str(count), (10, 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        diff = cv2.absdiff(frame1, frame2)  # find difference between first frame and 2nd frame
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)  # easier to find contours in gray
        blur = cv2.GaussianBlur(gray, (5, 5), 0)  # blur to remove noise, this line might not matter for our purpose.
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)  # ignore black parts with thresholding
        dilated = cv2.dilate(thresh, None, iterations=3)  # Dilates image, fill small holes. Three params(img,kernel,iterations)
        # None in kernels, means default 3x3 matrix, iterations, doing it three times, so 7x7
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # find contours er lidt mere kompleks og der kan man komme ud for kun at skulle forklare grass fire
       # cv2.line(frame1, start, end, (0, 0, 255), 2)  # draws the line which the persons head has to go under

        for contour in contours:
            # save all coordinates of found contours
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 25000:  # if area is less than, then do nothing #6000ish if video, 16000 ish if webcam.
                #Jo tættere på man er på kameraet jo større skal det tal være. IKKE?
                continue
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)  # draw the rectangle
            cv2.putText(frame1, "status: {}".format("Movement"), (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 0, 0), 2)  # Text to show if we detect movement


            if y > linecheck and count == 0: #if flag is not -1, and y is higher than linecheck
                linecheck = y # make linecheck same as y
                liney = y-20 # set the line a less than y,
                start1 = (0, liney)  # line1 start pos
                end1 = (frame1.shape[1], liney)  # line1 end pos
            if "start1" and "end1" in locals():
                cv2.line(frame1, start1, end1, (255, 0, 0), 2)  # draws the line which the persons head has to go under




            if y > liney and flag == 1:  # Checks if we are under the line, accepted as a squat.
                flag = -1
            elif y < liney:
                if flag == -1:
                    count += 1
                    print(count)
                    flag = 0
                if flag == 0:
                    flag = 1

        #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2) # draws contours around moving object


        cv2.imshow('feed', frame1)  # show the frame
        frame1 = frame2
        ret, frame2 = cap.read()  # frame will get the next frame in the video (via "cap"). "Ret" will obtain return value from getting the video frame.


        if cv2.waitKey(15) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


#while (clip.isOpened()):
#    ret, frame = clip.read()
#    cv2.imshow('frame', frame)

#    if cv2.waitKey(4) == ord('q'):
#        break
#clip.release()

for i in range(5, 0, -1):
    time.sleep(1)
    print(i)
motion_detection(clip)
