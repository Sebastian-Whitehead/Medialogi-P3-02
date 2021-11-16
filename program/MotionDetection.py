import cv2
import time
import numpy as np

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

    #Selfmade dilation
<<<<<<< Updated upstream
    def DilSelf(self, img, kernel, iterations): #Give image, kernel size, number of iterations
        mid = int((kernel/2))   #How far away from the center it should look
        for i in range(iterations):  #Repeats the loop i amount of times
            for y, row in enumerate(img):
                for x, pixel in enumerate(row):
                    for x_step in range(kernel):  # Will times x kernel size.
                        x_check = x + (x_step - mid)   # Goes from -1, to 0, to 1 + x
                        if x_check < 0 or x_check >= img.shape[1]:  # if current x is outside the image
                            continue
                        for y_step in range(kernel):
                            y_check = y + (y_step - mid)  # Goes from -1, to 0, to 1 + y
                            if y_check < 0 or y_check >= img.shape[0]:  # if current y is outside the image
                                continue
                            if img[y_check, x_check] > 20:  # if any part of our kernel hits
                                img[y, x] = 255   # if the kernel hits, set the pixel to white 
        return img

    #Selfmade grayscale function
    def grayself(self, img):
        image = np.empty((img.shape[0], img.shape[1]), dtype=int) #Make an empty array with the correct size
        for y, row in enumerate(img):
            for x, pixels in enumerate(row):
                image[y][x] = (int(img[y][x][0]) + int(img[y][x][1]) + int(img[y][x][2]))/3.0  #Avg from RBG will be the colour
        return image
=======
    def DilSelf(self, img, kernel, iterations): #Gives image, kernel size, number of iterations
        mid = int((kernel/2))
        #print(type(img))
        for i in range(iterations):
            print(i)
            for x, row in enumerate(img):
                for y, pixel in enumerate(row):
                    for x_step in range(kernel):
                        x_check = x + (x_step - mid)
                        #print(type(img))
                        #print(img.size[1])
                        if x_check < 0 or x_check >= img.shape[1]:  # if current x is outside the image
                            continue
                        for y_step in range(kernel):
                            y_check = y + (y_step - mid)
                            #print(y_check)
                            if y_check < 0 or y_check >= img.shape[0]:  # if current y is outside the image
                                #print(y_check)
                                continue
                            if img[y_check, x_check] > 20:  # if any part of our kernel hits
                                img[y, x] = 255
                        #print(x,y)
        return img

>>>>>>> Stashed changes

    def run(self):

        cv2.putText(self.frame1, str(self.squatCount), (10, 600), self.font, 1, (255, 255, 255), 2)  # Write amount of squats

        diff = cv2.absdiff(self.frame1, self.frame2)  # find difference between first frame and 2nd frame
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)  # easier to find contours in gray
        #gray = self.grayself(diff)  Selfmade grayscale function - is slow
        #gray = gray.astype('uint8')  Changes dtype for selfmade grayscale function, required for the prog to run
        blur = cv2.GaussianBlur(gray, (5, 5), 0)  # blur to remove noise, this line might not matter for our purpose.
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)  # ignore black parts with thresholding

        # Dilates image, fill small holes. Three params (img, kernel, iterations)
        # None in kernels, means default 3x3 matrix, iterations, doing it three times, so 7x7
<<<<<<< Updated upstream
        dilated = cv2.dilate(thresh, None, iterations=7)
        #dilated = self.DilSelf(thresh, 3, 1) Selfmade dilation function
        cv2.imshow('dil', dilated)
        #cv2.waitKey(0)
        print(type(dilated))
=======
        #dilated = cv2.dilate(thresh, None, iterations=7)
        dilated = self.DilSelf(thresh, 3, 1)
        cv2.imshow('dil', dilated)
        #cv2.waitKey(0)

>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
    md = motion_detection(5, 2, cv2.VideoCapture(0, cv2.CAP_DSHOW))
    while True:
        cv2.imshow('feed', md.run())  # show the framerun()
        # Press Q on keyboard to  exit
        if cv2.waitKey(30) & 0xFF == ord('q'): break
=======
    motion_detection(5, 2, cv2.VideoCapture(0, cv2.CAP_DSHOW)).run()
>>>>>>> Stashed changes
