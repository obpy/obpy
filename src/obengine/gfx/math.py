"""
This file is part of The OpenBlox Game Engine.

    The OpenBlox Game Engine is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    The OpenBlox Game Engine is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with The OpenBlox Game Engine.  If not, see <http://www.gnu.org/licenses/>.

"""
__author__="openblocks"
__date__ ="$Mar 3, 2011 3:30:17 PM$"

import warnings

class Vector(object):

    def __init__(self, x = 0, y = 0, z = 0):
        
        self.x = x
        self.y = y
        self.z = z

    def __getitem__(self, index):

        warnings.warn('Usage of lists for vectors will be removed in OpenBlox 0.8', DeprecationWarning)

        keys = {0 : self.x, 1 : self.y, 2 : self.z}

        try:
            return keys[index]

        except KeyError:
            raise IndexError(index)

    def __setitem__(self, index, value):

        warnings.warn('Usage of lists for vectors will be removed in OpenBlox 0.8', DeprecationWarning)

        if index == 0:
            self.x = value

        elif index == 1:
            self.y = value
            
        elif index == 2:
            self.z = value



class EulerAngle(object):

    def __init__(self, h = 0, p = 0, r = 0):

        self.h = h
        self.p = p
        self.r = r

    def __getitem__(self, index):

        warnings.warn('Usage of lists for Euler angles will be removed in OpenBlox 0.8', DeprecationWarning)

        keys = {0 : self.h, 1 : self.p, 2 : self.r}

        try:
            return keys[index]

        except KeyError:
            raise IndexError(index)

    def __setitem__(self, index, value):

        warnings.warn('Usage of lists for Euler angles will be removed in OpenBlox 0.8', DeprecationWarning)

        if index == 0:
            self.h = value

        elif index == 1:
            self.p = value

        elif index == 2:
            self.r = value

class Color(object):

    def __init__(self, r = 0, g = 0, b = 0, a = 255):

        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __getitem__(self, index):

        warnings.warn('Usage of lists for RGBA colors will be removed in OpenBlox 0.8', DeprecationWarning)

        keys = {0 : self.r, 1 : self.g, 2 : self.b, 3 : self.a}

        try:
            return keys[index]

        except KeyError:
            raise IndexError(index)

    def __setitem__(self, index, value):

        warnings.warn('Usage of lists for RGBA colors will be removed in OpenBlox 0.8', DeprecationWarning)

        if index == 0:
            self.r = value

        elif index == 1:
            self.g = value

        elif index == 2:
            self.b = value

        elif index == 3:
            self.a = value