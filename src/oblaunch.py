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
import obengine.world
import obengine.phys
import obengine.gfx.worldsource as worldsource

from obengine.gfx.player import PlayerView
from obengine.gfx.player import KeyboardPlayerController
from obengine.gfx.math import Vector

import shutil
import os
import sys

import zipfile
import tempfile

import atexit
    
def load_world(game):

    def run_world(win):
        """
        Actually runs the world.
        win is a reference to the root Panda3D window.
        """

        obengine.phys.init()

        # Extract the file
        world_file = zipfile.ZipFile(os.path.join(__file__[:len(__file__) - len('oblaunch.py') - 1],os.path.join('games', game + '.zip')))

        # We can't run inside the zip file, now can we? :)
        tmpdir = tempfile.mkdtemp()

        # Extract and change directories
        world_file.extractall(tmpdir)

        os.chdir(tmpdir)

        # Open and parse the world
        source = worldsource.FileWorldSource('world.xml')
        source.parse()


        # Start 'er up, Jack!
        world = obengine.world.World(game, 1)
        world.load_world(source)

        # Initalize the player
        p = PlayerView('OBPlayer')
        p.join_world(world, Vector(-10, -10, -5))
        KeyboardPlayerController(p)

        def clean_up():
            """
            Removes the temporary directory.
            """

            os.chdir(os.pardir)
            shutil.rmtree(tmpdir)

        atexit.register(clean_up)
        
    obengine.gfx.run(run_world)

if __name__ == '__main__':

    obengine.cfg.init()
    obengine.utils.init()
    
    load_world(sys.argv[1])