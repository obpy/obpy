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
__date__ ="$Oct 25, 2010 9:57:22 PM$"

import copy

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.gui.OnscreenText import OnscreenText

import obengine.gfx
import obengine.player
import obengine.utils
import obengine.elementfactory

class PlayerController(object):

    def __init__(self, view):

        self.view = view

        self.init()

    def init(self): pass
    """
    This method is meant to be overridden in a derivatave.
    It initalizes the controller, which could mean adding
    key bindings, or another means to control the player.
    """


class KeyboardPlayerController(PlayerController):

    def init(self):
        
        obengine.gfx.get_rootwin().accept('arrow_up', self.view._move_f)
        obengine.gfx.get_rootwin().accept('arrow_down', self.view._move_b)
        obengine.gfx.get_rootwin().accept('arrow_left', self.view._rotate_l)
        obengine.gfx.get_rootwin().accept('arrow_right', self.view._rotate_r)

        obengine.gfx.get_rootwin().accept('arrow_up-repeat', self.view._move_f)
        obengine.gfx.get_rootwin().accept('arrow_down-repeat', self.view._move_b)
        obengine.gfx.get_rootwin().accept('arrow_left-repeat', self.view._rotate_l)
        obengine.gfx.get_rootwin().accept('arrow_right-repeat', self.view._rotate_r)

        obengine.gfx.get_rootwin().accept('space', self.view._jump)

    

class PlayerView(object):
    """
    If you're directly using OpenBlox from Python, use this class instead of obengine.player.Player.
    Experimental!
    """

    move_speed = 5

    def __init__(self, name):

        self.name = name
        self.player = obengine.player.Player(name, self)
        self.camera = obengine.gfx.get_rootwin().camera

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

        factory = obengine.elementfactory.ElementFactory()

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

            larm_joint_pos.append(self.world.element[self.name + '_torso'].brick.coords[index])
            lleg_joint_pos.append(self.world.element[self.name + '_torso'].brick.coords[index])
            rarm_joint_pos.append(self.world.element[self.name + '_torso'].brick.coords[index])
            rleg_joint_pos.append(self.world.element[self.name + '_torso'].brick.coords[index])

        joint1 = OdeHingeJoint(obengine.phys.get_phys_world())
        joint2 = OdeHingeJoint(obengine.phys.get_phys_world())
        joint3 = OdeHingeJoint(obengine.phys.get_phys_world())
        joint4 = OdeHingeJoint(obengine.phys.get_phys_world())
        joint5 = OdeHingeJoint(obengine.phys.get_phys_world())

        joint1.attach(self.world.element[self.name + '_torso'].phys_obj.body, self.world.element[self.name + '_larm'].phys_obj.body)
        joint2.attach(self.world.element[self.name + '_torso'].phys_obj.body, self.world.element[self.name + '_rarm'].phys_obj.body)
        joint3.attach(self.world.element[self.name + '_torso'].phys_obj.body, self.world.element[self.name + '_lleg'].phys_obj.body)
        joint4.attach(self.world.element[self.name + '_torso'].phys_obj.body, self.world.element[self.name + '_rleg'].phys_obj.body)
        joint5.attach(self.world.element[self.name + '_torso'].phys_obj.body, self.world.element[self.name + '_head'].phys_obj.body)

        joint1.setAxis(0, 1, 0)
        joint1.setAnchor(larm_joint_pos[0], larm_joint_pos[1], larm_joint_pos[2])
        joint1.setParamLoStop(0)
        joint1.setParamHiStop(0)

        joint2.setAxis(0, 1, 0)
        joint2.setAnchor(rarm_joint_pos[0], rarm_joint_pos[1], rarm_joint_pos[2])
        joint2.setParamLoStop(0)
        joint2.setParamHiStop(0)

        joint3.setAxis(0, 0, 1)
        joint3.setAnchor(*self.world.element[self.name + '_lleg'].brick.coords)
        joint3.setParamLoStop(0)
        joint3.setParamHiStop(0)

        joint4.setAxis(0, 0, 1)
        joint4.setAnchor(*self.world.element[self.name + '_rleg'].brick.coords)
        joint4.setParamLoStop(0)
        joint4.setParamHiStop(0)

        joint5.setAxis(0, 0, 1)
        joint5.setAnchor(*self.world.element[self.name + '_torso'].brick.coords)
        joint5.setParamLoStop(0)
        joint5.setParamHiStop(0)

        self.lleg_joint = joint3
        self.rleg_joint = joint4

    def _construct_gui(self):

        name_text = OnscreenText(text = 'you are ' + self.name, scale = (0.06, 0.06), pos = (0, 0.95, 1), bg = (0, 0, 0, 0.5), fg = (1, 1, 1, 0.9))

        obengine.gfx.get_rootwin().disableMouse()
        obengine.gfx.get_rootwin().taskMgr.add(self._update_camera, self.name + '_update', priority = 1)

    def _rotate_r(self):
        
        vel = self.world.element[self.name + '_torso'].phys_obj.body.getAngularVel()
        vel.setZ(-2)
        self.world.element[self.name + '_torso'].phys_obj.body.setAngularVel(vel)

    def _rotate_l(self):

       vel = self.world.element[self.name + '_torso'].phys_obj.body.getAngularVel()
       vel.setZ(2)
       self.world.element[self.name + '_torso'].phys_obj.body.setAngularVel(vel)
        

    def _move_f(self):

        h = self._get_member('torso').brick.hpr[0]

        if -90 < h < 0:

            for name in self._get_all_members():

                heading = self._get_member(name).brick.hpr[0]
                pos = copy.copy(self._get_member(name).brick.coords)

                pos[0] += (1 - (heading / -90.0)) / self.move_speed
                pos[1] -= (heading / -90.0) / self.move_speed

                self._get_member(name).set_pos(*pos)

        elif 0 < h < 90:

            for name in self._get_all_members():

                heading = self._get_member(name).brick.hpr[0]
                pos = copy.copy(self._get_member(name).brick.coords)

                pos[0] += (1 - (heading / 90.0)) / self.move_speed
                pos[1] += (heading / 90.0) / self.move_speed

                self._get_member(name).set_pos(*pos)

        elif -180 < h < -90:

            for name in self._get_all_members():

                heading = self._get_member(name).brick.hpr[0]
                pos = copy.copy(self._get_member(name).brick.coords)

                pos[0] += (1 - (heading / -90.0)) / self.move_speed
                pos[1] -= ((1 - (heading / -90.0)) + 1) / self.move_speed

                self._get_member(name).set_pos(*pos)

        elif 90 < h < 180:

            for name in self._get_all_members():

                heading = self._get_member(name).brick.hpr[0]
                pos = copy.copy(self._get_member(name).brick.coords)

                pos[0] += (1 - (heading / 90.0)) / self.move_speed
                pos[1] += ((1 - (heading / 90.0)) + 1) / self.move_speed

                self._get_member(name).set_pos(*pos)



    def _move_b(self):

        h = self._get_member('torso').brick.hpr[0]

        if -90 < h < 0:

            for name in self._get_all_members():

                heading = self._get_member(name).brick.hpr[0]
                pos = copy.copy(self._get_member(name).brick.coords)

                pos[0] -= (1 - (heading / -90.0)) / self.move_speed
                pos[1] += (heading / -90.0) / self.move_speed

                self._get_member(name).set_pos(*pos)

        elif 0 < h < 90:

            for name in self._get_all_members():

                heading = self._get_member(name).brick.hpr[0]
                pos = copy.copy(self._get_member(name).brick.coords)

                pos[0] -= (1 - (heading / 90.0)) / self.move_speed
                pos[1] -= (heading / 90.0) / self.move_speed

                self._get_member(name).set_pos(*pos)

        elif -180 < h < -90:

            for name in self._get_all_members():

                heading = self._get_member(name).brick.hpr[0]
                pos = copy.copy(self._get_member(name).brick.coords)

                pos[0] -= (1 - (heading / -90.0)) / self.move_speed
                pos[1] += ((1 - (heading / -90.0)) + 1) / self.move_speed

                self._get_member(name).set_pos(*pos)

        elif 90 < h < 180:

            for name in self._get_all_members():

                heading = self._get_member(name).brick.hpr[0]
                pos = copy.copy(self._get_member(name).brick.coords)

                pos[0] -= (1 - (heading / 90.0)) / self.move_speed
                pos[1] -= ((1 - (heading / 90.0)) + 1) / self.move_speed

                self._get_member(name).set_pos(*pos)

    def _jump(self):

        self.world.element[self.name + '_torso'].phys_obj.body.setLinearVel(0, 0, 20)

    def _get_member(self, name, default = None):
        """
        Returns the given member name of this player.
        Returns default if name is not found.
        """

        return self.world.element.get(self.name + '_' + name, default)

    def _get_all_members(self):
        """
        Returns the names of all the members of this player.
        Meant to be used in conjunction with _get_member.
        """

        names = ['torso', 'head', 'larm', 'lleg', 'rarm', 'rleg']

        return names

    def _update_camera(self, task):

        pos = self._get_member('head').view.getPos()

        if obengine.cfg.get_config_var('viewmode') == 'fps':

            self.camera.setPos(*pos)

            hpr = self._get_member('head').view.getHpr()
            hpr[0] -= 90
            hpr[1] = 0
            hpr[2] = 0
            
            self.camera.setHpr(hpr)

        else:

            pos[0] = pos[0] - 70
            pos[1] = pos[1] - 80
            pos[2] = pos[2] + 60

            self.camera.setPos(*pos)
            self.camera.lookAt(self._get_member('head').view)

        return task.cont