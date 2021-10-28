import numpy as np
import cv2
import tkinter as tk
from PIL import Image
from PIL import ImageTk

def runLowerBarUI(media, squatCount: int, squatTotal: int, repCount: int, repTotal: int):
    showSquatCountVisual(media, squatCount, squatTotal)
    showCountText(media, squatCount, squatTotal)
    showCountText(media, repCount, repTotal)

def showSquatCountVisual(media, squatCount: int, squatTotal: int):
    pass

def showCountText(media, count: int, total: int):
    pass

if __name__ == '__main__':
    # Set up GUI
    window = tk.Tk()  # Makes main window
    window.wm_title("Digital Microscope")
    window.config(background="#FFFFFF")

    # Graphics window
    imageFrame = tk.Frame(window, width=600, height=500)
    imageFrame.grid(row=0, column=0, padx=10, pady=2)

    # Capture video frames
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

        # Slider window (slider controls stage position)


    sliderFrame = tk.Frame(window, width=600, height=100)
    sliderFrame.grid(row=600, column=0, padx=10, pady=2)

    show_frame()  # Display 2
    window.mainloop()  # Starts GUI
    """
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
    root.mainloop()

    root = Tk()
    canvas = Canvas(root, width=300, height=300)
    canvas.pack()
    img = PhotoImage(file="ball.ppm")
    canvas.create_image(20, 20, anchor=NW, image=img)
    mainloop()
    """