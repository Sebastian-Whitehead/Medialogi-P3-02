import cv2, time, frameUI, keyboardInput


# Counting squats "Motion Detection"-method
# Comparing prevoius frame with current one to get a difference, which is the movement.
# Making contours arround the movement to get position of the movement
# Uses this to get a minimal y-position to calculate current movement on the y-axis
class motion_detection:
    def __init__(self, squatTotal: int, setTotal: int, cap):

        # Const variables
        self.offset = 20  # Offset from the actual line for the user to get a helping hand
        self.minDistance = 100  # Min. distance between upper- and lower line to count a squat

        # Dynamic variables
        self.squatCount = 0  # Current counted squats
        self.squatTotal = squatTotal  # Total target squat
        self.setCount = 0  # Current counted sets
        self.setTotal = setTotal  # Total target sets
        self.direction = False  # Current direction the user has to go next (t=down,f=up)
        self.workoutComplete = False  # Workout status, completion
        self.addSquat = False  # Tell the UI that a squat has been added

        self.upperLine = self.lowerLine = None  # The value of the upper- and lower line

        self.font = cv2.FONT_HERSHEY_SIMPLEX  # The font to write on the frame

        self.cap = cap  # Video capture
        _, self.frame1 = _, self.frame2 = self.cap.read()  # Read the frames from video capture

        # Reset tracker
        self.resetTimer = 2  # Time it takes for timer to reset (const)
        self.frameCount = 0  # Current frame count
        self.resetStartFrame = 0  # Holder for what frame to reset
        self.trackingRunning = False  # Bool keeping track of programming being active
        self.calculationSquat = False  # Bool keeping track of calibration squat

    # Run the program
    def run(self, cap):
        media = self.__trackMotion(cap)  # Track the motion in the frame
        self.__resetTracking(media)  # "Space" press to start countdown and reset
        return media  # Return media to show in UI

    # General tracking method running
    def __trackMotion(self, cap):
        diff = cv2.absdiff(self.frame1, self.frame2)  # find difference between first frame and 2nd frame
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)  # easier to find self.contours in gray
        blur = cv2.GaussianBlur(gray, (5, 5), 0)  # blur to remove noise, this line might not matter for our purpose.
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)  # ignore black parts with thresholding

        # Dilates image, fill small holes. Three params (img, kernel, iterations)
        # None in kernels, means default 3x3 matrix, iterations, doing it three times, so 7x7
        dilated = cv2.dilate(thresh, None, iterations=7)  # Dialate image to close holes
        # cv2.imshow('dil', dilated) # Show dilated image

        # find self.contours er lidt mere kompleks og der kan man komme ud for kun at skulle forklare grass fire
        self.contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if self.trackingRunning:
            for contour in self.contours:
                # save all coordinates of found self.contours
                (x, y, w, h) = cv2.boundingRect(contour)

                # self.__showMovement(x, y, w, h) # Show the movement of the user on the frame

                # if area is less than, then do nothing #6000 ish if video, 16000 ish if webcam.
                # Jo tættere på man er på kameraet jo større skal det tal være.
                if cv2.contourArea(contour) < 11000: continue  # Continue if there is not enough area
                # if 150 > w and 150 > h: continue # Continue if the contour is too small

                # Makes bottom line
                if self.calculationSquat:
                    if self.upperLine is None: self.upperLine = y  # Initilize the upper line
                    if self.lowerLine is None: self.lowerLine = y  # Initilize the lower line

                    self.upperLine = min(self.upperLine, y)  # Get the min. point of current and new y-value
                    self.lowerLine = max(self.lowerLine, y)  # Get the max. point of current and new y-value

                # Check the location of the user in regards of the lines
                if self.upperLine is not None and self.lowerLine is not None:
                    # Check if the two lines are separated enough in regards of "minDistance"
                    if self.upperLine + self.minDistance < self.lowerLine - self.offset:
                        # Checks if the user is below the bottom line and that is the next direction
                        if y > self.lowerLine - self.offset and self.direction == True:
                            self.direction = False  # Set the next direction to (up)
                            print(self.direction)

                        # Checks if the user is above the top line
                        if y < self.upperLine + self.offset and self.direction == False:
                            self.direction = True  # Set the next direction to (down)
                            self.squatCount += 1  # Add one squat to counter
                            self.addSquat = True  # Tell UI that a squat has been counted
                            self.calculationSquat = False  # Stop calibrating squat / update lines
                            print(f'{self.squatCount}/{self.squatTotal}', f'{self.setCount}/{self.setTotal}')

                    # Set squatCounter and squat squatCount reset
                    if self.squatCount >= self.squatTotal:
                        self.setCount += 1  # Count an additional set
                        self.squatCount = 0  # Reset the squat counter

            # Check if the counted sets is greater or same as target sets
            if self.setCount >= self.setTotal:
                self.setCount = 0  # Reset the set counter
                self.workoutComplete = True  # Set workout status to complete
                print(f'{self.workoutComplete=}')

            self.__showLines()  # Show upper- and lower line

        # cv2.drawContours(self.frame1, self.contours, -1, (0, 255, 0))  # draws self.contours around moving object

        returnFrame = self.frame1.copy()  # Copy the frame to return to feedback

        self.frame1 = self.frame2  # Convert the current frame to the previus one
        # frame will get the next frame in the video (via "cap").
        # "Ret" will obtain return value from getting the video frame.
        _, self.frame2 = self.cap.read()  # Get the next frame from the video capture

        return returnFrame  # Return the video frame for feedback

    # Show movement on the frame
    def __showMovement(self, x, y, w, h):
        frameUI.drawTrackingLine(self.frame1, x, y, w)  # Draw a tracking line over the user
        # cv2.rectangle(self.frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)  # draw the rectangle

        text = "status: {}".format("Movement")
        cv2.putText(self.frame1, text, (10, 50), self.font, 1, (255, 0, 0), 2)  # Text to show if we detect movement

    # Show the upper- and lower line on the frame
    def __showLines(self):
        # Only draw if they are set
        if self.upperLine != None and self.lowerLine != None and self.offset != None:
            # Convert data type to fit "drawData" input
            self.blobData = {
                'head': {
                    'min': self.upperLine,
                    'max': self.lowerLine,
                    'offset': self.offset
                }
            }
            # Draw the guide lines (CalcSquat)
            self.frame1 = frameUI.drawData(self.frame1, self.blobData, self.direction)

    # Check if the user press "space" to start counter and reset calibration
    def __resetTracking(self, media):
        self.frameCount += 1  # Count frames
        keyboardInput.reCalcTracking(self)  # Reset on "space"-click
        # Run calculating squats objects
        if self.resetStartFrame - 1 < self.frameCount:
            self.trackingRunning = True # Let the tracking method run
            # Check if the program is "empty" (reset)
            if self.calculationSquat is False and self.squatCount <= 0 and self.setCount <= 0:
                frameUI.pressSpaceToStart(media) # Tell the user to press "space" to start

        # Show counter and reset blob data, and labels
        else: self.__reset(media)

    # Start countdown and reset the calibration
    def __reset(self, media):
        self.upperLine = self.lowerLine = None # Reset lines
        self.direction = False # Set direction to up
        self.trackingRunning = False # Stop tracking
        self.calculationSquat = True # Do calibration squat (update lines)

        # Write countdown on scree
        pos = (int(media.shape[1] / 2), int(media.shape[0] / 2)) # Position center frame
        text = 'Start in: ' + str(int((self.resetStartFrame - self.frameCount) / 30))  # Set the position text
        frameUI.writeText(media, text, pos, 1, 'center', (255, 255, 255))  # Write the text on the image


if __name__ == '__main__':
    """
    for i in range(5, 0, -1):
        time.sleep(1)
        print(f'Start in {i}')
    """
    md = motion_detection(5, 2, cv2.VideoCapture(0, cv2.CAP_DSHOW)) # Test program
    while True:
        cv2.imshow('feed', md.run())  # show the framerun()
        # Press Q on keyboard to  exit
        if cv2.waitKey(30) & 0xFF == ord('q'): break
