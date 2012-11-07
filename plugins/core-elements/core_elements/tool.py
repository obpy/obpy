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
__date__ = "Dec 19, 2011 3:58:46 PM"


import obengine.interface
import obengine.event
import obengine.async
import obengine.vfs
import obengine.plugin
import obengine.element
import obengine.gfx.player
import obengine.gfx.worldsource


TOOL_DIR = 'tools'


class ToolElement(obengine.element.Element):

    def __init__(self, name, script, model = None):

        obengine.element.Element.__init__(self, name)

        self._script = script
        self._model = model
        if self._model is not None:
            self._model.hide()
        self._player = None

        self.on_equipped = obengine.event.Event()
        self.on_unequipped = obengine.event.Event()
        self._equipped = False

        self.on_parent_changed += self._check_for_equip

        self._script.parent = self
        self._script.execute()

        if TOOL_DIR not in obengine.vfs.listdir('/'):
            obengine.vfs.mount('/' + TOOL_DIR, obengine.fs.MemoryFS)

    def equip(self):

        assert self._player is not None

        self._model.show()
        self._equipped = True
        self.on_equipped()

    def unequip(self):

        assert self._player is not None

        self._model.hide()
        self._equipped = False
        self.on_unequipped()

    @property
    def equipped(self):
        return self._equipped

    def _check_for_equip(self, new_parent):

        if obengine.interface.implements(new_parent, obengine.gfx.player.PlayerController):

            self._player = new_parent

            if self._model is not None:
                # TODO: Replace use of private attributes here with something better!
                self._model.parent = self._player._view._model

        else:

            self._model.parent = self._model.window
            self._player = None


class XmlToolParser(obengine.element.XmlElementParser):

    tag = 'tool'

    def parse(self, node):

        name = node.attrib['name']

        script_path = obengine.vfs.getsyspath('/data/%s/%s/tool.lua' % (TOOL_DIR, name))
        element_factory = obengine.elementfactory.ElementFactory()
        tool_script = element_factory.make('tool-script', script_path)

        import obplugin.core.graphics

        mesh_path = node.attrib.get('mesh', None)
        tool_mesh = None
        if mesh_path is not None:

            mesh_path = obengine.vfs.getsyspath('/data/%s/%s/%s' % (TOOL_DIR, name, mesh_path))
            tool_mesh = obplugin.core.graphics.Model(mesh_path, element_factory.window)
            tool_mesh.load()
            obengine.async.wait_on(tool_mesh.load_okay, element_factory.window.scheduler)

        tool_element = ToolElement(name, tool_script, tool_mesh)
        return tool_element


obengine.gfx.worldsource.WorldSource.add_element_parser(XmlToolParser)
