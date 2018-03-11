from queue import Queue
from tkinter import *
import pickle
import argparse

import os
from PIL import Image, ImageTk


def get_click(file_path, queue):
    root = Tk()

    # setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E + W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N + S)
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N + S + E + W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH, expand=1)

    # adding the image
    img = ImageTk.PhotoImage(Image.open(file_path))
    canvas.create_image(0, 0, image=img, anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

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
    files = {}
    if os.path.isfile('centres.pkl'):
        with open('centres.pkl', 'rb') as f:
            files = pickle.load(f)

    print('Files', files)
    keys = {x for x in files.keys()}
    print("loaded")
    queue = Queue()
    for file_name in set(file_names) - keys:
            get_click(file_name, queue)
            files[file_name] = queue.get()

    with open('centres.pkl', 'wb') as f:
        pickle.dump(files, f, pickle.HIGHEST_PROTOCOL)
    print("saved")
