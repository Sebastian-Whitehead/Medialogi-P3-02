# Import Python libraries
import cv2  # OpenCV
import numpy as np


# Mask for green objects in image using LAB (t = 115)
def colorMaskLAB(img: np.ndarray) -> np.ndarray:
    # Convert image to LAB
    LAB = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # BRG image to LAB color space
    LAB = LAB[:, :, 1]  # Extract 2. channel from LAB (A-channel)

    # cv2.imshow('LAB channel 1', LAB)

    # Threshold image
    threshold = 115  # Initialize of intensity threshold
    LAB[LAB < threshold] = 0  # Assign pixels less than threshold to 0
    LAB[LAB > threshold] = 255  # Assign pixels above threshold to 255
    LAB = cv2.bitwise_not(LAB)  # Convert img to binary

    # Remove noise and holes in objects
    LAB = cv2.erode(LAB, None, iterations=2)  # Erode to remove noise
    LAB = cv2.dilate(LAB, None, iterations=5)  # Dilate to remove holes

    # cv2.imshow('Color masking masking - LAB', LAB)

    return LAB  # Return binary img np.array


# Will only be called when running this file
# Used for testing functions in file
if __name__ == "__main__":
    img = cv2.imread("TestImages/Gloves1.png")  # Get image
    maskedImg = colorMaskLAB(img)  # Mask out green objects
    cv2.imshow('Color masking masking - LAB', maskedImg)  # Show masked img
    cv2.waitKey(0)  # Stop program to see image(s)
