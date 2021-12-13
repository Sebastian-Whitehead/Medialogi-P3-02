import cv2, frameUI, keyboardInput
from math import sqrt
from CalcSquat import CalcSquat

"""
USAGE
Call the 'BlobTracking' class before running the softwareProgram
Call the 'run'-method each frame the softwareProgram should track the blobs
"""


# Keep track of multiple blobs knowing which of them are which
class BlobTracking():
    def __init__(self, squatTotal: int, setTotal: int):

        # Constant variables changable variables
        self.maxScore = 300  # Max similarity score (const) (s=300)
        self.resetTimer = 2  # Time it takes for timer to reset (const) (s=2)

        self.labelBlobs = {}  # Dict. for labeled blobs
        self.archivedBlobs = {}  # Dict. for archived blobs
        self.frameCount = 0  # Current frame counter
        self.resetStartFrame = 0  # Holder for what frame to reset
        self.calcSquat = CalcSquat(squatTotal, setTotal)  # Initialize a CalcSquat object

    # Run the blob tracking
    def run(self, blobs, media):
        self.blobs = blobs  # Set the current frames blobs
        self.__trackBlobs()  # Analyze the blobs
        self.__resetTracker(media)  # Reset tracking
        return self.__writeLabel(media)  # Write the label on the screen

    # Write the label of each blob on its rect
    def __writeLabel(self, media):
        # Only if there are any labeled blobs
        if len(self.labelBlobs) > 0:
            # Go through each labeled blob
            for blob in self.labelBlobs:
                values = self.labelBlobs[blob]  # Get the coordination of the blob
                text = blob.title()  # Get the label using the index
                pos = (values.x + int(values.w / 2), values.y - 5)  # Position text center/over of blob
                frameUI.writeText(media, text, pos, 1, 'center', (0, 0, 255))

        return media  # Return the media/frame

    # Track all labeled blobs with the next blobs
    def __trackBlobs(self) -> dict:

        if len(self.labelBlobs):
            self.newLabelBlobs = {}  # Make a dict for the next blobs
            self.unusedLabels = self.labelBlobs.copy()  # Copy labeled blobs

            # Loop all previous blobs
            for j, prevBlob in enumerate(self.labelBlobs):
                prevLabel = prevBlob  # Save the label of this blob
                prevBlob = self.labelBlobs[prevLabel]  # Get the coordination of this blob
                self.__checkScore(prevLabel, prevBlob)  # Check current blobs for similarity score

            if not len(self.unusedLabels) == 0:
                self.archivedBlobs = self.unusedLabels.copy()  # Copy unusedLabels
                # print(self.unusedLabels)
                # print(f"Unused blobs remaining \n")
            else:
                self.archivedBlobs = {}  # Empty archived blobs

            # Return all the next blobs with their labels and coordination
            self.labelBlobs = self.newLabelBlobs  # Assign new labels to labeled blobs
            self.labelBlobs = {**self.labelBlobs, **self.archivedBlobs}  # Merge labeled and arhcived blobs

    # Compare all blobs with each labeled blobs for a closest match
    def __checkScore(self, prevLabel, prevBlob):
        newBlob = curScore = nextScore = None  # Set this blobs next buddy to None/Empty

        # Loop all new blobs in current frame
        for i, curBlob in enumerate(self.blobs):
            # Each blob will get a score to compare
            if curBlob in self.blobs:
                curScore = calcScore(prevBlob, curBlob)

            # Calculate the score for the next blob, if there is any
            if newBlob is not None and curScore is not None:
                # Calculate the score of the next blob
                if curBlob in self.blobs:
                    nextScore = calcScore(prevBlob, newBlob)

                # Set new buddy if score is lower than current
                if curScore < nextScore:
                    newBlob = curBlob
            else:
                newBlob = curBlob  # Set the current blob as next one, if there None

        # Check if the best score is less that tne max score threshold
        if newBlob is not None:
            if calcScore(prevBlob, newBlob) < self.maxScore:
                # Mark the closest blob its buddy with the same label
                self.newLabelBlobs[prevLabel] = newBlob
                self.unusedLabels.pop(prevLabel)  # Remove the blob from unused labeled blobs

    # Set the labels of blobs width predetermined positions relative to each other
    def __setLabelsByPosition(self, media):
        if len(self.blobs) > 0:
            pos = (int(media.shape[1] / 2), int(media.shape[0] / 2))  # Center text in middle of frame
            text = 'Start in: ' + str(int((self.resetStartFrame - self.frameCount) / 30))  # Set the position text
            frameUI.writeText(media, text, pos, 1, 'center', (255, 255, 255))  # Write the text on the image

            # Label the highest position (lowest y-value) blob "head"
            # Sort blobs in regards of their y-coordinate
            sortedBlobs = sorted(self.blobs, key=lambda blob: blob.y)
            self.labelBlobs['head'] = sortedBlobs[0]  # Label the first blob to "head"

    # Reset tracking of green hat and upper-/lower line
    def __resetTracker(self, media):

        self.frameCount += 1  # Count frames

        # Run calculating squats objects
        if self.resetStartFrame - 1 < self.frameCount:
            # Let the user know, the program cannot find any green blobs in frame
            if 0 >= len(self.blobs):
                pos = (int(media.shape[1] / 2), int(media.shape[0] / 2))  # Position text in center of screen
                frameUI.writeText(media, "Can't find hat..", pos, 1.5, 'center', (255, 255, 255))
                return  # Stop method as it cannot work without a green object in frame

            # Let program run, when it can see a green object (bug = cannot start without any blobs)
            if 0 < len(self.labelBlobs):
                self.calcSquat.run(self.labelBlobs, media)
            # Write "Press space" text, to find "head" blob
            else:
                frameUI.pressSpaceToStart(media)

            keyboardInput.reCalcTracking(self)  # Reset green hat and lines on "space"-click

        # Show counter and reset blob data, and labels
        else:
            self.__setLabelsByPosition(media)  # Set labels on blobs
            self.calcSquat.resetTracking()  # Reset calculating squat data


# Calculate the similarities of two blobs
# distance, dimensions
def calcScore(mainBlob: [float], otherBlob: [float]) -> float:
    score = 0  # Set start score to zero
    # Calculate the distance between the two blobs
    mainMiddle = calcMiddle(mainBlob)  # Calculate the middle position of main blob
    otherMiddle = calcMiddle(otherBlob)  # Calculate the middle coordination of other blob

    score += calcDistance(mainMiddle, otherMiddle)  # Calc. the dist. from the middle the two blobs
    score += calcDimensionSim(mainBlob, otherBlob)  # Calculate the similarity in the two blobs dimensions
    return score  # Return the final score


# Calculate the similarity in the two blobs dimensions
def calcDimensionSim(mainBlob: [float], otherBlob: [float]) -> float:
    similarity = 0  # Holder for similarity score
    # Calculate each difference of each value (x, y, w, h)
    for attr in ['x', 'y', 'w', 'h']:
        distance = getattr(mainBlob, attr) - getattr(otherBlob, attr)  # Calculate the difference
        similarity += abs(distance)  # Make distance absolute
    return similarity  # Return the similarity


# Get collision of point and rectangle
def pointRectCollider(p, r):
    if r.x < p.x < r.x + r.w and r.y < p.y < r.y + r.h: return True


# Calculate the coordination for the middle of the blob
def calcMiddle(blob: [float]) -> [float]:
    xMiddle = blob.x + blob.w / 2  # Calculate x-coordination of the middle
    yMiddle = blob.y + blob.h / 2  # Calculate y-coordination of the middle
    middle = [xMiddle, yMiddle]  # Make into list
    return middle  # Return the middle coordination of the blob


# Calculate the distance between two points in 2D space
def calcDistance(p1: [float], p2: [float]) -> float:
    x = float(p2[0]) - float(p1[0])  # Calculate the x coordinate
    y = float(p2[1]) - float(p1[1])  # Calculate the y coordinate
    return sqrt(x ** 2 + y ** 2)  # Calculate and return the distance
