import cv2, frameUI
import numpy as np
from ColorMask import *
from BlobTracking import BlobTracking


class Blob:
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class ConnectedComponentMethod:
    def __init__(self, window_name):
        self.window_name = window_name
        self.blobTracking = BlobTracking(
            window_name=window_name,
            collisionType='dim'
        )

    def runManualMethod(self, originalImage: np.ndarray, lower: tuple, upper: tuple):
        processedImage = colorMaskManual(originalImage, lower, upper)
        return self.__continueMethod(originalImage, processedImage)

    def runLABMasking(self, originalImage: np.ndarray):
        processedImage = colorMaskLAB(originalImage)
        return self.__continueMethod(originalImage, processedImage)

    def runBoth(self, originalImage: np.ndarray, lower: tuple, upper: tuple):
        processedImage1 = colorMaskLAB(originalImage)
        processedImage2 = colorMaskManual(originalImage, lower, upper)
        merged = cv2.addWeighted(processedImage1, 1, processedImage2, 1, 0)
        cv2.imshow('Merged', merged)
        return self.__continueMethod(originalImage, merged)

    def __continueMethod(self, originalImage: np.ndarray, processedImage: np.ndarray):

        imageH, imageW, _ = originalImage.shape

        num_labels, labels = cv2.connectedComponents(processedImage)

        blobs = []
        for n in range(1, num_labels):
            nonZeroX, nonZeroY = np.where(labels[:, :] == n)

            x, y = min(nonZeroY), min(nonZeroX)
            w, h = max(nonZeroY) - x, max(nonZeroX) - y

            # Filter small blobs
            if 1 < w and 1 < h:
                blobs.append(Blob(x, y, w, h))
            if False:
                frameUI.writeText(originalImage, 'Looking for green hat,', [imageW / 2, imageH / 2 - 25], 1.5, 'center', (255, 255, 255))
                frameUI.writeText(originalImage, 'please, stand still..', [imageW / 2, imageH / 2 + 25], 1.5, 'center', (255, 255, 255))

        blobs = mergeBlobs(blobs, 5)

        for blob in blobs:
            pos1, pos2 = (blob.x, blob.y), (blob.x + blob.w, blob.y + blob.h)
            #originalImage = cv2.rectangle(originalImage, pos1, pos2, (0, 0, 255), 1) # Draw border on blobs

            pos2 = (blob.x + blob.w, blob.y)
            originalImage = cv2.line(originalImage, pos1, pos2, (0, 0, 255))

        self.blobTracking.run(blobs, originalImage)

        # cv2.imshow('ConnectedComponents', originalImage)

        return blobs


def checkOverLap(obj1, obj2, threshold: int) -> bool:
    if obj1.x - threshold < obj2.x + obj2.w + threshold:
        if obj1.x + obj1.w + threshold > obj2.x - threshold:
            if obj1.y - threshold < obj2.y + obj2.h + threshold:
                if obj1.h + obj1.y + threshold > obj2.y - threshold:
                    return True
    return False


def mergeBlobs(blobs, threshold: int):
    #blobs = list(set(blobs))
    for blob1 in list(blobs):
        for blob2 in list(blobs):
            if blob1 is not blob2:
                if checkOverLap(blob1, blob2, threshold):
                    if blob1 in blobs: blobs.remove(blob1)
                    if blob2 in blobs: blobs.remove(blob2)

                    x = min(blob1.x, blob2.x)
                    y = min(blob1.y, blob2.y)
                    w = max(blob1.w, blob2.w)
                    h = max(blob1.h, blob2.h)
                    blobs.append(Blob(x, y, w, h))
    return blobs
