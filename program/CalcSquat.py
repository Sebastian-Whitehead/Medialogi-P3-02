import json
import cv2

class CalcSquat:
    def __init__(self):
        self.blobData = dict()

        self.count = 0
        self.flag = 0
        self.offset = 40

    def runCalc(self, blobs):

        for n, blob in enumerate(blobs):
            label = blob
            blob = blobs[blob]
            if label in self.blobData:
                thisBlobData = self.blobData[label]
                thisBlobData['min'] = min(thisBlobData['min'], blob[1])
                thisBlobData['max'] = max(thisBlobData['max'], blob[1])
                self.blobData[label] = thisBlobData
            else:
                self.blobData[label] = dict()
                self.blobData[label]['min'] = blob[1]
                self.blobData[label]['max'] = blob[1]
                thisBlobData = self.blobData[label]

            # Checks if we are under the line, accepted as a squat.
            if thisBlobData['min'] < thisBlobData['max'] - self.offset:
                if blob[1] > thisBlobData['max'] - self.offset and self.flag == 1:
                    self.flag = -1
                elif blob[1] < thisBlobData['min'] + self.offset:
                    if self.flag == -1:
                        self.count += 1
                        print('Squats:', self.count)
                        self.flag = 0
                    if self.flag == 0:
                        self.flag = 1


    def drawDat(self, media):


        for n, blob in enumerate(self.blobData):
            label = blob
            blobData = self.blobData[blob]

            drawLine(label + ': min', 0, blobData['min'], (0, 0, 255), media)
            drawLine(label + ': min', 0, blobData['min'] + self.offset, (0, 255, 0), media)
            drawLine(label + ': max', 0, blobData['max'], (0, 0, 255), media)
            drawLine(label + ': max', 0, blobData['max'] - self.offset, (0, 255, 0), media)


        return media

def drawLine(text, x, y, color, media):
    h, w, _ = media.shape

    cv2.line(media, (0, y), (w, y), color)

    pos = (10, y - 10)
    face, scale, thickness = cv2.FONT_HERSHEY_DUPLEX, 0.5, 1
    cv2.putText(media, text, pos, face, scale, color, thickness, cv2.LINE_AA)

if __name__ == '__main__':

    media = 'TestImages/greensmall.mp4',
    dataPath = 'manifacturedDataGreensmall.txt',

    blobs = []

    with open(dataPath) as json_file:
        if json_file:
            blobs = json.load(json_file)

            print('Loaded: ', blobs)
            print('')

    CalcSquat(blobs, media)