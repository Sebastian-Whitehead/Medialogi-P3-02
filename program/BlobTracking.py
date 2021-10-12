from math import sqrt

def BlobTracking(prevBlobs: dict, curBlobs: [float]) -> dict:

    # Make a dict for the next blobs
    nextBlobs = {}

    # Loop all previous blobs
    for i, prevBlob in enumerate(prevBlobs):
        # Save the label of this blob
        prevLabel = prevBlob
        # Get the coordination of this blob
        prevBlob = prevBlobs[prevBlob]
        # Calculate the middle position of this blob
        prevMiddle = getMiddle(prevBlob)
        # Set this blobs next buddy to None/Empty
        nextBlob = None

        # Loop all new blobs in current frame
        for j, curBlob in enumerate(curBlobs):
            # Get the middle coordination of this blob
            curMiddle = getMiddle(curBlob)
            # Calculate the distance from the middle of the previous blob to this one
            dist = getDistance(prevMiddle, curMiddle)
            # If this blobs distance is shorter than the current ones, ..
            if nextBlob == None or dist < getDistance(prevMiddle, nextBlob):
                # .. set this blob as the buddy
                nextBlob = curBlob

        # Mark the closest blob its buddy with the same label
        nextBlobs[prevLabel] = nextBlob

    # Return all the next blobs with their labels and coordination
    return nextBlobs

# Calculate the coordination for the middle of the blob
# Using ((x1,y2),(x2,y2)) (NOT ((x,y),(w,h)))
def getMiddle(blob: [float]) -> [float]:
    # Calculate x-coordination of the middle
    xMiddle = blob[0] + (blob[2] - blob[0]) / 2
    # Calculate y-coordination of the middle
    yMiddle = blob[1] + (blob[3] - blob[1]) / 2
    # Make into list
    middle = [xMiddle, yMiddle]
    # Return the middle coordination of the blob
    return middle

# Calculate the distance between two points in 2D space
def getDistance(p1: [float], p2: [float]) -> float:
    # Calculate the x coordinate
    x = float(p2[0]) - float(p1[0])
    # Calculate the y coordinate
    y = float(p2[1]) - float(p1[1])
    # Calculate and return the distance
    return sqrt(x ** 2 + y ** 2)