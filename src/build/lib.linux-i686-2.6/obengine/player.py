__author__="openblocks"
__date__ ="$Jul 13, 2010 6:15:27 PM$"

class Player(object):
    """
    This class handles the model for OpenBlox's players. Nothing's really here.
    """

    def __init__(self, name, event_handler):
        """
        name is what you want to call this player instance.
        """

        self.name = name
        self.event_handler = event_handler

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

    def on_joined(self, world):

        self.event_handler.on_joined(self, { 'world' :  world })
        self.world = world
        self.playing = True

    def on_leave(self):

        self.event_handler.on_leave(self, { 'world' : self.world })
        self.playing = False

    def on_full(self, world):

        if not hasattr(self, 'playing'):

            # Just in case we weren't playing before
            self.playing = False

        self.event_handler.on_full(self, { 'world' : world })