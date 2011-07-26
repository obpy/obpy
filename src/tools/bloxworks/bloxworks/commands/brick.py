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
__date__  = "$Jul 25, 2011 7:18:47 PM$"


import bloxworks.commands.element


class AddBrickCommand(bloxworks.commands.element.AddElementCommand):

    def __init__(self, project, factory, name, position = None, color = None, size = None, anchored = False, rotation = None):

        bloxworks.commands.element.AddElementCommand.__init__(self, project, factory)

        self._element_type = 'brick'
        self._factory_kwargs = {
        'name' : name,
        'coords' : position,
        'rgb' : color,
        'size' : size,
        'rotation' : rotation,
        'anchored' : anchored
        }
