#!/usr/bin/env python
"""
This file is part of The OpenBlox Game Engine.

    The OpenBlox Game Engine is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    The OpenBlox Game Engine is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with The OpenBlox Game Engine.  If not, see <http://www.gnu.org/licenses/>.

"""

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
        """
        Actually runs the world.
        win is a reference to the root Panda3D window.
        """

        try:

            # Extract the file
            world_file = zipfile.ZipFile(fe_text.get())

            # We can't run inside the zip file, now can we? :)
            tmpdir = tempfile.mkdtemp()

            # Extract and change directories
            world_file.extractall(tmpdir)

            os.chdir(tmpdir)

            # Open and parse the world
            source = worldsource.FileWorldSource('world.xml')
            source.parse()

            # Start 'er up, Jack!
            world = obengine.World(os.path.basename(fe_text.get()).strip('.zip'), 1)
            world.load_world(source)

            # Initalize the player
            p = PlayerView('OBPlayer')
            p.join_world(world, [-10, -10, -5])
            k = KeyboardPlayerController(p)

            def clean_up():
                """
                Removes the temporary directory.
                """

                # We can't remove an empty directory, so we have to remove everything first...
                for file in world_file.namelist():

                    os.remove(file)

                # NOW we can remove it!
                os.chdir(os.pardir)
                os.rmdir(tmpdir)

            # Call the clean_up function at exit
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

    # Initalize the graphics
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