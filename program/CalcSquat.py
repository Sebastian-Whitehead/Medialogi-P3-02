import json, cv2, UI


# Class for calculating and counting a squat with different blobs
# Right now it only works with one blob (The hat)
class CalcSquat:

    def __init__(self):
        self.resetData()

    def run(self, labelBlobs, media):
        if self.squatCount < 2: self.getData(labelBlobs)  # Get calculate squat data (CalcSquat)
        self.countSquat(labelBlobs)  # Count each squat (CalcSquat)
        self.drawData(media)  # Draw the guide lines (CalcSquat)

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
                thisBlobData['min'] = min(thisBlobData['min'], blob.y)
                thisBlobData['max'] = max(thisBlobData['max'], blob.y + blob.h)
                self.blobData[label] = thisBlobData  # Save the blob data
            else:
                self.blobData[label] = dict()  # Make dict for the blob
                thisBlobData = self.blobData[label]
                thisBlobData['min'] = blob.y  # Set the top of the blob to min
                thisBlobData['max'] = blob.y + blob.h  # Set the bottom of the blob to max

            thisBlobData['offset'] = int(thisBlobData['max'] / thisBlobData['min'] * 7)
            thisBlobData['minDistance'] = blob.h

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
                if (blob.y + blob.h > thisBlobData['max'] - thisBlobData['offset'] and
                        self.flag == 1):
                    self.flag = -1  # Set flag to -1 / DOWN
                    print('Down')
                # Check if the blob is above the min. value additional offset
                elif blob.y < thisBlobData['min'] + thisBlobData['offset']:
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

            min = blobData['min']
            max = blobData['max']
            offset = blobData['offset']

            """
            # Draw raw lines
            color = (0, 0, 255)
            UI.drawLine(label + ': min', 0, min, color, media) # Min. line
            UI.drawLine(label + ': max', 0, max, color, media) # Max. line
            """

            # Draw offset lines
            color = (0, 255, 0)
            UI.drawLine(label + ': min', 0, min + offset, color, media)  # Min. line with offset
            UI.drawLine(label + ': max', 0, max - offset, color, media)  # Max. line with threshold

        return media  # Return the frame

    def resetData(self):
        self.blobData = dict()  # Make dict for holding squat data

        self.squatCount = 0  # Count how many squats the user have made
        self.flag = -1  # Flag holder for users current position


if __name__ == '__main__':
    pass
