import numpy as np
import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
from connectedComponentsMethod import ConnectedComponentMethod

def runLowerBarUI(squatTotal: int, setTotal: int):
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
    lmain = tk.Label(imageFrame) # Make label
    lmain.grid(row=0, column=0)  # Insert video label

    # Set the tracking method
    trackingMethod = ConnectedComponentMethod(window_name=window.title())  # LAB method

    # Make HUD window
    HUDWindow = tk.Frame(window, width=600, height=100)
    HUDWindow.grid(row=600, column=0, padx=10, pady=2)

    showSquatCountVisual(HUDWindow, 0, squatTotal, 0, setTotal)

    # Update video frame
    def show_video():
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)

        # Tracking
        trackingMethod.runLABMasking(frame)  # Run tracking method
        #squatCount = trackingMethod.blobTracking.calcSquat.setCount  # Get sets amount counted

        if trackingMethod.blobTracking.calcSquat.addSquat:
            # Visualize squats
            squatCount = trackingMethod.blobTracking.calcSquat.squatCount # Get squats amount counted
            showSquatCountVisual(HUDWindow, squatCount, squatTotal, 0, setTotal)
            trackingMethod.blobTracking.calcSquat.addSquat = False

        # Show image
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)

        # Update frame
        lmain.after(10, show_video)

    show_video()  # Show video

    window.mainloop()  # Start GUI


# Show the counter for amount of squats made
def showSquatCountVisual(window, squatCount: int, squatTotal: int, setCount:int, setTotal: int):

    # Iterate total squats
    for i in range(squatTotal):
        # Turn all squats made ON
        if i < squatCount:
            counterImage = Image.open('TestImages/counterOn.png')
        else:
            counterImage = Image.open('TestImages/counterOff.png')

        counterImage = ImageTk.PhotoImage(counterImage)  # Get image from folder

        # Make label for counter image
        counterLabel = tk.Label(window, image=counterImage)  # Make label
        counterLabel.image = counterImage  # Change image
        counterLabel.grid(row=0, column=i)  # Insert into window

    # Write squats made and total onto window
    writeSquats = tk.Label(window, text=f'Squats: {squatCount}/{squatTotal}')  # Make label
    writeSquats.grid(row=1, column=0)  # Insert into window

    # Write sets made and total onto window
    writeSquats = tk.Label(window, text=f'Sets: {setCount}/{setTotal}')  # Make label
    writeSquats.grid(row=1, column=1)  # Insert into window


if __name__ == '__main__':
    # Capture and update video frames
    runLowerBarUI(4, 10)
