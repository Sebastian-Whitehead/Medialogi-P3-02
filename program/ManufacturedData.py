import cv2, json
from BlobTracking import BlobTracking

class ManufacturedData:
    def __init__(self, media, dataPath, startFrame, endFrame, cropped, manualFlow):

        self.dataPath = dataPath
        self.startFrame = startFrame
        self.endFrame = endFrame
        self.cropped = cropped
        self.manualFlow = manualFlow
        if not cropped:
            self.startFrame = 0

        self.window_name = 'Media'
        self.cap = cv2.VideoCapture(media)

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.startFrame)
        _, self.media = self.cap.read()
        self.length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frame = self.startFrame

        self.blobs = [[] for _ in range(self.length)]
        with open(self.dataPath) as json_file:
            if json_file:
                self.blobs = json.load(json_file)
                self.startBlobs = {
                    'head': [156, 70, 213, 133],\
                    'r_hand': [133, 249, 178, 279],\
                    'l_hand': [183, 243, 235, 277],\
                    'waist': [140, 286, 247, 310],\
                    'r_foot': [125, 481, 155, 520],\
                    'l_foot': [215, 481, 243, 519]
                }
                #print(self.blobs[46])

                print('Loaded: ', self.blobs)
                print('')

        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.click_event)

        self.run()

    def click_event(self, event, x, y, flags, params):

        # Draw rectangle for a new blob
        if flags == 1: # (Left click)

            # Set start position of new blob
            if event == 1: # (Mouse down)
                self.newBlob = (x, y)
                print('Press', x, y)

            # Display the rectangle of new blob (Not working. Image isn't updating)
            elif event == 0: # (Mouse drag)
                cv2.rectangle(self.media, (self.newBlob[0], self.newBlob[1]), (x, y), (0, 0, 255), 2)

            # Save new blob to current frame of blobs
            elif event == 4: # (Mouse up)
                print('Release', self.newBlob[0], self.newBlob[1], x, y)
                self.blobs[self.frame].append((self.newBlob[0], self.newBlob[1], x, y))

                # Save all blobs in all frames to file
                with open(self.dataPath, 'w') as outfile:
                    json.dump(self.blobs, outfile)

        # Remove all blobs in current frame
        if flags == 2: # (Right click)
            self.blobs[self.frame] = []

            # Save all blobs in all frames to file
            with open(self.dataPath, 'w') as outfile:
                json.dump(self.blobs, outfile)

    # Run video
    def run(self):

        # Go through all frames. Next frame on button click
        while (self.frame <= self.endFrame and self.cropped) or (self.frame <= self.length - 1 and not self.cropped):
            print('Frame:', self.frame)

            # Find the the buddy for the labels in this frame
            if self.frame - 1 > 0:
                self.startBlobs = BlobTracking(self.startBlobs, self.blobs[self.frame])

            # Get the labels from start blobs given
            labels = list(self.startBlobs.keys())
            # Get the similar values for the labels
            values = list(self.startBlobs.values())
            # Draw rectangles for all blobs in this frame
            for blob in self.blobs[self.frame]:
                # Make attributes for drawing the rectangle
                # Start coordination of the rectangle
                startPos = (blob[0], blob[1])
                # End coordination of the rectangle
                endPos = (blob[2], blob[3])
                cv2.rectangle(self.media, startPos, endPos, (0, 0, 255), 1)

                # Write label on blob
                # Get the index of the current label
                labelIndex = values.index(blob)
                # Get the label using the index
                feedbackText = labels[labelIndex]
                # Make new attributes for background of the text
                fontFace, fontScale, fontColor, thickness = cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1
                # Write the background of the text on frame
                cv2.putText(self.media, feedbackText, (blob[0], blob[1] - 5), fontFace, fontScale, fontColor, thickness,
                            cv2.LINE_AA)
                # Change attributes to front view of text


            # Show current frame
            cv2.imshow(self.window_name, self.media)

            # Next frame
            if self.manualFlow:
                cv2.waitKey(-1)
            else:
                cv2.waitKey(15)
            self.frame += 1
            _, self.media = self.cap.read()
            print('')

        # Reset video to startframe or 0
        self.frame = self.startFrame
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.startFrame)
        self.run()

        # Close video
        #self.cap.release()
        #cv2.destroyAllWindows()

if __name__ == '__main__':
    manufacturedData = ManufacturedData(
        media='TestImages/greensmall.mp4',
        dataPath='manifacturedDataGreensmall.txt',
        startFrame=47, endFrame=103,
        cropped=True, manualFlow=False
    )