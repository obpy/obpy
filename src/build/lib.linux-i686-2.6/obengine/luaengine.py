__author__="openblocks"
__date__ ="$Jul 14, 2010 12:19:08 AM$"

import lua
import luautils

class ScriptEngine(object):

    def __init__(self, error_cb = None):

        if error_cb:

            self.error_cb = error_cb

        else:

            self.error_cb = self.default_error_cb

    def eval(self, string):

        try:

            return lua.eval(string)

        except RuntimeError as exc:

            self.error_cb(exc.message)

    def execute(self, string):

        try:

            lua.execute(string)

        except RuntimeError as exc:

            self.error_cb(exc.message)

    def expose(self, obj):

        lua_obj = luautils.LuaObjectWrapper(obj)
        lua.globals()[obj.__tolua__()] = lua_obj

    def default_error_cb(self, msg):

        print 'Script error, on line',str(msg.split(':')[2]).strip(' '),':',msg.split(':')[3]
        
    def globals(self):

        return lua.globals()