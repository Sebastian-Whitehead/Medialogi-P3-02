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

    return processImageContinue(maskedImg)


def colorMaskAuto(img: np.ndarray, colSelector: str) -> np.ndarray:
    pass


def processImageContinue(image: np.ndarray) -> np.ndarray:
    # Image to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Convert image to binary
    (thresh, image) = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Invert image
    image = cv2.bitwise_not(image)

    # Filter only the edges of image
    # image = cv2.Canny(image, 100, 200)

    # Morph image
    kernel = np.ones((7, 7), np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    # Floodfill image
    th, im_th = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY_INV)
    # Copy the thresholded image.
    im_floodfill = im_th.copy()
    # Mask used to flood filling.
    mask = np.zeros((im_th.shape[0] + 2, im_th.shape[1] + 2), np.uint8)
    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0, 0), 255)
    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    # Combine the two images to get the foreground.
    image = im_th | im_floodfill_inv

    # Show processed image
    #cv2.imshow('Processed image', image)

    return image
