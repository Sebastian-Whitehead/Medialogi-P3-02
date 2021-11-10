import cv2
import time

class motion_detection:
    def __init__(self, squatTotal: int, setTotal: int, cap):
        self.squatCount = 0  # squatCount squats
        self.squatTotal = squatTotal
        self.setCount = 0 # Count sets
        self.setTotal = setTotal
        self.direction = True
        self.offset = 20
        self.workoutComplete = False
        self.addSquat = False

        self.upperLine = self.lowerLine = None

        self.font = cv2.FONT_HERSHEY_SIMPLEX

        self.cap = cap

        _, self.frame1 = _, self.frame2 = self.cap.read()

    def run(self):

        cv2.putText(self.frame1, str(self.squatCount), (10, 600), self.font, 1, (255, 255, 255), 2)  # Write amount of squats

        diff = cv2.absdiff(self.frame1, self.frame2)  # find difference between first frame and 2nd frame
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)  # easier to find contours in gray
        blur = cv2.GaussianBlur(gray, (5, 5), 0)  # blur to remove noise, this line might not matter for our purpose.
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)  # ignore black parts with thresholding

        # Dilates image, fill small holes. Three params (img, kernel, iterations)
        # None in kernels, means default 3x3 matrix, iterations, doing it three times, so 7x7
        dilated = cv2.dilate(thresh, None, iterations=7)
        cv2.imshow('dil', dilated)

        # find contours er lidt mere kompleks og der kan man komme ud for kun at skulle forklare grass fire
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # save all coordinates of found contours
            (x, y, w, h) = cv2.boundingRect(contour)

            # if area is less than, then do nothing #6000ish if video, 16000 ish if webcam.
            # Jo tættere på man er på kameraet jo større skal det tal være. IKKE?
            if cv2.contourArea(contour) < 11000: continue # Continue if there is not enough area
            # if 150 > w and 150 > h: continue # Continue if the contour is too small

            # Draws line above users head
            left = (int(x + (w / 2) - 100), y)
            right = (int(x + (w / 2) + 100), y)
            cv2.line(self.frame1, left, right, (0, 0, 255), 2)
            # cv2.rectangle(self.frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)  # draw the rectangle
            text = "status: {}".format("Movement")
            cv2.putText(self.frame1, text, (10, 50), self.font, 1, (255, 0, 0), 2)  # Text to show if we detect movement

            # Makes bottom line
            if self.squatCount < 1:
                if self.upperLine is None: self.upperLine = y
                if self.lowerLine is None: self.lowerLine = y

                self.upperLine = min(self.upperLine, y)
                self.lowerLine = max(self.lowerLine, y)

            # Checks if youre below the bottom line
            if self.upperLine + 150 < self.lowerLine - self.offset:
                if y > self.lowerLine - self.offset and self.direction == False:
                    self.direction = True
                    print(self.direction)

                # Checks if youre above the top line
                if y < self.upperLine + self.offset and self.direction == True:
                    self.direction = False
                    self.squatCount += 1
                    self.addSquat = True
                    print(f'{self.squatCount}/{self.squatTotal}', f'{self.setCount}/{self.setTotal}')

                    # Set squatCounter and squat squatCount reset
                    if self.squatCount >= self.squatTotal:
                        self.setCount += 1
                        self.squatCount = 0
                        if self.setCount >= self.setTotal:
                            self.setCount = 0
                            self.workoutComplete = True
                            print(f'{self.workoutComplete=}')

        # Draw the upper line
        if self.upperLine is not None:
            start = (0, self.upperLine + self.offset)  # line1 start pos
            end = (self.frame1.shape[1], self.upperLine + self.offset)  # line1 end pos
            cv2.line(self.frame1, start, end, (255, 255, 0), 2)

        # Draw the lower line
        if self.lowerLine is not None:
            start = (0, self.lowerLine - self.offset)  # line1 start pos
            end = (self.frame1.shape[1], self.lowerLine - self.offset)  # line1 end pos
            cv2.line(self.frame1, start, end, (255, 255, 0), 2)

        #cv2.drawContours(self.frame1, contours, -1, (0, 255, 0))  # draws contours around moving object

        returnFrame = self.frame1.copy()

        self.frame1 = self.frame2
        # frame will get the next frame in the video (via "cap").
        # "Ret" will obtain return value from getting the video frame.
        _, self.frame2 = self.cap.read()

        return returnFrame

if __name__ == '__main__':
    """
    for i in range(5, 0, -1):
        time.sleep(1)
        print(f'Start in {i}')
    """
    md = motion_detection(5, 2, cv2.VideoCapture(0, cv2.CAP_DSHOW))
    while True:
        cv2.imshow('feed', md.run())  # show the framerun()
        # Press Q on keyboard to  exit
        if cv2.waitKey(30) & 0xFF == ord('q'): break
