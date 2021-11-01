import numpy as np
import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
from connectedComponentsMethod import ConnectedComponentMethod

cap = None


def runLowerBarUI(squatTotal: int, nrset: int):
    # Get video data
    cap = cv2.VideoCapture(0)

    # Check if the camera is open on the users computer
    if not cap.isOpened():
        print("Cannot open camera")
        exit()  # Exit program on error
    else:
        # Get vcap property
        frameWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float width
        frameHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float height
        frameFps = cap.get(cv2.CAP_PROP_FPS)  # float fps

        # Print camera information
        print('Camera connected:')
        print('Dim:', frameWidth, 'x', frameHeight, 'fps:', int(frameFps))

    # Set up GUI
    window = tk.Tk()  # Makes main window
    window.wm_title('Training Assistant Computer - LAB')  # Set window title
    window.config(background="#FFFFFF")  # Set background color

    # Make video frame
    imageFrame = tk.Frame(window, width=600, height=500)  # Dimensions for video window
    imageFrame.grid(row=0, column=0, padx=10, pady=2)  # Grid for video window

    # Make video label
    lmain = tk.Label(imageFrame)
    lmain.grid(row=0, column=0)  # Insert video label

    trackingMethod = ConnectedComponentMethod(window_name=window.title())  # LAB method

    # Make HUD window
    HUDWindow = tk.Frame(window, width=600, height=100)
    HUDWindow.grid(row=600, column=0, padx=10, pady=2)

    # Update video frame
    def show_video():
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)

        # Tracking
        trackingMethod.runLABMasking(frame)  # Run tracking method
        squatCount = trackingMethod.blobTracking.calcSquat.squatCount

        # Show image
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)

        # Visualize squats
        showSquatCountVisual(HUDWindow, squatCount, squatTotal)

        # Update frame
        lmain.after(10, show_video)

    show_video()
    window.mainloop()  # Starts GUI


def showSquatCountVisual(window, squatCount: int, squatTotal: int):
    for i in range(squatTotal):
        if i < squatCount:
            counterImage = Image.open('TestImages/counterOn.png')
        else:
            counterImage = Image.open('TestImages/counterOff.png')

        counterImage = ImageTk.PhotoImage(counterImage)

        counterLabel = tk.Label(window, image=counterImage)
        counterLabel.image = counterImage

        counterLabel.grid(row=0, column=i)

    w = tk.Label(window, text=f'{squatCount}/{squatTotal}')
    w.grid(row=1, column=0)


if __name__ == '__main__':
    # Capture and update video frames
    cap = cv2.VideoCapture(0)
    runLowerBarUI(cap, 4, 10)
