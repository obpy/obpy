#!/usr/bin/env python

import obengine
import obengine.gfx.worldsource as worldsource
from obengine.gfx.player import PlayerView

import Tkinter, tkFileDialog
import os

import zipfile
import tempfile

import atexit

def set_text():
    
    fe_text.set(tkFileDialog.askopenfilename())
    
def load_world():
    
    root.quit()
    root.destroy()
    
    def run_world(win):
        
        world_file = zipfile.ZipFile(fe_text.get())
        tmpdir = tempfile.mkdtemp()
        
        world_file.extractall(tmpdir)
        
        os.chdir(tmpdir)
        
        source = worldsource.FileWorldSource('world.xml')
        source.parse()
        
        world = obengine.World(os.path.basename(fe_text.get()).strip('.zip'), 1)
        world.load_world(source)

        p = PlayerView('Test')
        p.join_world(world, [-10, -10, -5])
        
        def clean_up():
            
            for file in world_file.namelist():
                
                os.remove(file)
                
            os.chdir(os.pardir)
            os.rmdir(tmpdir)
        
        atexit.register(clean_up)
        
    obengine.gfx.init(run_world)
        
    

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