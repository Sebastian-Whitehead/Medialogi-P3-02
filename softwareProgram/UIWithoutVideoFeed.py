import tkinter as tk
import TonkoUI


# Make the window frame for the input UI
def make_frame(program):
    root = tk.Tk()  # Main window for input UI

    root.minsize(300, 200)  # Set minimum size of window
    labels(root, program)  # Make GUI with labels and inputs
    root.mainloop()  # Starts GUI


# Make labels on window frame
def labels(root, program):
    # Input squat text
    squats_label = tk.Label(root, text='Input nr of squats you wish to do:')  # Nr of squats
    squats_label.config(font=('helvetica', 14))  # Font-family
    squats_label.grid(row=3, column=0)  # Place top

    # Make squat input
    target_squats = tk.Entry(root)  # Target squat input
    target_squats.grid(row=4, column=0)  # Place second top

    # Input sets text
    sets_label = tk.Label(root, text='Input nr of sets you wish to do:')  # Nr of sets
    sets_label.config(font=('helvetica', 14))  # Font-family
    sets_label.grid(row=5, column=0)  # Place third top

    # Make set input
    target_sets = tk.Entry(root)  # Target sets input
    target_sets.grid(row=6, column=0)  # Place fourth top

    # User button, accept input
    accept = tk.Button(text='OK!',  # Make button
                       command=lambda: squats(root, target_squats, target_sets, program),
                       bg='blue', fg='white', width=10)  # Blue button
    accept.grid(row=7, column=0)  # Place fifth top


# Get and confirm user input
def squats(root, nr_of_squats, nr_of_sets, program):
    nr = nr_of_squats.get()  # Get squat input
    nrset = nr_of_sets.get()  # Get set input

    # User squat input text
    info = tk.Label(root, text=('You wish to do ' + nr + ' squats each set?'))  # Squat target label
    info.grid(row=8, column=0)  # Place third bottom

    # User set input text
    info1 = tk.Label(root, text=('You wish to do ' + nrset + ' sets?'))  # Sets target label
    info1.grid(row=9, column=0)  # Place second bottom

    intNr, intNrset = int(nr), int(nrset)  # Convert squat and set input to integers

    # Test if the input if more than zero
    if intNr > 0 and intNrset > 0:
        # Start softwareProgram button
        begin = tk.Button(text='Begin training',  # Make button
                          command=lambda: run_tonkos(root, intNr, intNrset, program),
                          bg='green', fg='white', width=10)  # White button
        begin.grid(row=10, column=0)  # Place first bottom


# Run softwareProgram with given inputs
def run_tonkos(root, nr, nrset, program):
    if nr > 30: return  # Stop the program from doing more than 30 squats pr set
    print(f'{nr=}, {nrset=}')  # Print total squat and set value
    root.destroy()  # Destroy input window
    TonkoUI.runLowerBarUI(nr, nrset, program)  # Open main squat tracking program


if __name__ == '__main__':
    make_frame()
