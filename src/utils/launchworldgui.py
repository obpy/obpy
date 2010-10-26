#!/usr/bin/env python

import Tkinter, tkFileDialog
import os

def set_text():
    
    fe_text.set(tkFileDialog.askopenfilename(initialdir = os.getenv('HOME')))
    
def load_world():
    
    import obengine

root = Tkinter.Tk()

label = Tkinter.Label(root, text = 'World file')
label.pack(side = Tkinter.LEFT)

fe_text = Tkinter.StringVar(root)
file_entry = Tkinter.Entry(root, textvariable = fe_text)
file_entry.pack(side = Tkinter.LEFT)

browse_button = Tkinter.Button(root, command = set_text, text = 'Browse...')
browse_button.pack(side = Tkinter.LEFT)

load_button = Tkinter.Button(root, command = load_world, text = 'Load world')
load_button.pack(side = Tkinter.BOTTOM)

root.mainloop()