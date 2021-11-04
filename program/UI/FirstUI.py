import cv2
import tkinter as tk
from PIL import Image, ImageTk
import TonkoUI


class test:

    def __init__(self):
        self.root = tk.Tk()
        self.nr_of_squats = tk.Entry(self.root)
        self.nr_of_sets = tk.Entry(self.root)

    def make_frame(self):
        window1 = tk.Canvas(self.root, width=600, height=500, relief='raised')

        imageFrame = tk.Frame(self.root, width=600, height=500)
        imageFrame.grid(row=2, column=0, padx=10, pady=2)
        # Capture video frames
        self.lmain = tk.Label(imageFrame)
        self.lmain.grid(row=0, column=0)

        self.cap = cv2.VideoCapture(0)

        self.labels()
        accept = tk.Button(text='OK!', command=self.squats, bg='blue', fg='white', width=10)
        accept.grid(row=7, column=0)

        self.show_frame()  #Display 2
        self.root.mainloop()  #Starts GUI

    def show_frame(self):
        _, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)

        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        self.lmain.after(10, self.show_frame)




    #Slider window (slider controls stage position)
    #sliderFrame = tk.Frame(root, width=600, height=100)
    #sliderFrame.grid(row = 600, column=0, padx=10, pady=2)

    #w = tk.Label(sliderFrame, text='awd')
    #w.grid(row=0, column=0)

    def labels(self):
        squats_label = tk.Label(self.root, text='Input nr of squats you wish to do:')
        squats_label.config(font=('helvetica', 14))
        squats_label.grid(row=3, column=0)


        self.nr_of_squats.grid(row=4, column=0)

        sets_label = tk.Label(self.root, text='Input nr of sets you wish to do:')
        sets_label.config(font=('helvetica', 14))
        sets_label.grid(row=5, column=0)


        self.nr_of_sets.grid(row=6, column=0)



    def squats(self):
        nr = self.nr_of_squats.get()
        nrset= self.nr_of_sets.get()
        info = tk.Label(self.root, text=('You wish to do ' + nr +' squats each set?'))
        info1 = tk.Label(self.root, text=('You wish to do ' + nrset + ' sets?'))
        info.grid(row=8, column=0)
        info1.grid(row=9, column=0)
        nr = self.nr_of_squats.get()
        nrset = self.nr_of_sets.get()
        if int(nr) > 0 and int(nrset) > 0:
            begin = tk.Button(text='Begin training', command=self.run_tonkos, bg='green', fg='white', width=10)
            begin.grid(row=10, column=0)


    def run_tonkos(self):
        nr = int(self.nr_of_squats.get())
        nrset = int(self.nr_of_sets.get())
        self.root.destroy()
        print(nr, nrset)
        TonkoUI.runLowerBarUI(nr, nrset)

if __name__ == '__main__':
    test().make_frame()