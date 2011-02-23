# To change this template, choose Tools | Templates
# and open the template in the editor.
"""
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
__date__ ="$Jan 23, 2011 8:10:16 AM$"

from obengine.element import Element

class ScriptElement(Element):

    def __init__(self, name, filename = None, code = None):

        Element.__init__(self, name)

        if filename != None:
            self.code = open(filename, 'r').read()

        else:
            self.code = code

        self.on_add += self.script_on_add

    def script_on_add(self, world):

        from thread import start_new_thread

        self.world = world

        start_new_thread(self.run, ())


    def run(self):
        
        import obengine.scripting.luaengine as luaeng
        import obengine.elementfactory

        self.script_engine = luaeng.ScriptEngine(self.name)

        self.script_engine.expose(self.world)
        self.script_engine.expose(self)
        self.script_engine.expose(obengine.elementfactory.ElementFactory())
        self.script_engine.execute(self.code)

    def __tolua__(self):
        return 'Script'