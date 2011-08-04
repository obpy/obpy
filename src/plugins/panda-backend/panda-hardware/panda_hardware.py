#
# This plugin provides a Panda3D-based hardware backend.
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
__date__ = "$Jun 1, 2011 7:55:43 PM$"


from panda3d.core import Point3

import obengine.cfg
import obengine.math
import obengine.event
import obengine.async
import obengine.depman

import obplugin.panda_utils

obengine.depman.gendeps()


def init():

    config_src = obengine.cfg.Config()

    a_key = config_src.get_str('a_key', 'core.hardware', '').lower()
    if a_key != '':
        KeyEvent._key_conv[KeyEvent.A_KEY] = a_key

    b_key = config_src.get_str('b_key', 'core.hardware', '').lower()
    if b_key != '':
        KeyEvent._key_conv[KeyEvent.B_KEY] = b_key

    x_key = config_src.get_str('x_key', 'core.hardware', '').lower()
    if x_key != '':
        KeyEvent._key_conv[KeyEvent.X_KEY] = x_key

    y_key = config_src.get_str('y_key', 'core.hardware', '').lower()
    if y_key != '':
        KeyEvent._key_conv[KeyEvent.Y_KEY] = y_key

    up_key = config_src.get_str('up_key', 'core.hardware', '').lower()
    if up_key != '':
        KeyEvent._key_conv[KeyEvent.UP_KEY] = up_key

    down_key = config_src.get_str('left_key', 'core.hardware', '').lower()
    if down_key != '':
        KeyEvent._key_conv[KeyEvent.DOWN_KEY] = down_key

    left_key = config_src.get_str('left_key', 'core.hardware', '').lower()
    if left_key != '':
        KeyEvent._key_conv[KeyEvent.LEFT_KEY] = left_key

    right_key = config_src.get_str('right_key', 'core.hardware', '').lower()
    if right_key != '':
        KeyEvent._key_conv[KeyEvent.RIGHT_KEY] = right_key

    jump_key = config_src.get_str('jump_key', 'core.hardware', '').lower()
    if jump_key != '':
        KeyEvent._key_conv[KeyEvent.JUMP_KEY] = jump_key


class KeyEvent(obengine.event.Event):

    A_KEY = 0
    B_KEY = 1
    X_KEY = 2
    Y_KEY = 3

    UP_KEY = 4
    DOWN_KEY = 5
    LEFT_KEY = 6
    RIGHT_KEY = 7
    JUMP_KEY = 8

    _key_conv = {

    A_KEY : 'a',
    B_KEY : 's',

    X_KEY : 'x',
    Y_KEY : 'c',

    UP_KEY : 'arrow_up',
    DOWN_KEY : 'arrow_down',
    LEFT_KEY : 'arrow_left',
    RIGHT_KEY : 'arrow_right',
    JUMP_KEY : 'space'

    }

    TYPE_REPEAT = 0
    TYPE_DOWN = 1
    TYPE_UP = 2

    _type_conv = {

    TYPE_REPEAT : '-repeat',
    TYPE_DOWN : '',
    TYPE_UP : '-up'

    }

    def __init__(self, window, key, event_type = TYPE_DOWN):

        obengine.event.Event.__init__(self)

        self._panda_key = KeyEvent._key_conv[key]
        self._panda_evt_type = KeyEvent._type_conv[event_type]
        self._window = window

        self._key = key
        self._event_type = event_type

        self._window.panda_window.accept(
        '%s%s' % (self._panda_key, self._panda_evt_type),
        self.fire
        )

    @property
    def key(self):
        return self._key

    @property
    def event_type(self):
        return self._event_type


class MouseEvent(obengine.event.Event):

    LEFT_MOUSE = 0
    RIGHT_MOUSE = 1
    MIDDLE_MOUSE = 2
    MOUSE_WHEEL = 3

    _mouse_conv = ['mouse1', 'mouse3', 'mouse2', 'wheel']

    TYPE_DOWN = 0
    TYPE_UP = 1
    TYPE_WHEEL_UP = 2
    TYPE_WHEEL_DOWN = 3

    _type_conv = ['', '-up', '_up', '_down']
    _created_handlers = {}


    def __init__(self, window, button, event_type, *args):

        obengine.event.Event.__init__(self)

        self._panda_button = MouseEvent._mouse_conv[button]
        self._panda_event_type = MouseEvent._type_conv[event_type]
        self._window = window

        self._button = button
        self._event_type = event_type
        self._method_args = args

        panda_str = '%s%s' % (self._panda_button, self._panda_event_type)
        if panda_str not in MouseEvent._created_handlers:

            MouseEvent._created_handlers[panda_str] = self
            self._window.panda_window.accept(
                                             panda_str,
                                             self.fire)
        else:
            MouseEvent._created_handlers[panda_str] += self

    @property
    def button(self):
        return self._button

    @property
    def event_type(self):
        return self._event_type


class MouseMotionEvent(obengine.event.Event):

    COORD_2D = 0
    COORD_3D = 1

    def __init__(self, window, coord_space = COORD_2D, z_value = 0):

        obengine.event.Event.__init__(self)

        self._window = window
        self._coord_space = coord_space
        self.z_value = z_value

        self._old_mouse_x = 0
        self._old_mouse_y = 0
        self._old_mouse_z = 0

        self._window.scheduler.add(obengine.async.Task(self._update_mouse_pos))

    def _update_mouse_pos(self, task):

        if not self._window.panda_window.mouseWatcherNode.hasMouse():
            return task.AGAIN

        mouse_pos_x = self._window.panda_window.mouseWatcherNode.getMouseX()
        mouse_pos_y = self._window.panda_window.mouseWatcherNode.getMouseY()

        if self._coord_space == MouseMotionEvent.COORD_3D:

            self._window.picker_ray.setFromLens(
            self._window.panda_window.camNode,
            mouse_pos_x,
            mouse_pos_y)

            near_point = self._window.panda_window.render.getRelativePoint(
            self._window.panda_window.camera,
            self._window.picker_ray.getOrigin())

            near_vector = self._window.panda_window.render.getRelativeVector(
            self._window.panda_window.camera,
            self._window.picker_ray.getOrigin())

            mouse_pos = point_at_z(self.z_value, near_point, near_vector)
            mouse_pos = obplugin.panda_utils.PandaConverter.convert_vec3(mouse_pos)

            if mouse_pos.x != self._old_mouse_x or mouse_pos.y != self._old_mouse_y or mouse_pos.z != self._old_mouse_z:

                self._old_mouse_x = mouse_pos.x
                self._old_mouse_y = mouse_pos.y
                self._old_mouse_z = mouse_pos.z

                self.fire(mouse_pos)

        else:

            mouse_pos_x *= obplugin.panda_utils.PANDA_TO_OPENBLOX_SCALE
            mouse_pos_y *= obplugin.panda_utils.PANDA_TO_OPENBLOX_SCALE

            mouse_pos = obengine.math.Vector2D(mouse_pos_x, mouse_pos_y)

            if mouse_pos.x != self._old_mouse_x or mouse_pos.y != self._old_mouse_y:

                self._old_mouse_x = mouse_pos.x
                self._old_mouse_y = mouse_pos.y

                self.fire(mouse_pos)

        return task.AGAIN


def point_at_z(z_value, point3, vec3):

    try:
        return point3 + vec3 * ((z_value - point3.getZ()) / vec3.getZ())

    except ZeroDivisionError:
        return Point3(0, 0, 0)
