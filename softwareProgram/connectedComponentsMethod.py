import frameUI, ColorMask, cv2
from BlobTracking import BlobTracking
import numpy as np


# Blob class which keeps track of each blobs position and dimensions
class Blob:
    # Construct getting position and dimension of blob
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x, self.y = x, y  # Initialize blobs position
        self.w, self.h = w, h  # Initialize blobs dimensions


# Find green objects in an image
# Using OpenCV ConnectedComponentMethod and LAB image color space
class ConnectedComponentMethod:
    # Constructer initlizing a BlobTracking object with the arguments (total squat and sets)
    def __init__(self, squatTotal, setTotal):
        self.blobTracking = BlobTracking(  # Intializing a BlobTracking object
            squatTotal=squatTotal,  # Intilize total squat target
            setTotal=setTotal  # Intilize total set target
        )

    # Find green objects in image
    def run(self, originalImage: np.ndarray) -> np.ndarray:
        processedImage = ColorMask.colorMaskLAB(originalImage)  # Mask out green colors in image
        blobs = findBlobs(processedImage)  # Find blobs in the binary masked image
        blobs = mergeBlobs(blobs, 5)  # Merge blobs by overlay

        # Filter blobs being still too small at given threshold
        filteredBlobs = []  # Initiliz empty array for filtered blobs
        for blob in blobs:  # Loop all blobs
            if blob.w > 5 or blob.h > 5: filteredBlobs.append(blob)  # Append accepted blobs
        blobs = filteredBlobs  # Assign filtered blobs to "blobs"

        # Draw a red line over each blob found
        for blob in blobs:  # Loop all blobs
            frameUI.drawTrackingLine(originalImage, blob.x, blob.y, blob.w)  # Draw tracking line (frameUI)

        self.blobTracking.run(blobs, originalImage)  # Run blobTracking with blobs and the original image

        # cv2.imshow('ConnectedComponents', originalImage)

        return originalImage  # Return original image for visualization


# Find blobs in the binary masked image
def findBlobs(processedImage: np.ndarray) -> [Blob]:
    blobs = []  # Declare empty array for containing blobs
    num_labels, labels = cv2.connectedComponents(processedImage)  # Label image using grass-fire
    # "num_labels" is the amount of labels in the given image
    # "labels" is the labeled image as a 2D-array with each object having individual labels

    # Find position and dimension of all objects in labeled image
    for n in range(1, num_labels):  # Loop given all labels except 0
        # Get location of each value containing the specific label (n)
        nonZeroX, nonZeroY = np.where(labels[:, :] == n)  # "nonZero" is the location in the x- or y-axis

        # Get the position and dimension of given object
        x, y = min(nonZeroY), min(nonZeroX)  # Get minimal location of x- and y-axis
        w, h = max(nonZeroY) - x, max(nonZeroX) - y  # Get maximal location of x- and y-axis

        if 1 < w and 1 < h: blobs.append(Blob(x, y, w, h))  # Filter small blobs at given threshold

    return blobs  # Return array of all the blobs founds in image


# Check if two rectangles are overlapping with additional threshold
def checkOverLap(obj1, obj2, threshold: int) -> bool:
    if obj1.x - threshold < obj2.x + obj2.w + threshold:  # left1 vs right2
        if obj1.x + obj1.w + threshold > obj2.x - threshold:  # right1 vs left2
            if obj1.y - threshold < obj2.y + obj2.h + threshold:  # top1 vs bottom2
                if obj1.h + obj1.y + threshold > obj2.y - threshold:  # bottom1 vs top2
                    return True  # Return true if the rect. overlap
    return False  # Return false if the rect. do not overlap


# Merge two rectangles (blobs) into one if they overlap
def mergeBlobs(blobs, threshold: int) -> [Blob]:
    blobs = list(set(blobs))  # Copy blob list
    # Double loop all blobs
    for blob1 in list(blobs):
        for blob2 in list(blobs):
            if blob1 is not blob2 and checkOverLap(blob1, blob2, threshold):
                if blob1 in blobs: blobs.remove(blob1)  # Remove first blob
                if blob2 in blobs: blobs.remove(blob2)  # Remove second blob
                x, y = min(blob1.x, blob2.x), min(blob1.y, blob2.y)  # Get the minimal blob position
                w, h = max(blob1.w, blob2.w), max(blob1.h, blob2.h)  # Get maximum blob dimension
                blobs.append(Blob(x, y, w, h))  # Append new blob to blob array
    return blobs  # Return updated array of blobs


# Will only be called when running this file
# Used for testing functions in file
if __name__ == "__main__":
    img = cv2.imread("TestImages/Gloves1.png")  # Get image
    maskedImg = ConnectedComponentMethod(10, 2).run(img)  # Find green objects in img
    cv2.imshow('Color masking masking - LAB', maskedImg)  # Show masked img
    cv2.waitKey(0)  # Stop program to see image(s)
