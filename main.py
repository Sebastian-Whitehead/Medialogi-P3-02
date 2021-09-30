import cv2
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
from acquisitionKinect import AcquisitionKinect
from frame import Frame

if __name__ == '__main__':

    kinect = AcquisitionKinect()
    frame = Frame()

    while True:
        kinect.get_frame(frame)
        kinect.get_color_frame()
        image = kinect._frameRGB
        #OpenCv uses RGB image, kinect returns type RGBA, remove extra dim.
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

        if not image is None:
            cv2.imshow("Output-Keypoints",image)

        cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
           break
