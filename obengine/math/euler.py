#
# This module provides a platform-independent way of representing Euler angles.
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
__date__ = "$Jun 1, 2011 7:41:31 PM$"


import warnings
import obengine.event
import obengine.datatypes


class EulerAngle(object):
    """
    Minimalistic Euler angle class.
    See http://en.wikipedia/Euler_Angle for more on Euler angles.
    """

    def __init__(self, h = 0, p = 0, r = 0):

        self.on_h_changed = obengine.event.Event()
        self.on_p_changed = obengine.event.Event()
        self.on_r_changed = obengine.event.Event()

        self._h = float(h)
        self._p = float(p)
        self._r = float(r)

    @obengine.datatypes.nested_property
    def h():

    	def fget(self):
    	    return self._h

    	def fset(self, value):
    	    self._h = float(value)
    	    self.on_h_changed(self._h)

        return locals()

    @obengine.datatypes.nested_property
    def p():

        def fget(self):
            return self._p

        def fset(self, value):
            self._p = float(value)
            self.on_p_changed(self._p)

        return locals()

    @obengine.datatypes.nested_property
    def r():

        def fget(self):
            return self._r

        def fset(self, value):
            self._r = float(value)
            self.on_r_changed(self._r)

        return locals()

    def __getitem__(self, index):
        """
        This is for backwards compatibility with OpenBlox < 0.6.2,
        which used lists instead of this class.
        """

        warnings.warn('Usage of lists for Euler angles will be removed in OpenBlox 0.8', DeprecationWarning, stacklevel = 2)

        keys = {0 : self.h, 1 : self.p, 2 : self.r}

        try:
            return keys[index]

        except KeyError:
            raise IndexError(index)

    def __setitem__(self, index, value):
        """
        This is for backwards compatibility with OpenBlox < 0.6.2,
        which used lists instead of this class.
        """

        warnings.warn('Usage of lists for Euler angles will be removed in OpenBlox 0.8', DeprecationWarning, stacklevel = 2)

        if index == 0:
            self.h = float(value)

        elif index == 1:
            self.p = float(value)

        elif index == 2:
            self.r = float(value)

    def __repr__(self):

        return '%s(%s, %s, %s)' % (
        self.__class__.__name__,
        self.h,
        self.p,
        self.r,
        )
