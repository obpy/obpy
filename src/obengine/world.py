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
__date__ ="$Jul 13, 2010 6:30:46 PM$"

import attrdict

class World(object):
    """
    OpenBlox's world model.
    It handles high-level things, like adding/removing players
    and elements. It does not, by itself, handle things like rendering, or other things like that.
    """

    def __init__(self, max_players, name):
        """
        max_players is the number of players that can play at once.
        name is what you you want to call this world.
        """

        self.max_players = max_players
        self.num_players = 0

        self.element = attrdict.AttrDict()
        self.player = attrdict.AttrDict()

        # Puzzled? Go look at attrdict.py

        self.name = name

    def load_world(self, world_source):
        """
        Loads a world, element by element.
        world_source can be anything that implements __getitem__.
        """

        for element in world_source:

            self.add_element(element)

    def add_element(self, element):
        """
        Adds an element(a subclass of class Element in element.py) to the world.
        You should probably call load_world instead.
        """

        self.element[element.name] = element
        element.on_add(self)

    def remove_element(self, name):
        """
        Removes an element with its name contained in name.
        There are a few cases where you should call this.
        """

        self.element[name].on_remove()
        del self.element[name]

    def add_player(self, player):
        """
        Adds a player to the game.
        player must be an instance of class Player(in player.py)
        """

        if not self.is_full():

            self.player[player.name] = player
            player.on_joined(self)
            self.num_players += 1

        else:

            player.on_full(self)

    def remove_player(self, name):
        """
        Removes a player from the game; the players name is contained in name.
        """

        self.player[name].on_leave()
        del self.player[name]
        self.num_players -= 1

    # Thats most of the interesting functions. The rest are just helpers..

    def is_full(self):
        """
        Returns True if we can't take any more players; False if otherwise.
        """

        return self.max_players == self.num_players

    def __tolua__(self):
        return 'World'