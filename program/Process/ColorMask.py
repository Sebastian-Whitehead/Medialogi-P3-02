import cv2
import numpy as np


def colorMaskManual(img: np.ndarray, lower: tuple, upper: tuple) -> np.ndarray:
    # Convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)

    # Slice the color
    imask = mask > 0
    maskedImg = np.zeros_like(img, np.uint8)
    maskedImg[imask] = img[imask]

    image = maskedImg

    #cv2.imshow('Color masking', maskedImg)

    # Image to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # image = cv2.bitwise_not(image)  # Invert image

    # Convert image to binary
    (thresh, image) = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    image = cv2.erode(image, None, iterations=5)
    # Morph image
    kernel = np.ones((5, 5), np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    # Dilate image three times
    image = cv2.dilate(image, None, iterations=5)

    cv2.imshow('Processed image', image)  # Show processed image

    return image


def colorMaskLAB(img: np.ndarray) -> np.ndarray:

    LAB = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    LAB = LAB[:, :, 1]

    cv2.imshow('LAB channel 1', LAB)

    threshold = 115
    LAB[LAB < threshold] = 0
    LAB[LAB > threshold] = 255

    LAB = cv2.bitwise_not(LAB)

    LAB = cv2.erode(LAB, None, iterations=2)
    LAB = cv2.dilate(LAB, None, iterations=5)

    cv2.imshow('Color masking masking - LAB', LAB)
    return LAB
