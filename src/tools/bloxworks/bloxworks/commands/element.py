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
__date__  = "$Jul 25, 2011 6:03:21 PM$"


import bloxworks.project


class ElementCommand(bloxworks.project.ProjectCommand):

    def __init__(self, project, factory):

        bloxworks.project.ProjectCommand.__init__(self, project)
        self.factory = factory


class AddElementCommand(bloxworks.project.ProjectCommand):

    def __init__(self, project, factory, type, *args, **kwargs):

        bloxworks.project.ProjectCommand.__init__(self, project)
        self.factory = factory

        self._element_type = type
        self._factory_args = args
        self._factory_kwargs = kwargs

    def execute(self):

        self._element = self.factory.make(
        self._element_type,
        *self._factory_args,
        **self._factory_kwargs)

        self.project.world.add_element(self._element)

    def undo(self):
         self.project.world.element.remove_node_by_id(self.element.nid)


class RemoveElementCommand(bloxworks.project.ProjectCommand):

    def __init__(self, project, name = None, nid = None):

        bloxworks.project.ProjectCommand.__init__(self, project)

        if name is None and nid is None:
            raise ValueError, 'name or nid must be given'

        self.element_name = name
        self.element_id = nid

    def execute(self):

        if self.element_id is not None:
            self.project.world.element.remove_node_by_id(self.element_id)

        else:
            self.project.world.element.remove_node_by_name(self.element_name)
