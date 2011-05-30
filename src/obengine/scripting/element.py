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
import obengine.plugin
import obengine.depman

obengine.depman.gendeps()

def init():
    obengine.plugin.require('core.scripting')


class ScriptElement(Element):

    def __init__(self, name, filename = None, code = None):

        Element.__init__(self, name)

        if filename != None:
            self.code = open(filename, 'r').read()

        else:
            self.code = code

        self.on_add += self.script_on_add

    def script_on_add(self, scene_graph):

        from thread import start_new_thread

        self.world = scene_graph.world

        start_new_thread(self.run, ())


    def run(self):

        import obplugin.core.scripting
        import obengine.elementfactory

        self.script_engine = obplugin.core.scripting.ScriptEngine(self.name)
        
        self.script_engine.expose(self.world)
        self.script_engine.expose(self)
        self.script_engine.expose(obengine.elementfactory.ElementFactory())
        self.script_engine.expose(LuaFactory())
        self.script_engine.execute(self.code)

    def __tolua__(self):
        return 'Script'

class LuaFactory(object):

    def __init__(self):

        import obengine.gfx.math
        import obengine.hardware.event

        self.factory_items = {
        'Vector' : obengine.gfx.math.Vector,
        'Color' : obengine.gfx.math.Color,
        'EulerAngle' : obengine.gfx.math.EulerAngle,

        'KeyEvent' : obengine.hardware.event.KeyEvent,
        'TimerEvent' : obengine.hardware.event.TimerEvent
        }

    def make(self, item, *args):

        if item in self.factory_items.keys():
            return self.factory_items[item](*args)

    def __tolua__(self):
        return 'LuaFactory'