import random, keyboard

import cv2, frameUI
from math import sqrt
from CalcSquat import CalcSquat

"""
USAGE
Call the 'BlobTracking' class before running the program
Call the 'run'-method each frame the program should track the blobs
"""


class BlobTracking():
    def __init__(self, window_name: str, collisionType: str):
        super().__init__()
        # Constant variables changing the programs threshold manually
        self.resetTimer = 2  # Time it takes for timer to reset (const)
        self.maxScore = 300  # Max similarity score threshold (const). -> Send to archived blob data

        self.window_name = window_name  # Set the window name of the window the tracking is enabled on
        self.colType = collisionType  # Collision type for detecting rect/mouse hit
        self.resetStartFrame = 0  # Holder for what frame to reset

        self.labelBlobs = {}  # Dict for labeled blobs
        self.clickable = True  # Holder for only clicking the screen once

        cv2.namedWindow(self.window_name)  # Get the window the tracking should be on
        cv2.setMouseCallback(self.window_name, self.__addLabel_event)  # Make a event clicker on the window

        self.calcSquat = CalcSquat()  # Initialize a CalcSquat object
        self.addBlobClick = 1  # Set button click to add blob labels to standard (1)

        self.frameCount = 0

        self.id = random.random()

    def setAddBlobClick(self, num: int):
        self.addBlobClick = num

    # Run the blob tracking
    def run(self, blobs, media):
        h, w, _ = media.shape

        self.__setBlobs(blobs)  # Set the current frames blobs
        self.__trackBlobs()  # Analyze the blobs

        # if key 'space' is pressed
        if keyboard.is_pressed('space'):
            print(f'Start program!')
            self.resetStartFrame = self.frameCount + 30 * self.resetTimer  # Reset system

        # Only show data if the counter is off
        self.frameCount += 1  # Set the current frame count
        if self.resetStartFrame - 1 < self.frameCount:
            if 0 < len(self.labelBlobs):
                self.calcSquat.run(self.labelBlobs, media)  # Run the calculate squat object
            else:
                frameUI.writeText(media, "Can't find hat..", [h, w], 1.5, 'center', (255, 255, 255))
        # Show counter and reset blob data, and labels
        else:
            pos = (int(media.shape[1] / 2), int(media.shape[0] / 2))
            text = 'Start in: ' + str(int((self.resetStartFrame - self.frameCount) / 30))  # Set the position of the text
            frameUI.writeText(media, text, pos, 1, 'center', (255, 255, 255))  # Write the text on the image
            self.calcSquat.__init__()  # Reset calculating squat data
            self.__setLabelsByPosition()  # Set labels on blobs

        return self.__writeLabel(media)  # Write the label on the screen

    # Add label to clicked blob
    def __addLabel_event(self, event, x, y, flags, params):
        # Left click
        if flags == self.addBlobClick and self.clickable:
            # self.__addLabelToBlobs((x, y))  # Check if blob is clicked on and add label (Commented)
            self.resetStartFrame = self.frameCount + 30 * self.resetTimer  # Reset system
            self.clickable = False  # Disable clicking before releasing

        # No click
        elif flags == 0:
            self.clickable = True  # Enable clicking on releasing

    # Check if the blob is clicked on and give the blob a label
    def __addLabelToBlobs(self, mousePos: [float]):
        for i, blob in enumerate(self.blobs):  # Go through all blobs
            if pointRectCollider(self.colType, mousePos, blob):  # Check rect/mouse collision

                size = len(self.labelBlobs)  # Get the length of all labeled blobs
                exists = False  # Check if the blob already exists

                # Check if the label already exists
                if size > 0:
                    for labelBlob in self.labelBlobs:
                        if self.labelBlobs[labelBlob] == blob:
                            exists = True

                # Label blob if not found any existing
                if not exists:
                    self.labelBlobs['label' + str(size)] = blob  # Give the blob a label
                    print('Label', size, 'made at', blob)  # Print label

    # Give the current blobs to the blob tracker
    def __setBlobs(self, blobs):
        self.blobs = blobs

    # Write the label of each blob on its rect
    def __writeLabel(self, media):
        # Only if there are any labeled blobs
        if len(self.labelBlobs) > 0:
            # Go through each labeled blob
            for blob in self.labelBlobs:
                values = self.labelBlobs[blob]  # Get the coordination of the blob
                text = blob.title()  # Get the label using the index
                pos = (values.x + int(values.w / 2), values.y - 5)
                frameUI.writeText(media, text, pos, 1, 'center', (0, 0, 255))

        return media  # Return the media/frame

    # Track all labeled blobs with the next blobs
    def __trackBlobs(self) -> dict:

        # Only if there are any blobs
        if len(self.labelBlobs):
            self.newLabelBlobs = {}  # Make a dict for the next blobs

            # Loop all previous blobs
            for j, prevBlob in enumerate(self.labelBlobs):
                prevLabel = prevBlob  # Save the label of this blob
                prevBlob = self.labelBlobs[prevLabel]  # Get the coordination of this blob
                self.__checkScore(prevLabel, prevBlob)  # Check current blobs for similarity score

            # Return all the next blobs with their labels and coordination
            self.labelBlobs = self.newLabelBlobs

    # Compare all blobs with each labeled blobs for a closest match
    def __checkScore(self, prevLabel, prevBlob):
        newBlob = curScore = nextScore = None  # Set this blobs next buddy to None/Empty

        # Loop all new blobs in current frame
        for i, curBlob in enumerate(self.blobs):
            # Each blob will get a score to compare
            if curBlob in self.blobs: curScore = calcScore(prevBlob, curBlob, method=self.colType)
            # Calculate the score for the next blob, if there is any
            if newBlob is not None and curScore is not None:
                # Calc. the score of the new blob
                if curBlob in self.blobs: nextScore = calcScore(prevBlob, newBlob, method=self.colType)
                if curScore < nextScore: newBlob = curBlob  # Set new buddy if score is lower than current
            else:
                newBlob = curBlob  # Set the current blob as next one, if there None

        # Check if the best score is less that tne max score threshold
        if newBlob is not None:
            if calcScore(prevBlob, newBlob, method=self.colType) < self.maxScore:
                # Mark the closest blob its buddy with the same label
                self.newLabelBlobs[prevLabel] = newBlob

    # Set the labels of blobs width predetermined positions relative to each other
    def __setLabelsByPosition(self):
        if len(self.blobs) > 0:
            # Label the highest blob 'head'
            sortedBlobs = sorted(self.blobs, key=lambda blob: blob.y)  # Sort blobs in regards of their y-coordinate
            self.labelBlobs['head'] = sortedBlobs[0]  # Label the first blob to 'head'


# Calculate the similarities of two blobs
# distance, dimensions
def calcScore(mainBlob: [float], otherBlob: [float], method: str) -> float:
    score = 0  # Set start score to zero

    # Calculate the distance between the two blobs
    mainMiddle = calcMiddle(method, mainBlob)  # Calculate the middle position of main blob
    otherMiddle = calcMiddle(method, otherBlob)  # Calculate the middle coordination of other blob
    score += calcDistance(mainMiddle, otherMiddle)  # Calc. the dist. from the middle the two blobs

    score += calcDimensionSim(mainBlob, otherBlob, method)  # Calculate the similarity in the two blobs dimensions

    return score  # Return the final score


# Calculate the similarity in the two blobs dimensions
def calcDimensionSim(mainBlob: [float], otherBlob: [float], method: str) -> float:
    similarity = 0  # Holder for similarity score
    # Calculate each difference of each value (x, y, w, h)
    for attr in ['x', 'y', 'w', 'h']:
        similarity += abs(getattr(mainBlob, attr) - getattr(otherBlob, attr))  # Calculate the difference
    return similarity  # Return the similarity


# Get collision of point and rectangle
# 'corners' will check with the corners of the rectangle ((x1,y2),(x2,y2))
# 'dim' will check with the width and height of the rectangle ((x,y),(w,h)))
def pointRectCollider(method, p, r):
    if method == 'corners' and r.x < p.x < r.w and r.y < p.y < r.h: return True
    if method == 'dim' and r.x < p.x < r.x + r.w and r.y < p.y < r.y + r.h: return True


# Calculate the coordination for the middle of the blob
# 'corners' will check with the corners of the rectangle ((x1,y2),(x2,y2))
# 'dim' will check with the width and height of the rectangle ((x,y),(w,h)))
def calcMiddle(method, blob: [float]) -> [float]:
    if method == 'corners':
        xMiddle = blob.x + (blob.w - blob.x) / 2  # Calculate x-coordination of the middle
        yMiddle = blob.y + (blob.h - blob.y) / 2  # Calculate y-coordination of the middle
        middle = [xMiddle, yMiddle]  # Make into list
        return middle  # Return the middle coordination of the blob
    elif method == 'dim':
        xMiddle = blob.x + blob.w / 2  # Calculate x-coordination of the middle
        yMiddle = blob.y + blob.h / 2  # Calculate y-coordination of the middle
        middle = [xMiddle, yMiddle]  # Make into list
        return middle  # Return the middle coordination of the blob


# Calculate the distance between two points in 2D space
def calcDistance(p1: [float], p2: [float]) -> float:
    x = float(p2[0]) - float(p1[0])  # Calculate the x coordinate
    y = float(p2[1]) - float(p1[1])  # Calculate the y coordinate
    return sqrt(x ** 2 + y ** 2)  # Calculate and return the distance
