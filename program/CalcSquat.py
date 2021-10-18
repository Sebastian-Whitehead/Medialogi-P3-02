import json
import cv2


# Class for calculating and counting a squat with different blobs
# Right now it only works with one blob (The hat)
class CalcSquat:

    def __init__(self):
        self.resetData()

    def run(self, labelBlobs, media):
        self.getData(labelBlobs) # Get calculate squat data (CalcSquat)
        self.countSquat(labelBlobs) # Count each squat (CalcSquat)
        self.drawData(media) # Draw the guide lines (CalcSquat)

    # Run the program getting the min. and max. value of the blob
    def getData(self, labelBlobs):

        # Loop through all labeled blobs
        for n, blob in enumerate(labelBlobs):
            label = blob  # Set the label of the blob
            blob = labelBlobs[blob]  # Set the values of the blob
            # Check if the class already has this blob
            if label in self.blobData:
                thisBlobData = self.blobData[label]  # Get current blob from data
                # Compare current and new input. Use the min. and max.
                thisBlobData['min'] = min(thisBlobData['min'], blob[1])
                thisBlobData['max'] = max(thisBlobData['max'], blob[1] + blob[3])
                self.blobData[label] = thisBlobData  # Save the blob data
            else:
                self.blobData[label] = dict()  # Make dict for the blob
                # Set the top of the blob to min
                self.blobData[label]['min'] = blob[1]
                # Set the bottom of the blob to max
                self.blobData[label]['max'] = blob[1] + blob[3]

            self.blobData[label]['offset'] = int(self.blobData[label]['max'] /
                                                 self.blobData[label]['min'] * 7)
            self.blobData[label]['minDistance'] = blob[3]

    # Count the squat using the min. and max. thresholds
    def countSquat(self, labelBlobs):

        # Loop through all labeled blobs
        for n, blob in enumerate(labelBlobs):
            label = blob  # Set blobs label
            blob = labelBlobs[blob]  # Set blobs values
            thisBlobData = self.blobData[label]  # Get the blob data from the dataset

            # Only count if the min and max has correct position and not to close
            if thisBlobData['max'] > thisBlobData['minDistance'] + thisBlobData['min'] + thisBlobData['offset'] * 2:
                # Check if the blob is under the max level subtracted by the offset
                if (blob[1] + blob[3] > thisBlobData['max'] - thisBlobData['offset'] and
                        self.flag == 1):
                    self.flag = -1  # Set flag to -1 / DOWN
                    print('Down')
                # Check if the blob is above the min. value additional offset
                elif blob[1] < thisBlobData['min'] + thisBlobData['offset']:
                    # Check if the user has been DOWN / -1
                    if self.flag == -1:
                        self.squatCount += 1  # Count one squat
                        print('Squats:', self.squatCount)  # Print total counted squats
                        self.flag = 0  # Set flag to 0 / NEUTRAL
                    # Check if flag is NEUTRAL / 0
                    if self.flag == 0:
                        self.flag = 1  # Set flag to 1 / UP
                        print('Up')

    # Draw the threshold lines on the frame
    def drawData(self, media):

        # Loop all blob datas
        for n, blob in enumerate(self.blobData):
            label = blob  # Set blob label
            blobData = self.blobData[blob]  # Set blob data

            # Draw raw lines
            # Min. line
            drawLine(label + ': min', 0, blobData['min'], (0, 0, 255), media)
            # Max. line
            drawLine(label + ': max', 0, blobData['max'], (0, 0, 255), media)
            """
            """

            # Draw offset lines
            # Draw min. line with offset
            drawLine(label + ': min', 0, blobData['min'] + blobData['offset'], (0, 255, 0), media)
            # Draw max. line with threshold
            drawLine(label + ': max', 0, blobData['max'] - blobData['offset'], (0, 255, 0), media)

        return media  # Return the frame

    def resetData(self):
        self.blobData = dict()  # Make dict for holding squat data

        self.squatCount = 0  # Count how many squats the user have made
        self.flag = -1  # Flag holder for users current position

# Draw the threshold line with label
def drawLine(text, x, y, color, media):
    h, w, _ = media.shape  # Get the height and width of the frame

    cv2.line(media, (0, y), (w, y), color)  # Draw the line

    pos = (10, y - 10)  # Set the position of the text
    face, scale, thickness = cv2.FONT_HERSHEY_DUPLEX, 0.5, 1  # Set other attributes
    cv2.putText(media, text, pos, face, scale, color, thickness, cv2.LINE_AA)  # Write text on frame


if __name__ == '__main__':

    media = 'TestImages/greensmall.mp4',
    dataPath = 'manifacturedDataGreensmall.txt',

    blobs = []

    with open(dataPath) as json_file:
        if json_file:
            blobs = json.load(json_file)

            print('Loaded: ', blobs)
            print('')

    CalcSquat(blobs, media)
