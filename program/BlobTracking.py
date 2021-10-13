import random
from math import sqrt
import cv2

"""
USAGE
Call the 'BlobTracking' class before running the program
Call the 'run'-method each frame the program should track the blobs

"""


class BlobTracking:
    def __init__(self, window_name: str, collisionType: str, addBlobClick: int):
        self.window_name = window_name  # Set the window name of the window the tracking is enabled on
        self.colType = collisionType  # Collision type for detecting rect/mouse hit
        self.addBlobClick = addBlobClick  # Button label for adding labels

        self.labelBlobs = {}  # Dict for labeled blobs
        self.clickable = True  # Holder for only clicking the screen once

        self.id = random.random()  # Blob trackers random ID

        cv2.namedWindow(self.window_name)  # Get the window the tracking should be on
        cv2.setMouseCallback(self.window_name, self.__addLabel_event)  # Make a event clicker on the window

    # Run the blob tracking
    def run(self, blobs, media):
        self.__setBlobs(blobs)  # Set the current frames blobs
        self.__trackBlobs()  # Analyze the blobs
        return self.__writeLabel(media)  # Write the label on the screen

    # Add label to clicked blob
    def __addLabel_event(self, event, x, y, flags, params):
        if flags == self.addBlobClick and self.clickable:  # (Left click)
            self.__addLabelToBlobs((x, y))  # Check if blob is clicked on
            self.clickable = False  # Disable clicking before releasing
        elif flags == 0:  # (No click)
            self.clickable = True  # Enable clicking on releasing

    # Check if the blob is clicked on and give the blob a label
    def __addLabelToBlobs(self, mousePos: [float]):
        for i, blob in enumerate(self.blobs):  # Go through all blobs
            if pointRectCollider(self.colType, mousePos, blob):  # Check rect/mouse collision
                size = len(self.labelBlobs)  # Get the length of all labeled blobs
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
                text = blob  # Get the label using the index
                # Make new attributes for background of the text
                face, scale, color, thickness = cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1
                pos = (values[0], values[1] - 5)
                # Write the background of the text on frame
                cv2.putText(media, text, pos, face, scale, color, thickness, cv2.LINE_AA)

        return media  # Return the media/frame

    # Track all labeled blobs with the next blobs
    def __trackBlobs(self) -> dict:

        # Only if there are any blobs
        if len(self.labelBlobs):
            nextBlobs = {}  # Make a dict for the next blobs

            # Loop all previous blobs
            for i, prevBlob in enumerate(self.labelBlobs):
                prevLabel = prevBlob  # Save the label of this blob
                prevBlob = self.labelBlobs[prevBlob]  # Get the coordination of this blob
                nextBlob = None  # Set this blobs next buddy to None/Empty

                # Loop all new blobs in current frame
                for j, curBlob in enumerate(self.blobs):
                    # Each blob will get a score to compare
                    curScore = calcScore(prevBlob, curBlob, method=self.colType)
                    # Calculate the score for the next blob, if there is any
                    if nextBlob is not None:
                        nextScore = calcScore(prevBlob, nextBlob, method=self.colType)
                        # If this blobs distance is shorter than the current ones, ..
                        if curScore < nextScore: nextBlob = curBlob # .. set this blob as the buddy
                    else:
                        nextBlob = curBlob # Set the current blob as next one, if there None

                nextBlobs[prevLabel] = nextBlob  # Mark the closest blob its buddy with the same label

            # Return all the next blobs with their labels and coordination
            self.labelBlobs = nextBlobs


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
    for n, mainBlobValue in enumerate(mainBlob):
        similarity += abs(mainBlobValue - otherBlob[n])  # Calculate the difference

    return similarity  # Return the similarity


# Get collision of point and rectangle
# 'corners' will check with the corners of the rectangle ((x1,y2),(x2,y2))
# 'dim' will check with the width and height of the rectangle ((x,y),(w,h)))
def pointRectCollider(method, point, rect):
    if method == 'corners':
        if rect[0] < point[0] < rect[2] and rect[1] < point[1] < rect[3]:
            return True
    elif method == 'dim':
        if rect[0] < point[0] < rect[0] + rect[2] and rect[1] < point[1] < rect[1] + rect[3]:
            return True
    return False


# Calculate the coordination for the middle of the blob
# 'corners' will check with the corners of the rectangle ((x1,y2),(x2,y2))
# 'dim' will check with the width and height of the rectangle ((x,y),(w,h)))
def calcMiddle(method, blob: [float]) -> [float]:
    if method == 'corners':
        # Calculate x-coordination of the middle
        xMiddle = blob[0] + (blob[2] - blob[0]) / 2
        # Calculate y-coordination of the middle
        yMiddle = blob[1] + (blob[3] - blob[1]) / 2
        # Make into list
        middle = [xMiddle, yMiddle]
        # Return the middle coordination of the blob
        return middle
    elif method == 'dim':
        # Calculate x-coordination of the middle
        xMiddle = blob[0] + blob[2] / 2
        # Calculate y-coordination of the middle
        yMiddle = blob[1] + blob[3] / 2
        # Make into list
        middle = [xMiddle, yMiddle]
        # Return the middle coordination of the blob
        return middle


# Calculate the distance between two points in 2D space
def calcDistance(p1: [float], p2: [float]) -> float:
    # Calculate the x coordinate
    x = float(p2[0]) - float(p1[0])
    # Calculate the y coordinate
    y = float(p2[1]) - float(p1[1])
    # Calculate and return the distance
    return sqrt(x ** 2 + y ** 2)
