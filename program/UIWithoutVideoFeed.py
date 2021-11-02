import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import TonkoUI

root = tk.Tk()

target_squats = tk.Entry(root)
target_sets = tk.Entry(root)


def make_frame():
    root.minsize(300, 200)

    labels() # Make GUI with labels and inputs

    root.mainloop()  # Starts GUI


def labels():
    squats_label = tk.Label(root, text='Input nr of squats you wish to do:')
    squats_label.config(font=('helvetica', 14))
    squats_label.grid(row=3, column=0)

    target_squats.grid(row=4, column=0)

    sets_label = tk.Label(root, text='Input nr of sets you wish to do:')
    sets_label.config(font=('helvetica', 14))
    sets_label.grid(row=5, column=0)

    target_sets.grid(row=6, column=0)

    accept = tk.Button(text='OK!', command=lambda: squats(target_squats, target_sets), bg='blue', fg='white', width=10)
    accept.grid(row=7, column=0)

def squats(nr_of_squats, nr_of_sets):
    nr = nr_of_squats.get()
    nrset = nr_of_sets.get()
    info = tk.Label(root, text=('You wish to do ' + nr + ' squats each set?'))
    info1 = tk.Label(root, text=('You wish to do ' + nrset + ' sets?'))
    info.grid(row=8, column=0)
    info1.grid(row=9, column=0)
    intNr, intNrset = int(nr), int(nrset)
    if intNr > 0 and intNrset > 0:
        begin = tk.Button(text='Begin training', command=lambda: run_tonkos(intNr, intNrset), bg='green', fg='white', width=10)
        begin.grid(row=10, column=0)


def run_tonkos(nr, nrset):
    print(f'{nr=}, {nrset=}') # Print total squat and set value

    root.destroy()  # Destroy input window

    TonkoUI.runLowerBarUI(nr, nrset)  # Open full program


if __name__ == '__main__':
    make_frame()
