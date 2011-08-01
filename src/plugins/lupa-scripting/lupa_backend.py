#
# This plugin provides a Lupa (http://pypi.python.org/pypi/lupa)-based scripting
# engine implementation.
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
__date__  = "$May 2, 2011 1:15:36 AM$"


import sys

import lupa

# Panda3D hack for errant Windows sys.path

if sys.platform == 'win32':

    sys.path.insert(0, 'C:\\Program Files\\OpenBlox')
    sys.path.insert(1, 'C:\\Program Files\\OpenBlox\\obengine\\scripting')

from obengine.utils import error
import obengine.event


# Default globals that lupa/LuaJIT creates when its lua runtime is created.
# We don't want to expose these, so we make a list of them here.

default_globals = [

'string',
'xpcall',
'package',
'tostring',
'gcinfo',
'os',
'unpack',
'require',
'getfenv',
'setmetatable',
'next',
'assert',
'tonumber',
'io',
'rawequal',
'collectgarbage',
'jit',
'getmetatable',
'module',
'_G',
'python',
'bit',
'math',
'debug',
'pcall',
'table',
'coroutine',
'type',
'_VERSION',
'print',
'select',
'newproxy',
'dofile',
'rawget',
'loadstring',
'load',
'rawset',
'setfenv',
'pairs',
'ipairs',
'error',
'loadfile'
]


class ScriptEngine(object):
    """
    OpenBlox's powerful script engine class. Use this to run Lua scripts, by calling execute.
    You can also expose Python objects, by calling expose.

    Example:

        >>> lua = ScriptEngine()
        >>> lua.execute('''
        ... function hello()
        ... print("Hello Python world!")
        ... end
        ... hello()
        ... ''')
        Hello Python world!
    """

    def __init__(self, filename = '<stdin>'):
        """If error_cb is None(i.e, not given), error messages are printed on stdout.
        filename is the name of the Lua script being processed. If not given, it is
        automatically <stdin>. It's for error output only; nothing is read from the file
        that filename represents.
        """

        self.on_error = obengine.event.Event()

        # Create the Lua runtime
        self.lua = lupa.LuaRuntime()

        self.filename = filename

    def eval(self, string):
        """
        Return the result of a Lua script.
        If the script is invalid, error_cb is called.
        """

        try:

            val = self.lua.eval(string)
            return val

        # Houston, we have a problem...
        except Exception, message:
            self.on_error(message)

    def execute(self, string):
        """
        Runs a Lua script; nothing(None) is returned.
        If the script is invalid, error_cb is called.
        """
        try:

            self.lua.execute(string)
            self._update_globals()

        except Exception, message:
            self.on_error(message)
    def expose(self, obj):
        """Exposes obj to the Lua interpreter.
        If obj has a __tolua__ method, the return value of that method is used as the exposed
        name. Otherwise, obj's class name is used.
        """
        if hasattr(obj, '__tolua__'):
            self.lua.globals()[obj.__tolua__()] = obj
        else:
            self.lua.globals()[obj.__class__.__name__] = obj

    def _default_error_cb(self, msg):
        error('Script error: Script ' + self.filename + ', error: ' + msg)