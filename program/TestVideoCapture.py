import cv2
import numpy as np
from SelfmadeBlobDetection import *
from BlobTracking import BlobTracking


def nothing(value):
    pass


class TrackObject:
    def __init__(self):
        self.window_name = 'Image'
        self.blobTracking = BlobTracking(
            window_name=self.window_name,
            collisionType='dim',
            addBlobClick=1
        )
        self.clickable = True

    def main(self):
        # Video to test
        cap = cv2.VideoCapture('TestImages/greensmall.mp4')

        # Frame counter
        frameCount = 0

        while True:
            # Capture frame-by-frame
            _, frame = cap.read()

            # Skip frames
            frameCount += 1
            # if frameCount % 5 == 0:

            cv2.setMouseCallback(self.window_name, self.click_event, param=[frame])

            if len(self.blobTracking.labelBlobs) > 0:
                self.com(frame, (0, 0))

            cv2.imshow('Image', frame)

            # Wait ms to simulate framerate
            if cv2.waitKey(15) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap.release()

        cv2.destroyAllWindows()

    def click_event(self, event, x, y, flags, params):
        if self.clickable:
            if flags == 1:  # (Left click)
                self.com(params[0], (x, y))
                self.blobTracking.addLabelToBlobs((x, y))
            self.clickable = False
            if flags == 0:
                self.clickable = True

    def com(self, originalImage, pos):
        image = originalImage.copy()

        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.threshold(image, 110, 255, cv2.THRESH_BINARY)[1]

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

            if w > 50 and h > 50 and w < 100 and h < 100:
                blobs.append((x, y, w, h))

        for blob in blobs:
            startPos = (blob[0], blob[1])
            endPos = (blob[0] + blob[2], blob[1] + blob[3])
            labeled_img = cv2.rectangle(labeled_img, startPos, endPos, (0, 0, 255), 1)

        self.blobTracking.run(blobs, originalImage)

        for blob in self.blobTracking.labelBlobs:
            blob = self.blobTracking.labelBlobs[blob]
            x1, x2 = blob[0], blob[0] + blob[2]
            y1, y2 = blob[1], blob[1] + blob[3]

            # cv2.imshow('com' + str(blob[0]), labeled_img[y1:y2, x1:x2])

        cv2.imshow('com', labeled_img)
        cv2.imshow('Image', originalImage)

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


if __name__ == '__main__':
    TrackObject().main()
