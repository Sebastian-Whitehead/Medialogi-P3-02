import cv2
import numpy as np
from ColorMask import *
from BlobTracking import BlobTracking

class Blob:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class ConnectedComponentMethod:
    def __init__(self, window_name):
        self.window_name = window_name
        self.blobTracking = BlobTracking(
            window_name=self.window_name,
            collisionType='dim',
            addBlobClick=1
        )

    def runManualMethod(self, originalImage: np.ndarray, lower: tuple, upper: tuple, frameCount):
        processedImage = colorMaskManual(originalImage, lower, upper)
        return self.__continueMethod(originalImage, processedImage, frameCount)


    def runAutoMethod(self, originalImage: np.ndarray, colSelector: str, frameCount):
        processImage = colorMaskAuto(originalImage, colSelector)
        return self.__continueMethod(originalImage, processImage, frameCount)

    def __continueMethod(self, originalImage: np.ndarray, processedImage: np.ndarray, frameCount):

        num_labels, labels = cv2.connectedComponents(processedImage)

        blobs = []
        for n in range(1, num_labels):
            nonZeroX, nonZeroY = np.where(labels[:, :] == n)

            x, y = min(nonZeroY), min(nonZeroX)
            w, h = max(nonZeroY) - x, max(nonZeroX) - y

            # Filter small blobs
            if w > 25 and h > 25:
                blobs.append(Blob(x, y, w, h))

        blobs = mergeBlobs(blobs, 5)

        for blob in blobs:
            pos1, pos2 = (blob.x, blob.y), (blob.x + blob.w, blob.y + blob.h)
            originalImage = cv2.rectangle(originalImage, pos1, pos2, (0, 0, 255), 1)

        self.blobTracking.run(blobs, originalImage, frameCount)

        #cv2.imshow('ConnectedComponents', originalImage)

        return blobs

def checkOverLap(obj1, obj2, threshold: int) -> bool:
    if obj1.x - threshold < obj2.x + obj2.w + threshold:
        if obj1.x + obj1.w + threshold > obj2.x - threshold:
            if obj1.y - threshold < obj2.y + obj2.h + threshold:
                if obj1.h + obj1.y + threshold > obj2.y - threshold:
                    return True
    return False

def mergeBlobs(blobs, threshold: int):
    blobs = list(set(blobs))
    for blob1 in list(blobs):
        for blob2 in list(blobs):
            if blob1 is not blob2:
                if checkOverLap(blob1, blob2, threshold):
                    blob2.x = min(blob1.x, blob2.x)
                    blob2.w = max(blob1.w, blob2.w)
                    blob2.y = min(blob1.y, blob2.y)
                    blob2.h = max(blob1.h, blob2.h)
                    if blob1 in blobs:
                        blobs.remove(blob1)
    return blobs

