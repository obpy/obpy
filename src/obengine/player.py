"""
Copyright (C) 2010 The OpenBlox Project

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
__date__ ="$Jul 13, 2010 6:15:27 PM$"

import obengine.event

class Player(object):
    """
    This class handles the model for OpenBlox's players. Nothing's really here.
    """

    def __init__(self, name):
        """
        name is what you want to call this player instance.
        """

        self.name = name

        self.on_joined = obengine.event.Event()
        self.on_leave = obengine.event.Event()
        self.on_full = obengine.event.Event()

        self.on_joined += self.player_on_joined
        self.on_leave += self.player_on_leave
        self.on_full += self.player_on_full

    def join_world(self, world):
        """
        Joins a world. world is the instance of the world you want to join.
        """

        world.add_player(self)

    def leave_world(self):
        """
        Leaves the world you joined.
        """

        self.world.remove_player(self)

    def player_on_joined(self, world):

        self.world = world
        self.playing = True

    def player_on_leave(self):
        self.playing = False

    def player_on_full(self, world):

        if not hasattr(self, 'playing'):

            # Just in case we weren't playing before
            self.playing = False