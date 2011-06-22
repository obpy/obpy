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
__date__  = "$Jun 1, 2011 7:55:43 PM$"


import obengine.cfg
import obengine.event
import obengine.depman

obengine.depman.gendeps()


def init():

    config_src = obengine.cfg.Config()

    a_key = config_src.get_str('a_key', 'core.hardware', '').lower()
    b_key = config_src.get_str('b_key', 'core.hardware', '').lower()
    x_key = config_src.get_str('x_key', 'core.hardware', '').lower()
    y_key = config_src.get_str('y_key', 'core.hardware', '').lower()

    if a_key != '':
        KeyEvent._key_conv[KeyEvent.A_KEY] = a_key

    if b_key != '':
        KeyEvent._key_conv[KeyEvent.B_KEY] = b_key
        
    if x_key != '':
        KeyEvent._key_conv[KeyEvent.X_KEY] = x_key

    if y_key != '':
        KeyEvent._key_conv[KeyEvent.Y_KEY] = y_key


class KeyEvent(obengine.event.Event):

    A_KEY = 0
    B_KEY = 1
    X_KEY = 2
    Y_KEY = 3

    _key_conv = {

    A_KEY : 'a',
    B_KEY : 's',

    X_KEY : 'x',
    Y_KEY : 'c'

    }

    TYPE_REPEAT = 0
    TYPE_DOWN = 1
    TYPE_UP = 2

    _type_conv = {

    TYPE_REPEAT : 'repeat',
    TYPE_DOWN : 'down',
    TYPE_UP : 'up'

    }

    def __init___(self, window, key, event_type, *args):

        self._panda_key = KeyEvent._key_conv[key]
        self._panda_evt_type = KeyEvent._type_conv[event_type]
        self._window = window

        self._key = key
        self._event_type = event_type

        self._method_args = args

    def enable(self):
        
        self._window.panda_window.accept(
        '%s-%s' % (self._panda_key, self._panda_evt_type),
        self.fire,
        self._method_args
        )

    @property
    def key(self):
        return self._key

    @property
    def event_type(self):
        return self._event_type
