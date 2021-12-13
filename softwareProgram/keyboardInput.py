import keyboard, time

# Force the program to finish the current set when "r" is pressed
def FinishSet(program, trackingMethod):
    if keyboard.is_pressed('r'): # When "r" is pressed
        print("R Pressed")
        # Depends on program method
        if program == 'motionProgram':
            print(program)
            trackingMethod.squatCount = 0 # Reset squat counter
            trackingMethod.setCount += 1 # Add one set
            trackingMethod.addSquat = True # Tell UI to update

        elif program == 'greenHatProgram':
            print(program)
            trackingMethod.blobTracking.calcSquat.squatCount = 0 # Reset squat counter
            trackingMethod.blobTracking.calcSquat.setCount += 1 # Add one set
            trackingMethod.blobTracking.calcSquat.addSquat = True # Tell UI to update

        time.sleep(1) # Wait one second, to disable multiple clicks (Bad)

# Start countdown to re-calibrate blob data
def reCalcTracking(trackingMethod):
    if keyboard.is_pressed('space'):    # if key 'space' is pressed
        print(f'Start softwareProgram!')
        # Start counter, which will re-calibrate blob data
        trackingMethod.resetStartFrame = trackingMethod.frameCount + 30 * trackingMethod.resetTimer