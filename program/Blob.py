import cv2
import imageProcessing as IP
import math


class Blob:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 0
        self.h = 0
        Blob.blobThreshold = 100  # 0 <

    def setThreshold(blobThreshold):
        Blob.blobThreshold = blobThreshold

    def print(self):
        print(self.x, self.y, self.w, self.h)


def mergeBlobs(blobs):
    blobs = list(set(blobs))
    for blob1 in list(blobs):
        for blob2 in list(blobs):
            if blob1 is not blob2:
                if blob1.x - Blob.blobThreshold < blob2.x + blob2.w and blob1.x + blob1.w + Blob.blobThreshold > blob2.x and blob1.y - Blob.blobThreshold < blob2.y + blob2.h and blob1.h + blob1.y + Blob.blobThreshold > blob2.y:
                    blob2.x = min(blob1.x, blob2.x)
                    blob2.w = max(blob1.w, blob2.w)
                    blob2.y = min(blob1.y, blob2.y)
                    blob2.h = max(blob1.h, blob2.h)
                    blobs.remove(blob1)
    return blobs

def show(blobs, originalFrame, frame):
    for blob in blobs:
        detectedImage = cv2.rectangle(originalFrame.copy(), (blob.x, blob.y), (blob.x + blob.w, blob.y + blob.h), (0, 0, 255), 1)
        cv2.imshow('originalFrame', detectedImage)
        cv2.waitKey(5)

def blobDetection2(frame, originalFrame):
    blobs = []
    for y, row in enumerate(frame):
        # print(y, ':', len(frame))

        # if 0 >= sum(row): # Skips row if all black (Makes it slower??)
            # continue
        #show(blobs, originalFrame, frame)
        for x, pixel in enumerate(row):
            # if 0 >= sum(row[x:]): # Skips rest of black pixels in row (Makes it slower??)
                # continue
            #originalFrame[y][x] = 0
            if 0 < pixel:
                blobFound = False
                for blob in blobs:
                    if not (x > blob.x and blob.x + blob.w > x and y > blob.y and blob.y + blob.h > y):
                        dist1 = math.dist((blob.x, blob.y), (x, y))
                        dist2 = math.dist((blob.x + blob.w, blob.y + blob.h), (x, y))
                        dist3 = math.dist((blob.x, blob.y + blob.h), (x, y))
                        dist4 = math.dist((blob.x + blob.w, blob.y), (x, y))
                        dist = min(dist1, dist2, dist3, dist4)
                        if dist < Blob.blobThreshold:
                            blob.x = min(x, blob.x)
                            blob.w = max(x - blob.x, blob.w)
                            blob.y = min(y, blob.y)
                            blob.h = max(y - blob.y, blob.h)
                            blobFound = True
                            break
                if not blobFound:
                    blob = Blob(x, y)
                    blobs.append(blob)
    # Blobs merge on overlap
    if 1 < len(blobs):
        blobs = mergeBlobs(blobs)
    detectedImage = originalFrame.copy()
    for blob in blobs:
        detectedImage = cv2.rectangle(detectedImage, (blob.x, blob.y), (blob.x + blob.w, blob.y + blob.h), (0, 0, 255), 1)
    return detectedImage

def testCode(window_name):
    originalFrame = cv2.imread('../handskerBillede.png', cv2.IMREAD_UNCHANGED)
    height, width, channels = originalFrame.shape
    imageProcess = originalFrame.copy()

    # LOWER RESOLUTION
    imageProcess = cv2.GaussianBlur(imageProcess, (7, 7), 0)
    imageProcess = IP.threshold(imageProcess, (0, 0, 0), (48, 30, 104), (78, 122, 255))  # Mask green gloves
    imageProcess = cv2.cvtColor(imageProcess, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Color mask', imageProcess)
    edges = cv2.Canny(image=imageProcess, threshold1=100, threshold2=200)  # Canny Edge Detection
    cv2.imshow('Edges', edges)
    originalFrame = blobDetection2(edges, originalFrame)
    cv2.imshow(window_name, originalFrame)
    cv2.waitKey(0)


testCode('colorDetection')
