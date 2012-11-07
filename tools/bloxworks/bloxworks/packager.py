#
# This module provides serialization (saving) of OpenBlox worlds for BloxWorks.
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
__date__ = "$Jul 16, 2011 11:06:26 PM$"


import xml.etree.ElementTree

import obengine
import bloxworks.project


class ProjectPackagerVisitor(bloxworks.project.ProjectVisitor):

    def __init__(self, outfile):
        self.outfile = outfile

    def visit(self, project):

        scene_graph = project.world.element
        root_node = self._make_node()

        for scene_node in scene_graph.nodes.itervalues():

            xml_node = scene_node.get_extension('xml').xml_element

            if xml_node is not None:
                root_node.append(xml_node)

        xml_tree = xml.etree.ElementTree.ElementTree(root_node)
        xml_tree.write(self.outfile)

    def _make_root_node(self):

        root_node_attribs = {
        'version' : obengine.version_string()
        }

        root_node = xml.etree.ElementTree.Element('world', root_node_attribs)
        return root_node
