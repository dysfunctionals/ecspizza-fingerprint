from queue import Queue
from tkinter import *
import argparse

from PIL import Image, ImageTk

from file_handling import load_pkl, write_pkl

CENTRES_FILE = 'centres.pkl'


def get_click(file_path, queue):
    root = Tk()

    # setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    canvas = Canvas(frame, bd=0)
    canvas.grid(row=0, column=0, sticky=N + S + E + W)
    frame.pack(fill=BOTH, expand=1)

    # adding the image
    img = ImageTk.PhotoImage(Image.open(file_path))
    canvas.create_image(0, 0, image=img, anchor="nw")
    # canvas.config(scrollregion=canvas.bbox(ALL))

    # function to be called when mouse is clicked
    def printcoords(event):
        # outputting x and y coords to console
        pos = (event.x, event.y)
        print(pos)
        queue.put(pos)
        root.destroy()

    # mouseclick event
    canvas.bind("<Button 1>", printcoords)

    root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()
    file_names = args.files
    files = load_pkl(CENTRES_FILE)

    print('Files', files)
    keys = {x for x in files.keys()}
    print("loaded")
    queue = Queue()
    for file_name in set(file_names) - keys:
            get_click(file_name, queue)
            files[file_name] = queue.get()

    write_pkl(CENTRES_FILE, files)
    print("saved")
