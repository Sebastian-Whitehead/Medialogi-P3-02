import tkinter as tk
from tkinter import *
import cv2, UIWithoutVideoFeed
import sys


# Start "Motion Detection"-program
def motion(win):
    win.destroy()  # Destroy end screen window
    UIWithoutVideoFeed.make_frame('motionProgram')  # Start input UI


# Start "Green hat"-program
def Hat(win):
    win.destroy()  # Destroy end screen window
    UIWithoutVideoFeed.make_frame("greenHatProgram")  # Start input UI


# End screen function showing the UI
def Screen():
    window = Tk()  # Make a tkinter window
    window.title('test')  # Set the title of the window
    window.minsize(500, 500)  # Set the size of the window

    # Text-label saying "Good job" placed top/center
    Good_Label = tk.Label(window, text='Good job')  # Make label on "window"
    Good_Label.config(font=('helvetica', 36))  # Set the font-family and -size
    Good_Label.place(x=250, y=150, anchor="center")  # Place in top/center of window

    # Text-label info completion placed top/center
    # Good_Label2 = tk.Label(window, text='You completed your workout') # Make label on "window"
    # Good_Label2.config(font=('helvetica', 28)) # Set the font-family and -size
    # Good_Label2.place(x=250, y=300, anchor="center") # Place in top/center of winwow

    # Exit button quiting the program (placed buttom/right)
    exitbutton = Button(window, text='Exit', bg='red', width=6,  # Make red button
                        command=lambda: sys.exit('program terminated'))  # Quit program
    exitbutton.config(font=('helvetica', 28))  # Set font-family and -size
    exitbutton.place(x=350, y=350, anchor='center')  # Place buttom/right of window

    # Button to start "Motion Detection"-program (placed bottom/left upper)
    restartbutton = Button(window, text='Motion', bg='green',  # Make green button
                           command=lambda: motion(window))  # Start MD-program
    restartbutton.config(font=('helvetica', 28))  # Set font-family and -size
    restartbutton.place(x=150, y=325, anchor='center')  # Place bottom/left upper

    # Button to start "Green hat"-program (placed bottom/left lower)
    hatbutton = Button(window, text='Hat', bg='blue', width=6,  # Make blue button
                       command=lambda: Hat(window))  # Start GH-program
    hatbutton.config(font=('helvetica', 28))  # Set font-family and -size
    hatbutton.place(x=150, y=425, anchor='center')  # Place bottom/left lower

    window.mainloop()  # Loop UI
