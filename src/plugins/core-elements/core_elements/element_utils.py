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
__date__ = "Jan 18, 2012 7:43:45 PM"


class XmlElementExtension(object):

    def _vector_str(self, vector):

        vector_str = str(vector)
        vector_str = vector_str[len('Vector') + 1:len(vector_str) - 1]

        return vector_str

    def _color_str(self, color):

        color_str = str(color)
        color_str = color_str[len('Color') + 1:len(color_str) - 1]

        return color_str

    def _euler_str(self, angle):

        euler_str = str(angle)
        euler_str = euler_str[len('EulerAngle') + 1:len(euler_str) - 1]

        # TODO: There has to be a better solution than this!
        return euler_str or '0.0, 0.0, 0.0'

    def _bool_str(self, bool):

        conv_dict = {True : 'yes', False : 'no'}
        return conv_dict[bool]
