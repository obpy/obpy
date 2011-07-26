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
__date__  = "$Jul 14, 2011 4:19:44 PM$"


import ConfigParser
import os

import obengine
import obengine.world
import obengine.gfx.worldsource


PROJECT_CFG_FILE = 'project.ini'
WORLD_XML_FILE = os.path.join('bwproject', 'world.xml')


class Project(object):

    def __init__(self, world, author, ob_version):

        self.author = author
        self.ob_version = ob_version
        self.world = world
        self.path = path

    def accept(self, visitor):
        visitor.visit(self)

    @property
    def name(self):
        return self.world.name


class ProjectVisitor(object):

    def accept(self, project):
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
        self._path = path

        world_file = os.path.join(self._path, WORLD_XML_FILE)
        self._world_source = obengine.gfx.worldsource.FileWorldSource(
        element_factory,
        world_file)

    def load(self):

        self._parser.read(self._path)

        name = self._parser.get('project', 'name')
        author = self._parser.get('project', 'author')
        ob_version = self._parser.get('project', 'obversion')

        world = obengine.world.World(name, 1)
        project = Project(world, author, ob_version)

        self._world_source.parse()
        world.load_world(self._world_source)

        return project