import string, random, cv2
import imageProcessing as IP
import math


class Blob:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 0
        self.h = 0
        Blob.threshold = 25

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def setDimension(self, w, h):
        self.w = w
        self.h = h

    def getPosition(self):
        return (self.x, self.y)

    def getDimension(self):
        return (self.w, self.h)

    def setThreshold(self, threshold):
        Blob.threshold = threshold

    def print(self):
        print(self.x, self.y, self.w, self.h)


class Pixel:
    def __init__(self, value, x, y):
        self.handled = False
        self.value = value
        self.x = x
        self.y = y

    def setParentArea(self, parentArea):
        self.parentArea = parentArea

    def getParentArea(self):
        return self.parentArea


offset = [-1, 1]


def grassFire(frame, pixel, x, y, blob, row):
    for i in offset:
        for j in offset:
            if x is not x + i or y is not y + j:
                x = x + i
                y = y = j
                if 0 <= x and x < len(frame) and 0 <= y and y < len(row):
                    if 0 < pixel:
                        pixel = frame[x][y]
                        grassFire(frame, pixel, x, y, blob, row)
    else:
        if blob.getPosition()[0] < x:
            blob.x = x
        else:
            blob.w = x

        if blob.getPosition()[1] < y:
            blob.y = y
        else:
            blob.h = y

        blobs.append(blob)


def blobDetection(frame, originalFrame):
    for x, row in enumerate(frame):
        for y, pixel in enumerate(row):
            if 0 < pixel:
                blob = Blob(x, y)
                grassFire(frame, pixel, x, y, blob, row)

    for blob in blobs:
        print(blob)
        # originalFrame = cv2.rectangle(originalFrame, (blob.x, blob.y), (blob.x + blob.w, blob.y + blob.h), (0, 0, 255), 1)

    return originalFrame

def mergeBlobs(blobs):
    blobs = list(set(blobs))
    for blob1 in list(blobs):
        for blob2 in list(blobs):
            if blob1 is not blob2:
                if blob1.x - Blob.threshold < blob2.x + blob2.w and blob1.x + blob1.w + Blob.threshold > blob2.x and blob1.y - Blob.threshold < blob2.y + blob2.h and blob1.h + blob1.y + Blob.threshold > blob2.y:
                    blob2.x = min(blob1.x, blob2.x)
                    blob2.w = max(blob1.w, blob2.w)
                    blob2.y = min(blob1.y, blob2.y)
                    blob2.h = max(blob1.h, blob2.h)
                    blobs.remove(blob1)
    return blobs

def show(blobs, originalFrame, frame):
    for blob in blobs:

        detectedImage = cv2.rectangle(originalFrame.copy(), (blob.x, blob.y), (blob.x + blob.w, blob.y + blob.h), (0, 0, 255), 1)

        textPosition, fontFace, fontScale, fontColor, thickness = (blob.x, blob.y), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1
        detectedImage = cv2.putText(detectedImage, str(blob.x) + ':' + str(blob.y), textPosition, fontFace, fontScale, fontColor, thickness, cv2.LINE_AA)

        textPosition, fontFace, fontScale, fontColor, thickness = (blob.x + blob.w, blob.y + blob.h), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1
        detectedImage = cv2.putText(detectedImage, str(blob.w) + ':' + str(blob.h), textPosition, fontFace, fontScale, fontColor, thickness, cv2.LINE_AA)

        cv2.imshow('originalFrame', detectedImage)
        cv2.waitKey(5)

def blobDetection2(frame, originalFrame):
    blobs = []
    for y, row in enumerate(frame):

        #Blobs merge on overlap
        if 1 < len(blobs):
            blobs = mergeBlobs(blobs)
        #show(blobs, originalFrame, frame)

        #print('Row:', y, ':', len(frame))
        for x, pixel in enumerate(row):
            #print(x, y)
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
                        if dist < Blob.threshold:
                            #if x >= blob.x + blob.w:
                                #blob.w = x - blob.x
                            #elif x < blob.x:
                            #else:
                                #blob.w = blob.x - x
                                #blob.x = x

                            #if y >= blob.y + blob.h:
                                #blob.h = y - blob.y
                            #elif y < blob.y:
                            #else:
                                #blob.h = blob.y - y
                                #blob.y = y


                            blob.x = min(x, blob.x)
                            blob.w = max(x - blob.x, blob.w)
                            blob.y = min(y, blob.y)
                            blob.h = max(y - blob.y, blob.h)
                            blobFound = True
                            break
                if not blobFound:
                    blob = Blob(x, y)
                    blobs.append(blob)

    detectedImage = originalFrame.copy()
    for blob in blobs:
        blob.print()
        detectedImage = cv2.rectangle(detectedImage, (blob.x, blob.y), (blob.x + blob.w, blob.y + blob.h), (0, 0, 255), 1)

    return detectedImage

def testCode():
    originalFrame = cv2.imread('../handskerBillede.png')

    originalFrameBlured = cv2.GaussianBlur(originalFrame, (7, 7), 0)
    greenGloveMask = IP.threshold(originalFrameBlured, (0, 0, 0), (48, 30, 104), (78, 122, 255))  # Mask green gloves
    greenGloveMask = cv2.cvtColor(greenGloveMask, cv2.COLOR_BGR2GRAY)
    originalFrame = blobDetection2(greenGloveMask, originalFrame)
    cv2.imshow('originalFrame', originalFrame)
    cv2.waitKey(0)

testCode()