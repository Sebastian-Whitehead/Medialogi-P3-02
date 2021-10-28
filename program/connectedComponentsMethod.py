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

    def __continueMethod(self, originalImage: np.ndarray, processedImage: np.ndarray):
        # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # binaryImage = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)[1]
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

        for blob in blobs:
            originalImage = cv2.rectangle(originalImage, (blob[0], blob[1]), (blob[0] + blob[2], blob[1] + blob[3]),
                                          (0, 0, 255), 1)

        self.blobTracking.run(blobs, originalImage)

        cv2.imshow(self.window_name, originalImage)

        return blobs



