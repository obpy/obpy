# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest
from world import *
from player import *

class  WorldTestCase(unittest.TestCase):
    
    def test_full_and_join(self):

        class TestHandler:

            def on_joined(self, player, args):

                self.playing = True

            def on_leave(self, player, args):

                self.playing = False

            def on_full(self, player, args):

                self.full = True

        h1 = TestHandler()
        p1 = Player('Player1', h1)

        h2 = TestHandler()
        p2 = Player('Player2', h2)

        h3 = TestHandler()
        p3 = Player('Player3', h3)

        w = World(2,"Test")

        w.add_player(p1)
        w.add_player(p2)
        w.add_player(p3)

        self.assertEqual(p1.playing, True, "p1 should be playing")
        self.assertEqual(p2.playing, True, "p2 should be playing")
        self.assertEqual(p3.playing, False, "p3 shouldn't be playing")

if __name__ == '__main__':
    unittest.main()

