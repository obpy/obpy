# panda_hardware
# ===================
#
# Panda3D hardware abstraction plugin.
#
# Copyright (C) 2011 The OpenBlox Project
# License: GNU GPL v3
#
# See <TODO: No Sphinx docs yet - add some!> for the primary source of documentation
# for this module.

__author__ = "openblocks"
__date__  = "$Jun 1, 2011 7:55:43 PM$"

import obengine.cfg
import obengine.event
import obengine.depman

obengine.depman.gendeps()

def init():

    config_src = obengine.cfg.Config()

    a_key = config_src.get_str('a_key', 'core.hardware')
    b_key = config_src.get_str('b_key', 'core.hardware')
    x_key = config_src.get_str('x_key', 'core.hardware')
    y_key = config_src.get_str('y_key', 'core.hardware')

    KeyEvent._key_conv[KeyEvent.A_KEY] = a_key
    KeyEvent._key_conv[KeyEvent.B_KEY] = b_key
    KeyEvent._key_conv[KeyEvent.X_KEY] = x_key
    KeyEvent._key_conv[KeyEvent.Y_KEY] = y_key

class KeyEvent(obengine.event.Event):

    A_KEY = 0
    B_KEY = 1
    X_KEY = 2
    Y_KEY = 3

    _key_conv = {

    A_KEY : 'q',
    B_KEY : 'w',

    X_KEY : 's',
    Y_KEY : 'd'

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