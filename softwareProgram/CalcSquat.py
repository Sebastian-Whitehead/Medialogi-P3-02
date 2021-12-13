import frameUI, cv2


# Class for calculating and counting a squat with different blobs
# Right now it only works with one blob (The hat)
# Each blob having their own data, containing their minimun and maximal target
class CalcSquat:
    def __init__(self, squatTotal, setTotal):
        self.blobData = dict()  # Make dict for holding squat data

        self.squatCount = 0  # Counter holding number of squats the user have made
        self.setCount = 0  # Counter holding number of sets the user have made
        self.squatTotal = squatTotal  # Total target of squats
        self.setTotal = setTotal  # Total target of sets
        self.workoutComplete = False  # Boolean containing workout status

        self.direction = True  # Flag holder for users current position
        self.addSquat = False  # Letting the UI know a squat has been added
        self.calculationSquat = True  # Boolean knowing if the user is currently making a calibration squat

        # Later used variables explained
        # thisBlobData['min'] is the minimal value of the blob doing the calibration squat
        # thisBlobData['max'] is the maximal value of the blob doing the calibration squat
        # thisBlobData['offset'] is an offset from the actual "min" and "max" value helping the user
        # thisBlobData['minDistance'] is the minimal distance "min" and "max" must have for a squat to count

    # Run the squat counter
    def run(self, labelBlobs, media):
        if self.calculationSquat: self.__getData(labelBlobs)  # Get calculation squat data (CalcSquat)
        self.__countSquat(labelBlobs)  # Count each squat (CalcSquat)
        frameUI.drawData(media, self.blobData, self.direction)  # Draw the guide lines (CalcSquat)

    # Run the program getting the minimal and maximal value of the blob at any time
    def __getData(self, labelBlobs):

        # Loop through all labeled blobs
        for n, blob in enumerate(labelBlobs):
            label = blob  # Set the label of the blob
            blob = labelBlobs[blob]  # Set the values of the blob

            # Check if the class already has this blobs data
            if label in self.blobData:
                thisBlobData = self.blobData[label]  # Get current blob from data
                # Compare current and new input. Use the min. and max.
                thisBlobData['min'] = min(thisBlobData['min'], blob.y)  # Get minimal value of y-pos
                thisBlobData['max'] = max(thisBlobData['max'], blob.y)  # Get maximun value of y-pos
                self.blobData[label] = thisBlobData  # Save the blob data
            else:
                self.blobData[label] = dict()  # Make dict for the blob
                thisBlobData = self.blobData[label]  # Rename blobData
                thisBlobData['min'] = thisBlobData['max'] = blob.y  # Set top and bottom

                thisBlobData['minDistance'] = blob.h

            # Calculate offset value
            if not thisBlobData['min'] == 0:
                # Calculate the offset value (Min. / max. - const)
                thisBlobData['offset'] = int(thisBlobData['max'] / thisBlobData['min'] * 7)

    # Count the squat using the min. and max. thresholds
    def __countSquat(self, blobLabels):

        # Loop through all labeled blobs
        for n, blobLabel in enumerate(blobLabels):
            blob = blobLabels[blobLabel]  # Retrieve blob values to blob
            thisBlobData = self.blobData[blobLabel]  # Get the blob data from the dataset

            # Only count if the min and max has correct position and not to close
            blobDatMax_minValue = thisBlobData['minDistance'] + thisBlobData['min'] + thisBlobData['offset']
            if thisBlobData['max'] > blobDatMax_minValue:
                # Check if the blob is under the max level subtracted by the offset
                if blob.y > thisBlobData['max'] - thisBlobData['offset'] and self.direction:
                    self.direction = False  # Set flag to False / DOWN
                    print('Down')
                # Check if the blob is above the min. value additional offset
                elif blob.y < thisBlobData['min'] + thisBlobData['offset'] and self.direction is False:
                    # Check if the user has been DOWN / False
                    self.squatCount += 1  # Count one squat
                    self.addSquat = True  # Tell UI a squat has been added
                    self.calculationSquat = False  # Stop calculate the upper- and lower line
                    print('Squats:', self.squatCount)  # Print total counted squats
                    self.direction = True  # Set flag to Up / True

                    # Set counter and squat count reset
                    if self.squatCount >= self.squatTotal:
                        self.setCount += 1  # Add one to current sets
                        self.squatCount = 0  # Reset current squats counted

        # Check if the work out is complete
        if self.setCount >= self.setTotal:
            self.setCount = 0  # Reset current squats counted
            self.workoutComplete = True  # Assign workout status as complete

    # Reset to calibrate a new squat
    def resetTracking(self):
        self.blobData = dict()  # Make a new dict for holding squat data
        self.calculationSquat = True  # Start calculate the minimun- and maximal value
        self.direction = True  # Assign the direction as true/"up"
