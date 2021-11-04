import numpy as np
import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
import sys
sys.path.append('Process')
from connectedComponentsMethod import ConnectedComponentMethod


# Connect to the camera selected
def connectToCamera():
    # 0 = Internal computer camera
    # 1 = External connected camera
    cap = cv2.VideoCapture(0)  # Get video data

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

    return cap


# Make the main window
def makeMainWindow():
    # Set up GUI
    window = tk.Tk()  # Makes main window
    window.wm_title('Training Assistant Computer - LAB')  # Set window title
    window.config(background="#FFFFFF")  # Set background color
    return window


# Make window/frame for video feed
def makeVideoWindow(window):
    # Make video frame
    imageFrame = tk.Frame(window, width=600, height=500)  # Dimensions for video window
    imageFrame.grid(row=0, column=0, padx=10, pady=2)  # Grid for video window

    # Make video label
    lmain = tk.Label(imageFrame)  # Make label
    lmain.grid(row=0, column=0)  # Insert video label

    return lmain


# Show the counter for amount of squats made
def showSquatCountVisual(window, squatCount: int, squatTotal: int, setCount: int, setTotal: int):
    # Make image counter window
    imageCounterWindow = tk.Frame(window, width=600, height=100)
    imageCounterWindow.grid(row=50, column=0, padx=5, pady=5)

    # Iterate total squats
    for i in range(squatTotal):
        # Turn all squats made ON
        counterImagePath = 'TestImages/counterOff.png'
        if i < squatCount: 'TestImages/counterOn.png'
        if __name__ == '__main__': counterImagePath = '../' + counterImagePath
        counterImage = Image.open(counterImagePath)
        counterImage = ImageTk.PhotoImage(counterImage)  # Get image from folder

        # Make label for counter image
        counterLabel = tk.Label(imageCounterWindow, image=counterImage)  # Make label
        counterLabel.image = counterImage  # Change image
        counterLabel.grid(row=0, column=i)  # Insert into window

    # Make text counter window
    textCounterWindow = tk.Frame(window, width=600, height=100)
    textCounterWindow.grid(row=51, column=0, padx=5, pady=5)

    # Write squats made and total onto window
    writeSquats = tk.Label(textCounterWindow, text=f'Squats: {squatCount}/{squatTotal}')  # Make label
    writeSquats.grid(row=0, column=0)  # Insert into window

    # Write sets made and total onto window
    writeSquats = tk.Label(textCounterWindow, text=f'Sets: {setCount}/{setTotal}')  # Make label
    writeSquats.grid(row=0, column=1)  # Insert into window


def runLowerBarUI(squatTotal: int, setTotal: int):
    window = makeMainWindow()
    lmain = makeVideoWindow(window)
    cap = connectToCamera()

    # Make HUD window
    HUDWindow = tk.Frame(window, width=600, height=100)
    HUDWindow.grid(row=50, column=0, padx=5, pady=5)
    showSquatCountVisual(HUDWindow, 0, squatTotal, 0, setTotal)

    # Set the tracking method
    trackingMethod = ConnectedComponentMethod(
        window_name=window.title(),
        squatTotal=squatTotal, setTotal=setTotal)  # LAB method

    # Update video frame
    def show_video():
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)

        trackingMethod.runLABMasking(frame)  # Run tracking method

        # Update UI
        if trackingMethod.blobTracking.calcSquat.addSquat:
            # Visualize squats
            trackingMethod.blobTracking.calcSquat.addSquat = False  # Return the "add squat" to False

            squatCount = trackingMethod.blobTracking.calcSquat.squatCount  # Get squats amount counted
            setCount = trackingMethod.blobTracking.calcSquat.setCount  # Get sets amount counted
            showSquatCountVisual(HUDWindow, squatCount, squatTotal, setCount, setTotal)  # Update UI frame

        # Show image
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)

        lmain.after(10, show_video)  # Update frame

    show_video()  # Show video
    window.mainloop()  # Start GUI


if __name__ == '__main__':
    # Capture and update video frames
    runLowerBarUI(3, 2)
