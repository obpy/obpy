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
from pandac.PandaModules import *

from obengine.gfx import get_rootwin, get_phys_world
from obengine.player import Player
from obengine.utils import *
from obengine.element import ElementFactory

class PlayerController(object): pass

class PlayerView(object):
    """
    If you're directly using OpenBlox from Python, use this class instead of obengine.player.Player.
    Experimental!
    """

    def __init__(self, name):

        self.name = name
        self.player = Player(name, self)
        self.camera = get_rootwin().camera

    def join_world(self, world, pos = [0, 0, 0]):

        self.pos = pos
        self.player.join_world(world)

    def leave_world(self):

        self.player.leave_world()

    def on_joined(self, player, **kwargs):

        self.joined = True
        self.world = kwargs['world']

        self._construct_avatar(self.pos)
        self._construct_gui()
        
    def on_full(self, player, **kwargs): error('World full')

    def on_leave(self, player, **kwargs):

        del self.world

    def _construct_avatar(self, pos = [0, 0, 0]):

        factory = ElementFactory()

        self.world.add_element(factory.make('brick', self.name + '_torso', pos, [0, 0, 128, 255], [2, 4, 2]))
        self.world.add_element(factory.make('brick', self.name + '_head', [pos[0], pos[1], pos[2] + 3], [238, 238, 0, 255], [2, 2, 1]))
        self.world.add_element(factory.make('brick', self.name + '_lleg', [pos[0], pos[1] - 1, pos[2] - 4], [238, 238, 0, 255], [2, 2, 2]))
        self.world.add_element(factory.make('brick', self.name + '_rleg', [pos[0], pos[1] + 1, pos[2] - 4], [238, 238, 0, 255], [2, 2, 2]))
        self.world.add_element(factory.make('brick', self.name + '_larm', [pos[0], pos[1] - 3, pos[2]], [238, 238, 0, 255], [2, 2, 2]))
        self.world.add_element(factory.make('brick', self.name + '_rarm', [pos[0], pos[1] + 3, pos[2]], [238, 238, 0, 255], [2, 2, 2]))

        larm_joint_pos = []
        lleg_joint_pos = []
        rarm_joint_pos = []
        rleg_joint_pos = []

        for index, val in enumerate(self.world.element[self.name + '_torso'].brick.coords):

            larm_joint_pos.append(self.world.element[self.name + '_larm'].brick.coords[index])
            lleg_joint_pos.append(self.world.element[self.name + '_lleg'].brick.coords[index])
            rarm_joint_pos.append(self.world.element[self.name + '_rarm'].brick.coords[index])
            rleg_joint_pos.append(self.world.element[self.name + '_rleg'].brick.coords[index])

        joint1 = OdeHingeJoint(get_phys_world())
        joint2 = OdeHingeJoint(get_phys_world())
        joint3 = OdeHingeJoint(get_phys_world())
        joint4 = OdeHingeJoint(get_phys_world())
        joint5 = OdeHingeJoint(get_phys_world())

        joint1.attach(self.world.element[self.name + '_torso'].phys_obj.body, self.world.element[self.name + '_larm'].phys_obj.body)
        joint2.attach(self.world.element[self.name + '_torso'].phys_obj.body, self.world.element[self.name + '_rarm'].phys_obj.body)
        joint3.attach(self.world.element[self.name + '_torso'].phys_obj.body, self.world.element[self.name + '_lleg'].phys_obj.body)
        joint4.attach(self.world.element[self.name + '_torso'].phys_obj.body, self.world.element[self.name + '_rleg'].phys_obj.body)
        joint5.attach(self.world.element[self.name + '_torso'].phys_obj.body, self.world.element[self.name + '_head'].phys_obj.body)

        joint1.setAxis(0, 1, 0)
        joint1.setAnchor(larm_joint_pos[0], larm_joint_pos[1], larm_joint_pos[2])

        joint2.setAxis(0, 1, 0)
        joint2.setAnchor(rarm_joint_pos[0], rarm_joint_pos[1], rarm_joint_pos[2])

        joint3.setAxis(0, 1, 0)
        joint3.setAnchor(lleg_joint_pos[0], lleg_joint_pos[1], lleg_joint_pos[2])

        joint4.setAxis(0, 1, 0)
        joint4.setAnchor(rleg_joint_pos[0], rleg_joint_pos[1], rleg_joint_pos[2])

        joint5.setAxis(0, 0, 1)
        joint5.setAnchor(*self.world.element[self.name + '_torso'].brick.coords)
        
        
    def _construct_gui(self):

        pass