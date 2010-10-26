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
__author__="openblocks"
__date__ ="$Oct 25, 2010 9:57:22 PM$"

from direct.gui.DirectGui import *

from obengine.gfx import get_rootwin
from obengine.player import Player
from obengine.utils import *
from obengine.element import ElementFactory

class PlayerController(object): pass

class PlayerView(object):

    def __init__(self, name):

        self.player = Player(name, self)

    def join_world(self, world):

        self.player.join_world(world)

    def leave_world(self):

        self.player.leave_world()

    def on_joined(self, **kwargs):

        self.joined = True
        self.world = kwargs['world']

        self._construct_avatar()
        self._construct_gui()

    def on_full(self, **kwargs): error('World full')

    def on_leave(self, **kwargs):

        del self.world


    def _construct_avatar(self, pos = [0, 0, 0]):

        factory = ElementFactory()
        self.world.add_element(factory.make(self.name + '_head', ))

    def _construct_gui(self):

        pass