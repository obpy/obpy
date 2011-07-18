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
__date__  = "$Jul 16, 2011 11:06:26 PM$"


import xml.etree.ElementTree

import obengine

import bloxworks.project


class ProjectPackagerVisitor(bloxworks.project.ProjectVisitor):
    
    def __init__(self, outfile):
        self.outfile = outfile

    def visit(self, project):

        class_map = {
        'BrickPresenter' : 'brick',
        'ScriptElement' : 'script',
        'SkyboxElement' : 'skybox',
        'SoundElement' : 'sound'
        }

        element_handlers = {
        'brick' : self._serialize_brick,
        'script' : self._serialize_script,
        'skybox' : self._serialize_skybox,
        'sound' : self._serialize_sound
        }

        scene_graph = project.world.element

        for scene_node in scene_graph.nodes.itervalues():

            node_type = class_map[scene_node.__class__.__name__]
            handler = element_handlers[node_type]

            raw_data = handler(scene_node)

    def _make_root_node(self):

        root_node_attribs = {
        'version' : obengine.version_string()
        }

        root_node = xml.etree.ElementTree.Element('world', root_node_attribs)
        return root_node