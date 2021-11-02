import tkinter as tk
import TonkoUI


# Make the window frame for the input UI
def make_frame():
    root = tk.Tk()  # Main window for input UI

    root.minsize(300, 200)  # Set minimum size of window
    labels(root)  # Make GUI with labels and inputs
    root.mainloop()  # Starts GUI


def labels(root):
    # Input squat text
    squats_label = tk.Label(root, text='Input nr of squats you wish to do:')
    squats_label.config(font=('helvetica', 14))
    squats_label.grid(row=3, column=0)

    # Make squat input
    target_squats = tk.Entry(root)
    target_squats.grid(row=4, column=0)

    # Input sets text
    sets_label = tk.Label(root, text='Input nr of sets you wish to do:')
    sets_label.config(font=('helvetica', 14))
    sets_label.grid(row=5, column=0)

    # Make set input
    target_sets = tk.Entry(root)
    target_sets.grid(row=6, column=0)

    # User button, accept input
    accept = tk.Button(text='OK!',
                       command=lambda: squats(root, target_squats, target_sets),
                       bg='blue', fg='white', width=10)
    accept.grid(row=7, column=0)


# Get and confirm user input
def squats(root, nr_of_squats, nr_of_sets):
    nr = nr_of_squats.get()  # Get squat input
    nrset = nr_of_sets.get()  # Get set input

    # User squat input text
    info = tk.Label(root, text=('You wish to do ' + nr + ' squats each set?'))
    info.grid(row=8, column=0)

    # User set input text
    info1 = tk.Label(root, text=('You wish to do ' + nrset + ' sets?'))
    info1.grid(row=9, column=0)

    intNr, intNrset = int(nr), int(nrset)  # Convert squat and set input to integers

    # Test if the input if more than zero
    if intNr > 0 and intNrset > 0:
        # Start program button
        begin = tk.Button(text='Begin training',
                          command=lambda: run_tonkos(root, intNr, intNrset),
                          bg='green', fg='white', width=10)
        begin.grid(row=10, column=0)


# Run program with given inputs
def run_tonkos(root, nr, nrset):
    print(f'{nr=}, {nrset=}')  # Print total squat and set value
    root.destroy()  # Destroy input window
    TonkoUI.runLowerBarUI(nr, nrset)  # Open full program


if __name__ == '__main__':
    make_frame()
