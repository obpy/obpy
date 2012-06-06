#
# This module provides a command DP-based way to make bricks from BloxWorks.
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
__date__ = "$Jul 25, 2011 7:18:47 PM$"


import functools
import copy

import obengine.math
import obengine.vfs

import bloxworks.commands.element


class AddBrickCommand(bloxworks.commands.element.AddElementCommand):

    CAM_MARGIN = 30.0

    def __init__(self, project, factory, name, position = None, color = None, size = None, anchored = False, rotation = None):

        bloxworks.commands.element.AddElementCommand.__init__(self, project, factory)

        self._element_type = 'brick'
        self._factory_args = [
        name,
        position,
        color,
        size,
        rotation,
        anchored
        ]

    def execute(self):

        bloxworks.commands.element.AddElementCommand.execute(self)

        move_tool = obengine.vfs.open('/bloxworks-registry/move-tool').read()
        self.element.on_click += functools.partial(move_tool.move, self.element)

        resize_tool = obengine.vfs.open('/bloxworks-registry/resize-tool').read()
        self.element.on_click += functools.partial(resize_tool.resize, self.element)

        world = obengine.vfs.open('/bloxworks-registry/project').read().world

        try:
            last_selected_brick_pos = obengine.vfs.open('/bloxworks-registry/property-editor').read()._brick.position
            self.element.position = obengine.math.Vector(
                                                         last_selected_brick_pos.x,
                                                         last_selected_brick_pos.y,
                                                         last_selected_brick_pos.z - self.element.size.z / 2)
        except AttributeError:
            pass


        for node in world.element.nodes.itervalues():

            try:
                node.position
                node.size

            except AttributeError:
                continue

            if node.position.z + node.size.z / 2 >= self.element.position.z + self.element.size.z / 2:
                if node.position.x + node.size.x / 2 >= self.element.position.x + self.element.size.x / 2:
                    if node.position.y + node.size.y / 2 >= self.element.position.y + self.element.size.y / 2:

                        new_pos = self.element.position
                        new_pos.z = node.position.z + node.size.z / 2 + self.element.size.z / 2
                        self.element.position = new_pos

        try:
            property_editor = obengine.vfs.open('/bloxworks-registry/property-editor').read()
            self.element.on_click += lambda: property_editor.populate(self.element)
            property_editor.populate(self.element)

        except obengine.vfs.ReadError:
            print 'warning: couldn\'t find property editor'

        camera = obengine.vfs.open('/bloxworks-registry/project').read().world.element.get_node_by_name('camera')
        cam_pos = obengine.math.Vector(
                                       self.element.position.x,
                                       self.element.position.y,
                                       self.element.position.z)
        cam_pos.x += self.element.size.x / 2.0 + self.CAM_MARGIN
        cam_pos.y += self.element.size.y / 2.0 + self.CAM_MARGIN
        cam_pos.z += self.element.size.z / 2.0 + self.CAM_MARGIN
        camera.position = cam_pos
        camera.look_at(self.element)
