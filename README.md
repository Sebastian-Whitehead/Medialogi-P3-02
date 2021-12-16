# Utilizing visual processing to count user squat repetitions, from a live video feed
3rd semester Medialogy, group 2 (P3)
Aalborg Universirty, Fall 2021

# About 
The program consist of two detection methods, which can count a person doing squats.
First method tracks movement in the frame, and the second methods tracks a light green hat.

This program has been developed as an university project at Aalborg University, trying to solve the problem statement:
"How can we make a training assistant program which counts a given exercise the user has performed, with minimal equipment requirements using computer vision?"

The project was made in the periode from September to December 2021.

- - -

# Start program
1. Run "main.py" using Python.
2. Pick which detection method to use.
3. Input the number of desired squats and sets this session should consist of.
4. Press the "Spacebar"-key to start the countdown and calibration of the program.
  - Motion detection program: Make sure there are no other movement in the room, other than the user.
  - Green hat program: Make sure the green hat is the highest found object doing the countdown.
6. First squat is a calibration squat, setting the top and lower line at the higehst and lowest point.
7. Reach under the lower line, and above the upper line, when doing each squat.
8. When the target squat and sets has been reached, the program will continue to the main screen (Step 2).

Additional features
- The "r"-key will force the program to skip the current set

- - -

# Requirements
- One light green hat
- One camera (Internal computer or external computer plugable)

The program has been developed in Python using following libraries:
- OpenCV (https://opencv.org)
- tkinter (https://docs.python.org/3/library/tkinter.html)
- NumPy (https://numpy.org)
- keyboard (https://pypi.org/project/keyboard/)

- - -

# Group members
- Charlotte Johansen
- Rebecca Ryø Hansen
- Sebastian Whitehead
- Tobias Niebuhr Kiholm
- Tonko Emil Westerhof Bossen

- Mark Philip Philipsen (Supervisor)
