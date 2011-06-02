# obengine.math.color
# ===================
#
# Provides various RGBA color-related utilites.
#
# Copyright (C) 2011 The OpenBlox Project
# License: GNU GPL v3
#
# See <TODO: No Sphinx docs yet - add some!> for the primary source of documentation
# for this module.

__author__ = "openblocks"
__date__  = "$Jun 1, 2011 7:42:22 PM$"

import warnings
import obengine.event

class Color(object):
    """
    This class manages RGBA colors.
    """

    def __init__(self, r = 0.0, g = 0.0, b = 0.0, a = 255.0):

        self.on_r_changed = obengine.event.Event()
        self.on_g_changed = obengine.event.Event()
        self.on_b_changed = obengine.event.Event()
        self.on_a_changed = obengine.event.Event()

        self._r = float(r)
        self._g = float(g)
        self._b = float(b)
        self._a = float(a)

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, value):

        self._r = float(value)
        self.on_r_changed(self._r)

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, value):

        self._g = float(value)
        self.on_g_changed(self._g)

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):

        self._b = float(value)
        self.on_b_changed(self._b)

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):

        self._a = float(value)
        self.on_a_changed(self._a)

    def __getitem__(self, index):
        """
        This is for backwards compatibility with OpenBlox < 0.6.2,
        which used lists instead of this class.
        """

        warnings.warn('Usage of lists for RGBA colors will be removed in OpenBlox 0.8', DeprecationWarning, stacklevel=2)

        keys = {0 : self.r, 1 : self.g, 2 : self.b, 3 : self.a}

        try:
            return keys[index]

        except KeyError:
            raise IndexError(index)

    def __setitem__(self, index, value):
        """
        This is for backwards compatibility with OpenBlox < 0.6.2,
        which used lists instead of this class.
        """

        warnings.warn('Usage of lists for RGBA colors will be removed in OpenBlox 0.8', DeprecationWarning, stacklevel=2)

        if index == 0:
            self.r = float(value)

        elif index == 1:
            self.g = float(value)

        elif index == 2:
            self.b = float(value)

        elif index == 3:
            self.a = float(value)