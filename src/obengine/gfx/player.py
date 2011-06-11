#
# Legacy module - will probably be removed/partitioned in the near future.
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
#
#
# Copyright (C) 2010-2011 The OpenBlox Project
#
# This file is part of The OpenBlox Game Engine.
#
#     The OpenBlox Game Engine is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     The OpenBlox Game Engine is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with The OpenBlox Game Engine.  If not, see <http://www.gnu.org/licenses/>.
#


__author__ = "openblocks"
__date__  = "$Oct 25, 2010 9:57:22 PM$"


import time
import copy

import obengine.gfx
import obengine.player
import obengine.utils
import obengine.elementfactory
import obengine.phys
from obengine.gfx.math import *


class PlayerController(object):
    """
    This class is not meant to be used directly (save for a new input device);
    instead, use one of its derivatives.

    This class abstracts the control mechanisim from the actual rendering of the player.
    """

    def __init__(self, view):

        self.view = view

        self._init()

    def _init(self): pass
    """
    This method is meant to be overridden in a derivatave.
    It initalizes the controller, which could mean adding
    key bindings, or another means to control the player.
    """


class KeyboardPlayerController(PlayerController):

    jump_interval = 2

    def _init(self):

        # Set up our key map, which maps key names to their current state

        self.key_map = {
        'left' : False,
        'right' : False,
        'up' : False,
        'down' : False,
        'space' : False
        }


        # Set up our key bindings

        win = obengine.gfx.get_rootwin()

        win.accept('arrow_left', self.set_key, ['left', True])
        win.accept('arrow_left-up', self.set_key, ['left', False])
        win.accept('arrow_right', self.set_key, ['right', True])
        win.accept('arrow_right-up', self.set_key, ['right', False])
        win.accept('arrow_up', self.set_key, ['up', True])
        win.accept('arrow_up-up', self.set_key, ['up', False])
        win.accept('arrow_down', self.set_key, ['down', True])
        win.accept('arrow_down-up', self.set_key, ['down', False])

        win.accept('space', self.set_key, ['space', True])
        win.accept('space-up', self.set_key, ['space', False])

        # Update us every frame

        win.connect_on_update(self.update_player)

        # This is used to keep sneaky players from flying!
        # NOTE: This will eventually be replaced with something better,
        # like checking for a collision with ground
        self.last_jump_time = time.time()

    def set_key(self, key, val):
        self.key_map[key] = val

    def update_player(self, task):

        # Check our key map.
        # If any keys are pressed, perform their appropriate actions

        if self.key_map['left'] == True:
            self.view._rotate_l()

        elif self.key_map['right'] == True:
            self.view._rotate_r()

        if self.key_map['up'] == True:
            self.view._move_f()

        elif self.key_map['down'] == True:
            self.view._move_b()

        # Is the space key pressed, and the user waited long enough to jump again?
        if self.key_map['space'] == True and time.time() - self.last_jump_time > self.jump_interval:

            # Save the current time, and then jump
            self.last_jump_time = time.time()
            self.view._jump()

        # Make ourselves be called again
        return task.cont


class PlayerView(object):
    """
    If you're directly using OpenBlox from Python, use this class instead of obengine.player.Player.
    This is a full drop-in replacement for obengine.player.Player, for non-server (i.e, graphical) purposes.
    """

    # Dictates how fast we move
    move_speed = 5

    def __init__(self, name):
        """
        name is the name of this view. Just like obengine.player.Player.
        """

        self.name = name
        self.player = obengine.player.Player(name)
        self.camera = obengine.gfx.get_rootwin().camera

        self.player.on_joined += self.model_on_joined
        self.player.on_leave += self.model_on_leave
        self.player.on_full += self.model_on_full

    def join_world(self, world, pos = Vector(0, 0, 0)):
        """
        Joins the world world.
        pos is the position to initially start at.
        NOTE: pos will eventually be removed, and replaced with Spawn Points (see http://openblox.sf.net/idea/spawn-points)
        """

        self.pos = pos
        self.player.join_world(world)

    def leave_world(self):
        """
        Leaves a world.
        """
        self.player.leave_world()

    def model_on_joined(self, world):

        self.joined = True
        self.world = world

        self._construct_avatar(self.pos)
        self._construct_gui()

    def model_on_full(self, **kwargs): error('World full')

    def model_on_leave(self, **kwargs):
        del self.world

    def _construct_avatar(self, pos = Vector(0, 0, 0)):
        """
        Actually builds the avatar.
        Currently, the avatar always has yellow arms, legs, and head, with a blue torso,
        but soon it will be re-configurable on a user-to-user basis.
        """

        factory = obengine.elementfactory.ElementFactory()

        yellow = Color(238, 238, 0, 255)
        blue = Color(0, 0, 128, 255)

        self.world.add_element(factory.make('brick', self.name + '_torso', pos, blue, Vector(2, 4, 2)))
        self.world.add_element(factory.make('brick', self.name + '_head', Vector(pos.x, pos.y, pos.z + 3), yellow, Vector(2, 2, 1)))
        self.world.add_element(factory.make('brick', self.name + '_lleg', Vector(pos.x, pos.y - 1, pos.z - 4), yellow, Vector(2, 2, 2)))
        self.world.add_element(factory.make('brick', self.name + '_rleg', Vector(pos.x, pos.y + 1, pos.z - 4), yellow, Vector(2, 2, 2)))
        self.world.add_element(factory.make('brick', self.name + '_larm', Vector(pos.x, pos.y - 3, pos.z), yellow, Vector(2, 2, 2)))
        self.world.add_element(factory.make('brick', self.name + '_rarm', Vector(pos.x, pos.y + 3, pos.z), yellow, Vector(2, 2, 2)))

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

        OnscreenText(text = self.name, scale = (0.06, 0.06), pos = (0, 0.95, 1), bg = (0, 0, 0, 0.5), fg = (1, 1, 1, 0.9))

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

        # See moveexp.txt for what this means

        h = self._get_member('torso').brick.hpr.h

        if -90 < h < 0:

            for name in self._get_all_members():

                heading = self._get_member(name).brick.hpr.h
                pos = copy.copy(self._get_member(name).brick.coords)

                pos.x += (1 - (heading / -90.0)) / self.move_speed
                pos.y -= (heading / -90.0) / self.move_speed

                self._get_member(name).set_pos(pos)

        elif 0 < h < 90:

            for name in self._get_all_members():

                heading = self._get_member(name).brick.hpr.h
                pos = copy.copy(self._get_member(name).brick.coords)

                pos.x += (1 - (heading / 90.0)) / self.move_speed
                pos.y += (heading / 90.0) / self.move_speed

                self._get_member(name).set_pos(pos)

        elif -180 < h < -90:

            for name in self._get_all_members():

                heading = self._get_member(name).brick.hpr.h
                pos = copy.copy(self._get_member(name).brick.coords)

                pos.x += (1 - (heading / -90.0)) / self.move_speed
                pos.y -= ((1 - (heading / -90.0)) + 1) / self.move_speed

                self._get_member(name).set_pos(pos)

        elif 90 < h < 180:

            for name in self._get_all_members():

                heading = self._get_member(name).brick.hpr.h
                pos = copy.copy(self._get_member(name).brick.coords)

                pos.x += (1 - (heading / 90.0)) / self.move_speed
                pos.y += ((1 - (heading / 90.0)) + 1) / self.move_speed

                self._get_member(name).set_pos(pos)



    def _move_b(self):

        # See moveexp.txt for what this means

        h = self._get_member('torso').brick.hpr.h

        if -90 < h < 0:

            for name in self._get_all_members():

                heading = self._get_member(name).brick.hpr.h
                pos = copy.copy(self._get_member(name).brick.coords)

                pos.x -= (1 - (heading / -90.0)) / self.move_speed
                pos.y += (heading / -90.0) / self.move_speed

                self._get_member(name).set_pos(pos)

        elif 0 < h < 90:

            for name in self._get_all_members():

                heading = self._get_member(name).brick.hpr.h
                pos = copy.copy(self._get_member(name).brick.coords)

                pos.x -= (1 - (heading / 90.0)) / self.move_speed
                pos.y -= (heading / 90.0) / self.move_speed

                self._get_member(name).set_pos(pos)

        elif -180 < h < -90:

            for name in self._get_all_members():

                heading = self._get_member(name).brick.hpr.h
                pos = copy.copy(self._get_member(name).brick.coords)

                pos.x -= (1 - (heading / -90.0)) / self.move_speed
                pos.y += ((1 - (heading / -90.0)) + 1) / self.move_speed

                self._get_member(name).set_pos(pos)

        elif 90 < h < 180:

            for name in self._get_all_members():

                heading = self._get_member(name).brick.hpr.h
                pos = copy.copy(self._get_member(name).brick.coords)

                pos.x -= (1 - (heading / 90.0)) / self.move_speed
                pos.y -= ((1 - (heading / 90.0)) + 1) / self.move_speed

                self._get_member(name).set_pos(pos)

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
        """
        Updates the camera's position.
        Currently, 2 positions are supported:

        * FPS
        * Adventure/Isometric

        A third-person view with the camera always pointing directly at the player's back is
        in the offing.
        """

        pos = copy.copy(self._get_member('head').brick.coords)

        if obengine.cfg.get_config_var('viewmode') == 'fps':

            # FPS view is very simple. Just move to wherever the player's head is, and copy its hpr!

            self.camera.setPos(*pos)

            hpr = copy.copy(self._get_member('head').view.hpr)
            hpr.h -= 90
            hpr.p = 0
            hpr.r = 0

            self.camera.setHpr(*hpr)

        else:

            # Adventure/Isometric is also simple: Offset the camera a bit, and then look at the player's head.

            pos.x = pos.x - 70
            pos.y = pos.y - 80
            pos.z = pos.z + 60

            self.camera.setPos(*pos)
            self.camera.lookAt(self._get_member('head').view.model)

        # Set ourselves up to be called again
        return task.cont
