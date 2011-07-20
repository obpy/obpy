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
__date__  = "$Oct 25, 2010 9:57:22 PM$"


import obengine.plugin
import obengine.depman

obengine.depman.gendeps()


def init():
    obengine.plugin.require('core.hardware')


class PlayerController(object):

    LINEAR_SPEED = 5
    ROT_SPEED = 2

    def __init__(self, view):
        self._view = view

    def forward(self):
        self._view.linear_velocity.x = self.LINEAR_SPEED

    def backward(self):
        self._view.linear_velocity.x = -self.LINEAR_SPEED

    def linear_stop(self):
        self._view.linear_velocity.x = 0
        
    def left(self):
        self._view.rotational_velocity.z = -self.ROT_SPEED

    def right(self):
        self._view.rotational_velocity.z = self.ROT_SPEED

    def rotation_stop(self):
        self._view.rotational_velocity.z = 0


class KeyboardPlayerController(PlayerController):

    def __init__(self, view):

        import obplugin.core.hardware

        PlayerController.__init__(self, view)

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

