#
# This module provides a platform-independent way of representing 3D vectors.
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
__date__  = "$Jun 1, 2011 7:39:52 PM$"


import warnings
import obengine.event
import obengine.datatypes

class Vector2D(object):

    def __init__(self, x = 0, y = 0):

        self.on_x_changed = obengine.event.Event()
        self.on_y_changed = obengine.event.Event()

        self._x = float(x)
        self._y = float(y)

    @obengine.datatypes.nested_property
    def x():

        def fget(self):
            return self._x

        def fset(self, value):

            self._x = value
            self.on_x_changed(self._x)

        return locals()

    @obengine.datatypes.nested_property
    def y():

        def fget(self):
            return self._y

        def fset(self, value):

            self._y = value
            self.on_y_changed(self._y)

        return locals()

class Vector(object):
    """
    Simple vector class; things like dot-product
    and vector multiplication currently not implemented.
    """

    def __init__(self, x = 0, y = 0, z = 0):

        self.on_x_changed = obengine.event.Event()
        self.on_y_changed = obengine.event.Event()
        self.on_z_changed = obengine.event.Event()

        self._x = float(x)
        self._y = float(y)
        self._z = float(z)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):

        self._x = float(value)
        self.on_x_changed(self._x)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):

        self._y = float(value)
        self.on_y_changed(self._y)

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):

        self._z = float(value)
        self.on_z_changed(self._z)

    def __getitem__(self, index):
        """
        This is for backwards compatibility with OpenBlox < 0.6.2,
        which used lists instead of this class.
        """

        # Warn our caller this is a deprecated facility
        warnings.warn('Usage of lists for vectors will be removed in OpenBlox 0.8', DeprecationWarning, stacklevel=2)

        # Try to convert the given index to one of our attributes
        keys = {0 : self.x, 1 : self.y, 2 : self.z}

        try:
            return keys[index]

        except KeyError:
            raise IndexError(index)

    def __setitem__(self, index, value):
        """
        This is for backwards compatibility with OpenBlox < 0.6.2,
        which used lists instead of this class.
        """

        # Warn our caller that using lists is deprecated
        warnings.warn('Usage of lists for vectors will be removed in OpenBlox 0.8', DeprecationWarning, stacklevel=2)

        if index == 0:
            self.x = float(value)

        elif index == 1:
            self.y = float(value)

        elif index == 2:
            self.z = float(value)