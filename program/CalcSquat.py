import frameUI


# Class for calculating and counting a squat with different blobs
# Right now it only works with one blob (The hat)
class CalcSquat:

    def __init__(self, squatTotal, setTotal):
        self.blobData = dict()  # Make dict for holding squat data

        self.squatCount = 0  # Count how many squats the user have made
        self.setCount = 0  # Count how many sets the user have made
        self.squatTotal = squatTotal  # Total target of squats
        self.setTotal = setTotal  # Total target of sets
        self.workoutComplete = False

        self.direction = True  # Flag holder for users current position
        self.position = (0, 0)  # Current (x, y) position
        self.addSquat = False  # The softwareProgram has added another squat (The UI has to use this information)

    def run(self, labelBlobs, media):
        if self.squatCount + self.setCount < 1: self.getData(labelBlobs)  # Get calculate squat data (CalcSquat)
        self.countSquat(labelBlobs)  # Count each squat (CalcSquat)
        frameUI.drawData(media, self.blobData, self.direction)  # Draw the guide lines (CalcSquat)

    # Run the softwareProgram getting the min. and max. value of the blob
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
                thisBlobData['max'] = max(thisBlobData['max'], blob.y)
                # thisBlobData['max'] = max(thisBlobData['max'], blob.y + blob.h) # (with height)
                self.blobData[label] = thisBlobData  # Save the blob data
            else:
                self.blobData[label] = dict()  # Make dict for the blob
                thisBlobData = self.blobData[label]
                thisBlobData['min'] = thisBlobData['max'] = blob.y  # Set top and bottom
                # thisBlobData['min'] = blob.y  # Set top
                # thisBlobData['max'] = blob.y + blob.h  # Set the bottom of the blob to max (with height)

                thisBlobData['minDistance'] = blob.h  # Min distance to count squat is the height of the head

            # Divide by zero protection
            if not thisBlobData['min'] == 0:
                thisBlobData['offset'] = int(thisBlobData['max'] / thisBlobData['min'] * 7)  # Min / max - ratio

    # Count the squat using the min. and max. thresholds
    def countSquat(self, blobLabels):

        # Loop through all labeled blobs
        for n, blobLabel in enumerate(blobLabels):
            blob = blobLabels[blobLabel]  # Retrieve blob values to blob
            thisBlobData = self.blobData[blobLabel]  # Get the blob data from the dataset

            # set the position of the blob to center x and current y coordinate
            if self.direction:
                self.position = (blob.x + (blob.w / 2), blob.y + blob.h)
            else:
                self.position = (blob.x + (blob.w / 2), blob.y)

            # Only count if the min and max has correct position and not to close
            # if thisBlobData['max'] > thisBlobData['minDistance'] + thisBlobData['min'] + thisBlobData['offset'] * 2: # (With height)
            if thisBlobData['max'] > thisBlobData['minDistance'] + thisBlobData['min'] + thisBlobData['offset']:
                # Check if the blob is under the max level subtracted by the offset
                if blob.y + blob.h > thisBlobData['max'] - thisBlobData['offset'] and self.direction:
                    self.direction = False  # Set flag to False / DOWN
                    print('Down')
                # Check if the blob is above the min. value additional offset
                elif blob.y < thisBlobData['min'] + thisBlobData['offset'] and self.direction is False:
                    # Check if the user has been DOWN / False
                    self.squatCount += 1  # Count one squat
                    self.addSquat = True
                    print('Squats:', self.squatCount)  # Print total counted squats
                    self.direction = True  # Set flag to Up / True

                    # Set counter and squat count reset
                    if self.squatCount >= self.squatTotal:
                        self.setCount += 1
                        self.squatCount = 0
                        if self.setCount >= self.setTotal:
                            self.setCount = 0
                            self.workoutComplete = True


if __name__ == '__main__':
    pass
