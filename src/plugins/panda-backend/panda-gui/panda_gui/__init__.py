#
# Base package for the Panda3D/DirectGUI renderer for obengine.gui.
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
__date__  = "$Jun 29, 2011 11:55:13 AM$"


# By default, Panda3D/DirectGUI's 2d rendering coords. are 2.0x2.6, so we'll
# use this tuple scale it to 100x100 (as per the OpenBlox GUI specs)

ASPECT2D_SCALE = (1.0 / 38.46, 1, 1.0 / 50)


def init():

    # The aspect2d "ghost" variable comes from Panda3D's ShowBase class,
    # which sticks the render window's 2D rendering scene node in __builtin__, under
    # the name aspect2d.
    # Note that this necessitates first loading the Panda3D graphics plugin
    # AND an instance of obplugin.panda_graphics.Window be instantiated
    # in order for this plugin to work.

    aspect2d.setScale(*ASPECT2D_SCALE)

from button import *