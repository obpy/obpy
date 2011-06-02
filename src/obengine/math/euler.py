# obengine.math.euler
# ===================
#
# Provides various Euler angle-related utilites.
#
# Copyright (C) 2011 The OpenBlox Project
# License: GNU GPL v3
#
# See <TODO: No Sphinx docs yet - add some!> for the primary source of documentation
# for this module.

__author__ = "openblocks"
__date__  = "$Jun 1, 2011 7:41:31 PM$"

import warnings
import obengine.event

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

    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, value):

        self._h = float(value)
        self.on_h_changed(self._h)

    @property
    def p(self):
        return self._p

    @p.setter
    def p(self, value):

        self._p = float(value)
        self.on_p_changed(self._p)

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, value):

        self._r = float(value)
        self.on_r_changed(self._r)

    def __getitem__(self, index):
        """
        This is for backwards compatibility with OpenBlox < 0.6.2,
        which used lists instead of this class.
        """

        warnings.warn('Usage of lists for Euler angles will be removed in OpenBlox 0.8', DeprecationWarning, stacklevel=2)

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

        warnings.warn('Usage of lists for Euler angles will be removed in OpenBlox 0.8', DeprecationWarning, stacklevel=2)

        if index == 0:
            self.h = float(value)

        elif index == 1:
            self.p = float(value)

        elif index == 2:
            self.r = float(value)