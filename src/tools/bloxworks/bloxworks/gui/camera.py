#
# <module description>
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
#
# Copyright (C) 2011 The OpenBlox Project
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
__date__ = "Aug 11, 2011 4:43:39 PM"


import obengine.math
import obengine.async
import obengine.plugin
import obengine.depman


obengine.depman.gendeps()


def init():

    obengine.plugin.require('core.graphics')
    obengine.plugin.require('core.hardware')


class CameraController(object):

    CAMERA_SPEED = 2.0

    def __init__(self, window):

        self._scheduler = window.scheduler

        self._enabled = False
        self._cam_trans_delta_x = 0.0
        self._cam_trans_delta_y = 0.0

        import obplugin.core.graphics
        self._camera = obplugin.core.graphics.Camera(window)

        import obplugin.core.hardware
        right_mouse = obplugin.core.hardware.MouseEvent.RIGHT_MOUSE
        mouse_down = obplugin.core.hardware.MouseEvent.TYPE_DOWN

        self._on_mouse_moved = obplugin.core.hardware.MouseMotionEvent(window)
        self._on_mouse_moved += self._move_camera

        self._on_rmb_down = obplugin.core.hardware.MouseEvent(
                                                              window,
                                                              right_mouse,
                                                              mouse_down)
        self._on_rmb_down += self.enable
        mouse_up = obplugin.core.hardware.MouseEvent.TYPE_UP
        self._on_rmb_up = obplugin.core.hardware.MouseEvent(
                                                            window,
                                                            right_mouse,
                                                            mouse_up)
        self._on_rmb_up += self.disable

        key_down = obplugin.core.hardware.KeyEvent.TYPE_DOWN
        key_up = obplugin.core.hardware.KeyEvent.TYPE_UP

        up_key = obplugin.core.hardware.KeyEvent.UP_KEY
        self._on_up_key_down = obplugin.core.hardware.KeyEvent(
                                                               window,
                                                               up_key,
                                                               key_down)
        self._on_up_key_down += self._move_cam_forward
        self._on_up_key_up = obplugin.core.hardware.KeyEvent(
                                                             window,
                                                             up_key,
                                                             key_up)
        self._on_up_key_up += self._stop_moving_cam_trans

        down_key = obplugin.core.hardware.KeyEvent.DOWN_KEY
        self._on_down_key_down = obplugin.core.hardware.KeyEvent(
                                                                window,
                                                                down_key,
                                                                key_down)
        self._on_down_key_down += self._move_cam_back
        self._on_down_key_up = obplugin.core.hardware.KeyEvent(
                                                               window,
                                                               down_key,
                                                               key_up)
        self._on_down_key_up += self._stop_moving_cam_trans

        left_key = obplugin.core.hardware.KeyEvent.LEFT_KEY
        self._on_left_key_down = obplugin.core.hardware.KeyEvent(
                                                                window,
                                                                left_key,
                                                                key_down)
        self._on_left_key_down += self._move_cam_left
        self._on_left_key_up = obplugin.core.hardware.KeyEvent(
                                                               window,
                                                               left_key,
                                                               key_up)
        self._on_left_key_up += self._stop_moving_cam_trans

        right_key = obplugin.core.hardware.KeyEvent.RIGHT_KEY
        self._on_right_key_down = obplugin.core.hardware.KeyEvent(
                                                                window,
                                                                right_key,
                                                                key_down)
        self._on_right_key_down += self._move_cam_right
        self._on_right_key_up = obplugin.core.hardware.KeyEvent(
                                                                window,
                                                                right_key,
                                                                key_up)
        self._on_right_key_up += self._stop_moving_cam_trans

        self._scheduler.add(obengine.async.Task(self._move_cam_trans))

    def disable(self):
        self._enabled = False

    def enable(self):
        self._enabled = True

    def _move_camera(self, mouse_pos):

        if self._enabled is False:

            self._on_down_key_down.disable()
            self._on_left_key_down.disable()
            self._on_right_key_down.disable()
            self._on_up_key_down.disable()
            return

        self._on_down_key_down.enable()
        self._on_left_key_down.enable()
        self._on_right_key_down.enable()
        self._on_up_key_down.enable()

        mouse_x_delta = self._on_mouse_moved.old_mouse_x - mouse_pos.x
        mouse_y_delta = mouse_pos.y - self._on_mouse_moved.old_mouse_y

        cam_rotation = self._camera.rotation
        cam_rotation.h += mouse_x_delta
        cam_rotation.p += mouse_y_delta

        self._camera.rotation = cam_rotation

    def _move_cam_forward(self):
        self._cam_trans_delta_y = self.CAMERA_SPEED

    def _move_cam_back(self):
        self._cam_trans_delta_y = -self.CAMERA_SPEED

    def _move_cam_right(self):
        self._cam_trans_delta_x = self.CAMERA_SPEED

    def _move_cam_left(self):
        self._cam_trans_delta_x = -self.CAMERA_SPEED

    def _stop_moving_cam_trans(self):

        self._cam_trans_delta_x = 0.0
        self._cam_trans_delta_y = 0.0

    def _move_cam_trans(self, task):

        if self._cam_trans_delta_x == 0.0 and self._cam_trans_delta_y == 0.0:
            return task.AGAIN

        velocity = obengine.math.Vector(self._cam_trans_delta_x, self._cam_trans_delta_y, 0)
        self._camera.move(velocity)

        return task.AGAIN
