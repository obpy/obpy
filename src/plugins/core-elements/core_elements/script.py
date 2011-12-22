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
__date__ = "Dec 1, 2011 2:44:58 PM"


import obengine.element
import obengine.depman

obengine.depman.gendeps()


class ScriptElement(obengine.element.Element):

    def __init__(self, name, scheduler, filename = None, code = None):

        obengine.element.Element.__init__(self, name)
        self.set_extension('xml', XmlScriptExtension)

        if filename != None:
            self.code = open(filename, 'r').read()

        else:
            self.code = code

        self.on_add += self.script_on_add
        self.on_world_loaded += self.script_on_loaded

        self.scheduler = scheduler

    def script_on_add(self, scene_graph):
        self.world = scene_graph.owner

    def script_on_loaded(self):
        self.run()

    def run(self):

        import obengine.plugin
        obengine.plugin.require('core.scripting')

        import obplugin.core.scripting
        import obengine.elementfactory

        self.script_engine = obplugin.core.scripting.ScriptEngine(self.name)

        self.script_engine.expose(self.world)
        self.script_engine.expose(self)
        self.script_engine.expose(obengine.elementfactory.ElementFactory())
        self.script_engine.expose(LuaFactory())
        self.script_engine.execute(self.code)
        self.script_engine.expose(obengine.vfs.get_global_filesystem(), 'Filesystem')

    def __tolua__(self):
        return 'Script'


class XmlScriptExtension(object):

    def __init__(self, script):
        self._script = script

    @property
    def xml_element(self):

        attributes = {
        'name' :  self._script.name
        }

        element = xmlparser.Element('script', attributes)
        element.text = self._script.code

        return element


class ScriptMaker(obengine.element.ElementMaker):

    element_name = 'script'

    def set_window(self, window):
        self._window = window

    def make(self, name, code, filename = None):

        element = ScriptElement(name, self._window.scheduler, filename, code)
        return element


class LuaFactory(object):

    def __init__(self):

        import obengine.math
        import obengine.async
        import obengine.gui

        self.factory_items = {
        'Vector' : obengine.math.Vector,
        'Vector2D' : obengine.math.Vector2D,
        'Color' : obengine.math.Color,
        'EulerAngle' : obengine.math.EulerAngle,

        'Task' : obengine.async.Task,
        'DelayedTask' : obengine.async.DelayedTask,
        'PeriodicTask' : obengine.async.PeriodicTask,
        'LoopingCall' : obengine.async.LoopingCall,
        'AsyncCall' : obengine.async.AsyncCall,

        'WidgetFactory' : obengine.gui.WidgetFactory
        }

    def make(self, item, *args):

        if item in self.factory_items.keys():
            return self.factory_items[item](*args)

    def __tolua__(self):
        return 'LuaFactory'
