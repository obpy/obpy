#!/usr/bin/env python

import obengine
import obengine.gfx.worldsource as worldsource
from obengine.gfx.player import PlayerView, KeyboardPlayerController
from obengine.gfx import get_rootwin

import Tkinter, tkFileDialog, tkMessageBox
import ttk
import os

import zipfile
import tempfile

import atexit

def set_text():
    """
    Callback for setting the text of the world loader entry
    """
    
    fe_text.set(tkFileDialog.askopenfilename())
    
def load_world():

    # Tricky users, can never trust 'em...
    if fe_text.get() == '':

        tkMessageBox.showerror('No world', 'World file entry is empty')
        return

    root.quit()
    root.destroy()

    def run_world(win):

        try:

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
            k = KeyboardPlayerController(p)

            def clean_up():

                for file in world_file.namelist():

                    os.remove(file)

                os.chdir(os.pardir)
                os.rmdir(tmpdir)

        
            atexit.register(clean_up)

        # The exceptions don't work right now, for some reason...
        except IOError as error:

            s = str(error)
            tkMessageBox.showerror(message=s[s.index(']') + 2:])
            clean_up()

        except Exception as error:

            s = str(error)
            tkMessageBox.showerror(message=s)
            clean_up()

    obengine.gfx.init(run_world)
        
    

root = ttk.Frame()

style = ttk.Style()

# clam looks best out of the default themes
style.theme_use('clam')

# Create the GUI

label = ttk.Label(root, text = 'World file')
label.pack(side = Tkinter.LEFT)

fe_text = Tkinter.StringVar(root)
file_entry = ttk.Entry(root, textvariable = fe_text)
file_entry.pack(side = Tkinter.LEFT)

browse_button = ttk.Button(root, command = set_text, text = 'Browse...')
browse_button.pack(side = Tkinter.LEFT)

load_button = ttk.Button(root, command = load_world, text = 'Load world')
load_button.pack(side = Tkinter.BOTTOM)

root.pack()

root.master.title('OpenBlox World Launcher')
root.mainloop()