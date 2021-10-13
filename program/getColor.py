import cv2
import numpy as np
from BlobTracking import BlobTracking

class PickColor:
    def __init__(self):
        self.window_name = 'Image'
        self.blobTracking = BlobTracking(
            window_name=self.window_name,
            collisionType='dim',
            addBlobClick=4
        )

        self.originalImage = cv2.imread('TestImages/handskerBillede.png')

        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.click_event, param=[self.originalImage])

    def getColor(self, x, y, image, n):
        image = cv2.circle(image, (x, y), radius=5, color=(0, 0, 255), thickness=-1)
        cv2.imshow('Image', image)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        if n == 1:
            self.color1 = hsv[x, y]
        if n == 2:
            self.color2 = hsv[x, y]

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        self.com(hsv, 102, 255, (x, y))
        print(self.color1, self.color2)

    def click_event(self, event, x, y, flags, params):
        if flags == 1:  # (Left click)
            self.getColor(x, y, params[0], 1)
        if flags == 2:  # (Right click)
            self.getColor(x, y, params[0], 2)

    def main(self):

        self.color1 = (0, 0, 0)
        self.color2 = (0, 0, 0)

        cv2.namedWindow(self.window_name)
        cv2.createTrackbar('Lower threshold', self.window_name, 0, 255, nothing)
        cv2.createTrackbar('Upper threshold', self.window_name, 10, 255, nothing)


        while True:
            lowerThresh = cv2.getTrackbarPos('Lower threshold', self.window_name)
            upperThresh = cv2.getTrackbarPos('Upper threshold', self.window_name)

            image = self.originalImage.copy()
            cv2.imshow('Image', self.originalImage)
            #hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            #self.com(hsv, lowerThresh, upperThresh)
            #edges(hsv, lowerThresh, upperThresh)
            #colorMaskManual(image, self.color1, self.color2, lowerThresh)

            #hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            #cv2.imshow('HSV', hsv)
            #gray = cv2.imread('TestImages/handskerBillede.png', cv2.IMREAD_GRAYSCALE)
            #gray = cv2.threshold(gray, lowerThresh, upperThresh, cv2.THRESH_BINARY)[1]
            #cv2.imshow('gray', gray)
            cv2.waitKey(1)

    def com(self, image, lower, upper, pos):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        image = cv2.threshold(image, lower, upper, cv2.THRESH_BINARY)[1]

        num_labels, labels = cv2.connectedComponents(image)

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

            if pointRectCollider('dim', pos, (x, y, w, h)):
                blobs.append((x, y, w, h))

        for blob in blobs:
            labeled_img = cv2.rectangle(labeled_img, (blob[0], blob[1]), (blob[0] + blob[2], blob[1] + blob[3]),
                                              (0, 0, 255), 1)

        self.blobTracking.run(blobs, labeled_img)

        for blob in blobs:
            cv2.imshow('com' + str(blob[0]), labeled_img[blob[1]:blob[1] + blob[3], blob[0]:blob[0] + blob[2]])

        cv2.imshow('com', labeled_img)

# Get collision of point and rectangle
# 'corners' will check with the corners of the rectangle ((x1,y2),(x2,y2))
# 'dim' will check with the width and height of the rectangle ((x,y),(w,h)))
def pointRectCollider(method, point, rect):
    if method == 'corners':
        if rect[0] < point[0] < rect[2] and rect[1] < point[1] < rect[3]:
            return True
    elif method == 'dim':
        if rect[0] < point[0] < rect[0] + rect[2] and rect[1] < point[1] < rect[1] + rect[3]:
            return True
    return False

def edges(image, lower, upper):

    # Filter only the edges of image
    image = cv2.Canny(image, lower, upper)
    cv2.imshow('edges', image)

def colorMaskManual(img: np.ndarray, color1, color2, lower) -> np.ndarray:

    offset = (lower, lower, lower)

    # Convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.subtract(color1, offset), np.add(color2, offset))

    # Slice the color
    imask = mask > 0
    maskedImg = np.zeros_like(img, np.uint8)
    maskedImg[imask] = img[imask]

    cv2.imshow('masked', maskedImg)

    return maskedImg

def nothing(value):
    pass


if __name__ == '__main__':
    pickColor().main()