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
__date__ ="$Jul 14, 2010 12:19:08 AM$"

import lupa
import luautils

from obengine.utils import error
from obengine.attrdict import AttrDict

# Default globals that lupa creates its lua runtime is created.
# We don't want to expose these, so we make a list here

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
'loadfile',

]

class ScriptEngine(object):
    """
    OpenBlox's powerful script engine class. Use this to run Lua scripts, by calling execute.
    You can also expose Python objects, by calling expose.

    Also, this class has attributes(namely, method and var) that exposes all Lua methods and variables:
    Example:

    lua = ScriptEngine()

    lua.execute('''
    function hello()
    print("Hello Python world!")
    end
    '''

    lua.method.hello()

    This should output:

    Hello Python world!
    """
    
    def __init__(self, filename = '<stdin>', error_cb = None):
        """
        If error_cb is None(i.e, not given), error messages are printed on stdout.
        """

        if error_cb:

            self.error_cb = error_cb

        else:

            self.error_cb = self.default_error_cb

        self.lua = lupa.LuaRuntime()
        self.filename = filename

        self.var = AttrDict()
        self.method = AttrDict()

    def eval(self, string):
        """
        Return the result of a Lua script.
        If the script is invalid, error_cb is called.
        """

        try:

            return self.lua.eval(string)

            for key in self.lua.globals():

                if key not in default_globals:

                    if str(self.lua.globals()['type'](self.globals()[key])) != u'function':

                        self.var[key] = self.globals()[key]

                    elif str(self.lua.globals()['type'](self.globals()[key])) == u'function':

                        self.method[key] = self.globals()[key]

        except Execption as exc:

            self.error_cb(exc.message)

    def execute(self, string):
        """
        Runs a Lua script; nothing(None) is returned.
        If the script is invalid, error_cb is called.
        """

        try:

            self.lua.execute(string)

            for key in self.lua.globals():

                if key not in default_globals:

                    if str(self.lua.globals()['type'](self.globals()[key])) != u'function':

                        self.var[key] = self.globals()[key]

                    elif str(self.lua.globals()['type'](self.globals()[key])) == u'function':

                        self.method[key] = self.globals()[key]

        except Exception as exc:
            
            self.error_cb(exc.message)

    def expose(self, obj):
        """
        Exposes obj to the Lua interpreter.
        If obj has a __tolua__ method, the return value of that method is used as the exposed
        name. Otherwise, obj's class name is used.
        """

        if hasattr(obj, '__tolua__'):

            self.lua.globals()[obj.__tolua__()] = obj

        else:
            
            self.lua.globals()[obj.__class__.__name__] = obj

    def default_error_cb(self, msg):

        error('Script error: Script ' + self.filename + ', error: ' + msg)
        
    def globals(self):
        
        return self.lua.globals()