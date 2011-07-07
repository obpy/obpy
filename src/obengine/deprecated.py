#
# This module provides a way to easily specify that a function/method is
# deprecated, in a non-instrusive manner (using decorators
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

__author__="openblocks"
__date__ ="$May 22, 2011 6:07:18 AM$"


import warnings
import functools


def deprecated(func):
    """Sets a function as deprecated
    A decorator than issues a DeprecationWarning whenever its decorated function
    is called.
    """

    @functools.wraps(func)
    def warning_wrapper(*args, **kwargs):

        warnings.warn(
        '%s is deprecated' % func.__name__,
        category = DeprecationWarning,
        stacklevel = 2
        )

        return func(*args, **kwargs)

    warning_wrapper.__name__ = func.__name__
    return warning_wrapper