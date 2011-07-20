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

sys.path.append(os.path.abspath(os.curdir))
sys.path.append(os.path.abspath(os.pardir))

import obengine.environ
import obengine.world
import obengine.elementfactory
import obengine.gfx.worldsource as worldsource
import obengine.worldloader
import obengine.player
from obengine.gfx.player import PlayerView
from obengine.gfx.player import KeyboardPlayerController
from obengine.math import Vector


def load_world(game):

    # Extract the file
    game_file = zipfile.ZipFile(game)
    tmpdir = tempfile.mkdtemp()

    # Extract and change directories
    game_file.extractall(tmpdir)
    os.chdir(tmpdir)

    game_name = os.path.basename(game).strip('.zip')

    environ = obengine.environ.Environment(game_name)
    element_factory = obengine.elementfactory.ElementFactory()
    element_factory.set_window(environ.window)
    element_factory.set_sandbox(environ.physics_sandbox)


    # Open and parse the world
    source = worldsource.FileWorldSource('world.xml', element_factory)

    world = obengine.world.World(game_name, 1)
    worldloader = obengine.worldloader.WorldLoader(world, source, environ.scheduler)

    def create_player():

        # Initialize the player
        player_model = obengine.player.Player('OBPlayer')
        player_view = PlayerView(environ.window, Vector(-10, -10, -5))
        player_controller = KeyboardPlayerController(player_model, player_view)
        player_model.join_world(world)

    def clean_up():

        os.chdir(os.pardir)
        shutil.rmtree(tmpdir)

    atexit.register(clean_up)

    environ.window.on_loaded += lambda: environ.window.start_rendering()
    environ.window.on_loaded += lambda: environ.physics_sandbox.load()
    
    environ.physics_sandbox.on_loaded += lambda: source.parse()
    environ.physics_sandbox.on_loaded += lambda: worldloader.load()
    worldloader.on_world_loaded += lambda: environ.physics_sandbox.unpause()
    worldloader.on_world_loaded += lambda: create_player()

    environ.window.load()
    environ.scheduler.loop()


if __name__ == '__main__':

    obengine.init()
    load_world(sys.argv[1])