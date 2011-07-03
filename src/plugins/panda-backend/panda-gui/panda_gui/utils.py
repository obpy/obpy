# To change this template, choose Tools | Templates
# and open the template in the editor.
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
__date__  = "$Jul 1, 2011 1:03:59 PM$"


import obengine.math
import obplugin.panda_utils


def panda_to_openblox_pos(position):
    # This method is currently broken!

    coords = map(lambda c: c * 100.0, position)
    return obengine.math.Vector2D(*coords)


def openblox_to_panda_pos(position):

    vector = obengine.math.Vector2D(position.x, position.y)
    vector.x /= 100.0
    vector.y /= 100.0
    return obplugin.panda_utils.PandaConverter.convert_vector2d(vector)