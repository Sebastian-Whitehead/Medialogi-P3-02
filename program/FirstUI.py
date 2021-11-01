import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk


root = tk.Tk()
window1 = tk.Canvas(root, width=600, height=500, relief='raised')


imageFrame = tk.Frame(root, width=600, height=500)
imageFrame.grid(row=2, column=0, padx=10, pady=2)
#Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)
cap = cv2.VideoCapture(0)
def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)


#Slider window (slider controls stage position)
#sliderFrame = tk.Frame(root, width=600, height=100)
#sliderFrame.grid(row = 600, column=0, padx=10, pady=2)

#w = tk.Label(sliderFrame, text='awd')
#w.grid(row=0, column=0)
nr_of_squats = tk.Entry(root)
nr_of_sets = tk.Entry(root)

def labels():
    squats_label = tk.Label(root, text='Input nr of squats you wish to do:')
    squats_label.config(font=('helvetica', 14))
    squats_label.grid(row=3, column=0)


    nr_of_squats.grid(row=4, column=0)

    sets_label = tk.Label(root, text='Input nr of sets you wish to do:')
    sets_label.config(font=('helvetica', 14))
    sets_label.grid(row=5, column=0)


    nr_of_sets.grid(row=6, column=0)



def squats():
    nr = nr_of_squats.get()
    nrset= nr_of_sets.get()
    info = tk.Label(root, text=('You wish to do ' + nr +' squats each set?'))
    info1 = tk.Label(root, text=('You wish to do ' + nrset + ' sets?'))
    info.grid(row=8, column=0)
    info1.grid(row=9, column=0)
    nr = nr_of_squats.get()
    nrset = nr_of_sets.get()
    if int(nr) > 0 and int(nrset) > 0:
        begin = tk.Button(text='Begin training', command=run_tonkos, bg='green', fg='white', width=10)
        begin.grid(row=10, column=0)


def run_tonkos():
    print("tonkos program")

if __name__ == '__main__':
    labels()
    accept = tk.Button(text='OK!', command=squats, bg='blue', fg='white', width=10)
    accept.grid(row=7, column=0)


    show_frame()  #Display 2
    root.mainloop()  #Starts GUI