#
# This module provides basic project functionality to BloxWorks.
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
__date__ = "$Jul 14, 2011 4:19:44 PM$"


import ConfigParser
import os
import xml.etree.ElementTree
import zipfile

import obengine.world
import obengine.vfs
import obengine.plugin
import obengine.elementfactory
import obengine.gfx.worldsource
import obengine.gfx.element3d


PROJECT_DIR = 'game'
PROJECT_CFG_FILE = 'project.ini'
WORLD_XML_FILE = os.path.join(PROJECT_DIR, 'world.xml')


class Project(object):

    def __init__(self, world, author, ob_version):

        self.author = author
        self.ob_version = ob_version
        self.world = world

    def accept(self, visitor):
        visitor.visit(self)

    @property
    def name(self):
        return self.world.name


class ProjectVisitor(object):

    def visit(self, project):
        # Override this in a subclass
        raise NotImplementedError


class ProjectCommand(object):

    def __init__(self, project):
        self.project = project

    def execute(self):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError


class ProjectLoader(object):

    def __init__(self, element_factory, path):

        self._parser = ConfigParser.ConfigParser()
        self.path = path

        world_file = os.path.join(self.path, WORLD_XML_FILE)
        self._world_source = obengine.gfx.worldsource.FileWorldSource(
        world_file,
        element_factory)

    def load(self):

        self._parser.read(os.path.join(self.path, PROJECT_CFG_FILE))
        name = self._parser.get('project', 'name')
        author = self._parser.get('project', 'author')
        ob_version = self._parser.get('project', 'obversion')

        world = obengine.world.World(0, name)
        project = Project(world, author, ob_version)

        self._world_source.parse()
        world.load_world(self._world_source)

        return project


class ProjectSaverVisitor(ProjectVisitor):

    def __init__(self, outfile):
        self.outfile = outfile

    def accept(self, project):

        scene_graph = project.world.element
        root_node = self._make_root_node()

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


class ProjectPackagerVisitor(ProjectVisitor):

    def __init__(self, outfile):
        self.outfile = outfile

    def accept(self, project):

        world_file = os.path.join(
                                  obengine.vfs.getsyspath('/bloxworks-games/' + project.world.name),
                                  WORLD_XML_FILE)

        zip_archive = zipfile.ZipFile(self.outfile, 'w')
        zip_archive.write(world_file, 'world.xml')


def load_project(path, window):

    element_factory = obengine.elementfactory.ElementFactory()
    element_factory.set_window(window)
    obengine.plugin.require('core.physics')
    import obplugin.core.physics
    physics_sandbox = obplugin.core.physics.World(gravity = 0)
    physics_sandbox.load()
    element_factory.set_sandbox(physics_sandbox)

    project_loader = ProjectLoader(element_factory, path)
    project = project_loader.load()

    obengine.vfs.open('/bloxworks-registry/project', 'w').write(project)
    obengine.vfs.open('/bloxworks-registry/sandbox', 'w').write(physics_sandbox)


def create_new_project(window, name, author):

    path = obengine.vfs.getsyspath('/bloxworks-games/' + name)

    os.mkdir(path)
    os.mkdir(os.path.join(path, PROJECT_DIR))
    open(os.path.join(path, WORLD_XML_FILE), 'w').write('')

    config_writer = ConfigParser.ConfigParser()
    config_writer.add_section('project')
    config_writer.set('project', 'obversion', obengine.version_string())
    config_writer.set('project', 'author', author)
    config_writer.set('project', 'name', name)
    config_writer.write(open(os.path.join(path, PROJECT_CFG_FILE), 'w'))

    world = obengine.world.World(0, name)
    world.element.add_node(obengine.gfx.element3d.CameraElement(window))
    project = Project(world, author, obengine.version_string())
    world.add_element(obengine.gfx.element3d.SkyboxElement(window))
    world.add_element(obengine.gfx.element3d.LightElement('ambient_light', window, 'ambient'))
    world.add_element(obengine.gfx.element3d.LightElement('sun_light', window))

    obengine.vfs.open('/bloxworks-registry/project', 'w').write(project)

    obengine.plugin.require('core.physics')
    import obplugin.core.physics
    physics_sandbox = obplugin.core.physics.World(gravity = 0)
    physics_sandbox.load()
    obengine.vfs.open('/bloxworks-registry/sandbox', 'w').write(physics_sandbox)
