import tkinter as tk
from PIL import Image, ImageTk
from connectedComponentsMethod import ConnectedComponentMethod
from MotionDetection import motion_detection
import EndScreen, cv2, keyboardInput


# Connect to the camera selected
def connectToCamera():
    # 0 = Internal, 1 = External computer camera
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
    return cap  # Return the cap from the video capture


# Make the main window
def makeMainWindow():
    window = tk.Tk()  # Makes main window
    window.wm_title('Training Assistant Computer - LAB')  # Set window title
    window.config(background="#FFFFFF")  # Set background color
    return window  # Return the tktiner window


# Make window/frame for video feed
def makeVideoWindow(window):
    # Make video frame
    imageFrame = tk.Frame(window, width=600, height=500)  # Dimensions for video window
    imageFrame.grid(row=0, column=0, padx=10, pady=2)  # Grid for video window

    # Make video label
    lmain = tk.Label(imageFrame)  # Make label
    lmain.grid(row=0, column=0)  # Insert video label

    return lmain  # Return the tkinter label


# Show the counter for amount of squats made
def showSquatCountVisual(
        imageCounterWindow,
        textCounterWindow,
        squatCount: int,
        squatTotal: int,
        setCount: int,
        setTotal: int):
    print(squatCount, ":", squatTotal)  # Print out counted squats and target squat

    # Turn counter diamonds on or off
    for i in range(squatTotal):
        counterImagePath = 'TestImages/counterOff.png' # Get "counter off" image path
        if i < squatCount: counterImagePath = 'TestImages/counterOn.png' # Get "counter on" image path
        counterImage = Image.open(counterImagePath) # Open picked counter image
        counterImage_resized_image = counterImage.resize((30, 45), Image.ANTIALIAS)  # Resize counter image
        counterImage = ImageTk.PhotoImage(counterImage_resized_image)  # Get image from folder

        # Make label for counter image
        counterLabel = tk.Label(imageCounterWindow, image=counterImage)  # Make label
        counterLabel.image = counterImage  # Change image
        counterLabel.grid(row=0, column=i)  # Insert into window

    # Write squats made and total onto window
    writeSquats = tk.Label(textCounterWindow, text=f'Squats: {squatCount}/{squatTotal}')  # Make label
    writeSquats.grid(row=0, column=0)  # Insert into window

    # Write sets made and total onto window
    writeSquats = tk.Label(textCounterWindow, text=f'Sets: {setCount}/{setTotal}')  # Make label
    writeSquats.grid(row=0, column=1)  # Insert into window

# Run window UI
def runLowerBarUI(squatTotal: int, setTotal: int, program):
    window = makeMainWindow() # Make main window
    lmain = makeVideoWindow(window) # Make video feedback window
    cap = connectToCamera() # Connect to camera

    # Make HUD window
    HUDWindow = tk.Frame(window, width=600, height=100) # Make window for underbar UI
    HUDWindow.grid(row=50, column=0, padx=5, pady=5) # Place underbar UI window

    # Make image counter window
    imageCounterWindow = tk.Frame(HUDWindow, width=600, height=100) # Make window on HUDWindow
    imageCounterWindow.grid(row=50, column=0, padx=5, pady=5) # Place image counter window top

    # Make text counter window
    textCounterWindow = tk.Frame(HUDWindow, width=600, height=100) # Make window on HUDWindow
    textCounterWindow.grid(row=51, column=0, padx=5, pady=5) # Place text counter window bottom

    # Show the HUD window
    showSquatCountVisual(imageCounterWindow, textCounterWindow, 0, squatTotal, 0, setTotal)

    # Set the tracking method
    if program == 'motionProgram':
        trackingMethod = motion_detection(squatTotal=squatTotal, setTotal=setTotal, cap=cap)
    elif program == 'greenHatProgram':
        trackingMethod = ConnectedComponentMethod(squatTotal=squatTotal, setTotal=setTotal)

    # Update video frame (Continuously loop)
    def show_video():
        _, frame = cap.read() # Get the frame from the video capture
        frame = cv2.flip(frame, 1) # Flip the window to mirror
        frame = trackingMethod.run(frame)  # Run tracking method

        keyboardInput.FinishSet(program, trackingMethod) # Check for "r"-pressed

        # Update UI
        if program == 'motionProgram':
            # Update when a squat has been added
            if trackingMethod.addSquat:
                trackingMethod.addSquat = False  # Return the "add squat" to False
                squatCount = trackingMethod.squatCount  # Get squats amount counted
                setCount = trackingMethod.setCount  # Get sets amount counted
                # Update UI frame and visualize squats
                showSquatCountVisual(
                    imageCounterWindow,
                    textCounterWindow,
                    squatCount,
                    squatTotal,
                    setCount,
                    setTotal
                )

            # When the workout is complete
            if trackingMethod.workoutComplete == True:
                window.destroy() # Destroy main window
                EndScreen.Screen() # Start end-screen window

        if program == 'greenHatProgram':
            # Update when a squat has been added
            if trackingMethod.blobTracking.calcSquat.addSquat:
                trackingMethod.blobTracking.calcSquat.addSquat = False  # Return the "add squat" to False
                squatCount = trackingMethod.blobTracking.calcSquat.squatCount  # Get squats amount counted
                setCount = trackingMethod.blobTracking.calcSquat.setCount  # Get sets amount counted
                # Update UI frame and visualize squats
                showSquatCountVisual(
                    imageCounterWindow,
                    textCounterWindow,
                    squatCount,
                    squatTotal,
                    setCount,
                    setTotal
                )

            # When the workout is complete
            if trackingMethod.blobTracking.calcSquat.workoutComplete == True:
                window.destroy() # Destroy main window
                EndScreen.Screen() # Start end-screen window

        # Show video feedback frame
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) # Convert BGR to RGBA
        img = Image.fromarray(cv2image) # Convert image to Image
        imgtk = ImageTk.PhotoImage(image=img) # Convert to ImageTk
        lmain.imgtk = imgtk # Set video feedback
        lmain.configure(image=imgtk) # Configure

        lmain.after(10, show_video)  # Update frame every 10 mill.

    show_video()  # Show video
    window.mainloop()  # Start GUI


if __name__ == '__main__':
    # Capture and update video frames
    detectionProgramMethod = 'greenHatProgram'
    # detectionProgramMethod = 'motionProgram'
    runLowerBarUI(5, 2, detectionProgramMethod)
