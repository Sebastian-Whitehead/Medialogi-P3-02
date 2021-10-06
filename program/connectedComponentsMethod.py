import cv2
import numpy as np

def connectedComponentsMethod(originalImage, processedImage):

    #gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #binaryImage = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)[1]
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
        nonZeroX, nonZeroY = np.where(labels[:,:] == n)

        x, y = min(nonZeroY), min(nonZeroX)
        w, h = max(nonZeroY) - x, max(nonZeroX) - y

        blobs.append((x, y, w, h))

    for blob in blobs:
        originalImage = cv2.rectangle(originalImage, (blob[0], blob[1]), (blob[0] + blob[2], blob[1] + blob[3]), (0, 0, 255), 1)

    cv2.imshow('ConnectedComponentsMethod', originalImage)

    return blobs