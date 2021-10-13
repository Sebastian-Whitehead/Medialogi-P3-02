import cv2
import numpy as np
from ColorMask import *
from BlobTracking import BlobTracking

class ConnectedComponentMethod:
    def __init__(self):
        self.window_name = 'ConnectedComponentsMethod'
        self.blobTracking = BlobTracking(
            window_name=self.window_name,
            collisionType='dim',
            addBlobClick=1
        )

    def runManualMethod(self, originalImage: np.ndarray, lower: tuple, upper: tuple):
        processedImage = colorMaskManual(originalImage, lower, upper)
        return self.__continueMethod(originalImage, processedImage)


    def runAutoMethod(self, originalImage: np.ndarray, colSelector: str):
        processImage = colorMaskAuto(originalImage, colSelector)
        return self.__continueMethod(originalImage, processImage)

    def runNoMasking(self, originalImage: np.ndarray):
        processedImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
        processedImage = cv2.threshold(processedImage, 102, 255, cv2.THRESH_BINARY)[1]
        return self.__continueMethod(originalImage, processedImage)

    def __continueMethod(self, originalImage: np.ndarray, processedImage: np.ndarray):
        num_labels, labels = cv2.connectedComponents(processedImage)

        label_hue = np.uint8(179 * labels / np.max(labels))
        blank_ch = 255 * np.ones_like(label_hue)
        labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

        # Converting cvt to BGR
        labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

        # set bg label to black
        labeled_img[label_hue == 0] = 0

        blobs = []
        for n in range(1, num_labels):
            nonZeroX, nonZeroY = np.where(labels[:, :] == n)

            x, y = min(nonZeroY), min(nonZeroX)
            w, h = max(nonZeroY) - x, max(nonZeroX) - y

            blobs.append((x, y, w, h))

        filtredBlobs = []
        for blob in blobs:
            if blob[2] > 50 and blob[3] > 50:
                filtredBlobs.append(blob)
        blobs = filtredBlobs

        for blob in blobs:
            originalImage = cv2.rectangle(originalImage, (blob[0], blob[1]), (blob[0] + blob[2], blob[1] + blob[3]),
                                          (0, 0, 255), 1)


        self.blobTracking.run(blobs, originalImage)

        cv2.imshow('processedImage', labeled_img)
        cv2.imshow(self.window_name, originalImage)

        return blobs



