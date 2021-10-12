import cv2
from ColorMask import *

def SimpleBlobDetectorManual(originalImage: np.ndarray, lower: tuple, upper: tuple):

    processedImage = colorMaskManual(originalImage, lower, upper)
    return SimpleBlobDetectorContinue(originalImage, processedImage)

def SimpleBlobDetectorAuto(originalImage: np.ndarray, colSelector: str):
    processedImage = colorMaskAuto(originalImage, colSelector)
    return SimpleBlobDetectorContinue(originalImage, processedImage)

def SimpleBlobDetectorContinue(originalImage: np.ndarray, processedImage: np.ndarray):

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
    keypoints = detector.detect(processedImage)
    # Draw blobs on our image as red circles
    blobs = cv2.drawKeypoints(originalImage, keypoints, 0, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.imshow('SimpleBlobDetector', blobs)

    return keypoints
