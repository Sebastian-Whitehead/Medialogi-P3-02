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
    kernel = np.ones((5, 5), np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    th, im_th = cv2.threshold(image, 220, 255, cv2.THRESH_BINARY_INV);
    # Copy the thresholded image.
    im_floodfill = im_th.copy()
    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = im_th.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0, 0), 255)
    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    # Combine the two images to get the foreground.
    image = im_th | im_floodfill_inv

    # Show processed image
    cv2.imshow('Processed image', image)

    # Blob detector
    params = cv2.SimpleBlobDetector_Params()

    # Blob detector - parameters
    params.filterByColor = False
    params.minThreshold = 0
    params.maxThreshold = 255
    params.minArea = 10
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
