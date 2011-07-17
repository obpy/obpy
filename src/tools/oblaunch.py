#!/usr/bin/env python

# A simple command-line OpenBlox game launcher.
# WARNING: This script is currently written for OpenBlox 0.6.2, and will not
# work with OpenBlox 0.7 (the current version OpenBlox, the one you're using now).
# See <TODO: no Sphinx docs yet - add some> for the main source of documentation
# for this script.

#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import shutil
import os
import sys
import zipfile
import tempfile
import atexit

import obengine
import obengine.world
import obengine.phys
import obengine.gfx.worldsource as worldsource
from obengine.gfx.player import PlayerView
from obengine.gfx.player import KeyboardPlayerController
from obengine.gfx.math import Vector


def load_world(game):

    def run_world(win):
        """
        Actually runs the world.
        win is a reference to the root Panda3D window.
        """

        obengine.phys.init()

        # Extract the file
        world_file = zipfile.ZipFile(os.path.join(os.path.abspath(__file__)[:-len(__file__)],os.path.join('games', game + '.zip')))

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
    sys.exit(0)

    obengine.cfg.init()
    obengine.utils.init()
    
    load_world(sys.argv[1])