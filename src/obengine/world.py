# OpenBlox world model (obengine.world)
# =====================================
#
# Provides OpenBlox's high-level world model.
#
# Copyright (C) 2010 The OpenBlox Project
# License: GNU GPL v3
#
# See <TODO: no Sphinx docs yet - add some!> for the primary source of documentation
# for this module.

__author__ = "openblocks"
__date__  = "$Jul 13, 2010 6:30:46 PM$"

import obengine.scenegraph
import obengine.datatypes
import obengine.deprecated

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

        self.element = obengine.scenegraph.SceneGraph(self)
        self.player = obengine.datatypes.AttrDict()

        self.name = name

    def load_world(self, world_source):
        """
        Loads a world, element by element.
        world_source can be anything that implements __getitem__.
        """

        for element in world_source:
            self.add_element(element)

        for element in self.element.itervalues():
            element.on_world_loaded(self)

    def add_element(self, element):
        """
        .. deprecated:: 0.7
            Use `obengine.world.World.element.add_node` instead
            .
        Adds an element (a subclass of `obengine.element.Element`) to the world.
        """

        self.element.add_node(element)

    def remove_element(self, name):
        """
        .. deprecated:: 0.7
            Use `obengine.world.World.element.remove_node_by_name` instead.
            
        Removes an element with its name contained in name.
        """

        nid = self.element.get_node_by_name().nid
        self.element.remove_node_by_id(nid)

    def add_player(self, player):
        """
        Adds a player to the game.
        player should be an instance or a substitute of class Player(in player.py)
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

        if self.player.has_key(name):

            self.player[name].on_leave()
            del self.player[name]

            self.num_players -= 1

        else:
            raise KeyError(name)

    # That's most of the interesting functions. The rest are just helpers..

    def is_full(self):
        """
        Returns True if we can't take any more players; False if otherwise.
        """

        return self.max_players == self.num_players

    def __tolua__(self):
        return 'World'