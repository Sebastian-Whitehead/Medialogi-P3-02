import cv2
import numpy as np


def colorMask(img: np.ndarray, lower: tuple, upper: tuple) -> np.ndarray:
    # Convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)

    # Slice the color
    imask = mask > 0
    maskedImg = np.zeros_like(img, np.uint8)
    maskedImg[imask] = img[imask]

    return maskedImg


def SimpleBlobDetector(image, lower, upper):
    # Process image
    # Make a copy of the image
    originalImage = image.copy()
    # Threshold image with color
    image = colorMask(image, lower, upper)
    # Image to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Convert image to binary
    (thresh, image) = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # Invert image
    image = cv2.bitwise_not(image)
    # Filter only the edges of image
    # image = cv2.Canny(image, 100, 200)
    # Morph image
    # ------------------------------

    # Show processed image
    cv2.imshow('Processed image', image)

    # Blob detector
    params = cv2.SimpleBlobDetector_Params()

    # Blob detector - parameters
    params.filterByColor = False
    params.minThreshold = 10
    params.maxThreshold = 30
    params.blobColor = 0
    params.minArea = 100
    params.maxArea = 500000
    params.filterByCircularity = False
    params.filterByConvexity = False
    params.minCircularity = 100
    params.maxCircularity = 1000

    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)
    # Detect blobs
    keypoints = detector.detect(image)
    # Draw blobs on our image as red circles
    blobs = cv2.drawKeypoints(originalImage, keypoints, 0, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    print("Number of Circular Blobs: " + str(len(keypoints)))

    cv2.imshow('SimpleBlobDetector', blobs)

    return keypoints
