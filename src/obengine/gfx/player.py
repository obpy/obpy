#
# Legacy module - will probably be removed/partitioned in the near future.
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
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
__date__ = "$Oct 25, 2010 9:57:22 PM$"


from math import pi, sin, cos

import obengine.datatypes
import obengine.math
import obengine.async
import obengine.plugin
import obengine.depman

obengine.depman.gendeps()


def init():

    obengine.plugin.require('core.hardware')
    obengine.plugin.require('core.graphics')
    obengine.plugin.require('core.physics')


class PlayerController(object):

    LINEAR_SPEED = 20
    ROT_SPEED = 2

    def __init__(self, model, view):

        self._model = model
        self._view = view

        self._model.on_joined += lambda _: self._view.show()

    def forward(self):
        self._view.linear_velocity.y = self.LINEAR_SPEED

    def backward(self):
        self._view.linear_velocity.y = -self.LINEAR_SPEED

    def linear_stop(self):
        self._view.linear_velocity.y = 0

    def left(self):
        self._view.rotational_velocity.h = self.ROT_SPEED

    def right(self):
        self._view.rotational_velocity.h = -self.ROT_SPEED

    def rotation_stop(self):
        self._view.rotational_velocity.h = 0

    def jump(self):
        self._view.jump()


class KeyboardPlayerController(PlayerController):

    def __init__(self, model, view):

        import obplugin.core.hardware

        PlayerController.__init__(self, model, view)

        forward = obplugin.core.hardware.KeyEvent(
        self._view.window,
        obplugin.core.hardware.KeyEvent.UP_KEY)
        forward += self.forward

        forward_stop = obplugin.core.hardware.KeyEvent(
        self._view.window,
        obplugin.core.hardware.KeyEvent.UP_KEY,
        obplugin.core.hardware.KeyEvent.TYPE_UP)
        forward_stop += self.linear_stop

        backward = obplugin.core.hardware.KeyEvent(
        self._view.window,
        obplugin.core.hardware.KeyEvent.DOWN_KEY)
        backward += self.backward

        backward_stop = obplugin.core.hardware.KeyEvent(
        self._view.window,
        obplugin.core.hardware.KeyEvent.DOWN_KEY,
        obplugin.core.hardware.KeyEvent.TYPE_UP)
        backward_stop += self.linear_stop

        left = obplugin.core.hardware.KeyEvent(
        self._view.window,
        obplugin.core.hardware.KeyEvent.LEFT_KEY)
        left += self.left

        left_stop = obplugin.core.hardware.KeyEvent(
        self._view.window,
        obplugin.core.hardware.KeyEvent.LEFT_KEY,
        obplugin.core.hardware.KeyEvent.TYPE_UP)
        left_stop += self.rotation_stop

        right = obplugin.core.hardware.KeyEvent(
        self._view.window,
        obplugin.core.hardware.KeyEvent.RIGHT_KEY)
        right += self.right

        right_stop = obplugin.core.hardware.KeyEvent(
        self._view.window,
        obplugin.core.hardware.KeyEvent.RIGHT_KEY,
        obplugin.core.hardware.KeyEvent.TYPE_UP)
        right_stop += self.rotation_stop

        jump = obplugin.core.hardware.KeyEvent(
        self._view.window,
        obplugin.core.hardware.KeyEvent.JUMP_KEY)
        jump += self.jump


class PlayerView(object):

    def __init__(self, window, sandbox, position = None):

        import obplugin.core.graphics
        import obplugin.core.physics

        self.window = window
        self.window.panda_window.disableMouse()
        self._scheduler = self.window.scheduler
        self._model = obplugin.core.graphics.Model('avatar', self.window)
        self._model.load()

        self.linear_velocity = obengine.math.Vector()
        self.rotational_velocity = obengine.math.EulerAngle()

        while self._model.load_okay is False:
            self._scheduler.step()

        self._capsule = obplugin.core.physics.CharacterCapsule(
        sandbox, self, self._scheduler)
        self._capsule.load()
        while self._capsule.loaded is False:
            self._scheduler.step()
        self._scheduler.add(obengine.async.Task(self._update_velocity, priority = 5))

        if position is not None:
            self._model.position = position
        self._capsule.position = position or obengine.math.Vector()

        self._camera = obplugin.core.graphics.Camera(self.window)
        self._scheduler.add(obengine.async.Task(self._update_camera, priority = 5))

    def show(self):
        self._model.showing = True

    def jump(self):
        self._capsule.jump()

    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return self._capsule.position

        def fset(self, new_pos):
            self._capsule.position = new_pos

        return locals()

    def _update_velocity(self, task):

        self._capsule.linear_velocity = self.linear_velocity
        self._model.position.x = self._capsule.position.x
        self._model.position.y = self._capsule.position.y
        self._model.position.z = self._capsule.position.z + 6

        self._capsule.rotational_velocity = self.rotational_velocity
        self._model.rotation = self._capsule.rotation

        return task.AGAIN

    def _update_camera(self, task):

        DISTANCE_FROM_AVATAR = 60
        Z_OFFSET = 10

        model_rotation = self._model.rotation
        model_heading_radians = model_rotation.h * (pi / 180.0)

        cam_position = obengine.math.Vector(
                                            self._model.position.x,
                                            self._model.position.y,
                                            self._model.position.z)

        cam_position.x += DISTANCE_FROM_AVATAR * sin(model_heading_radians)
        cam_position.y += -DISTANCE_FROM_AVATAR * cos(model_heading_radians)
        cam_position.z += Z_OFFSET

        self._camera.position = cam_position
        self._camera.look_at(self._model)

        return task.AGAIN
