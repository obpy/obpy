#
# This is the base OpenBlox package. All core OpenBlox code (save for BloxWorks)
# is located under this package.
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
#
#
# Copyright (C) 2010-2011 The OpenBlox Project
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
__date__  = "$Jul 12, 2010 7:59:47 PM$"


ENGINE_VERSION = (0, 7, 0)


def version_string():
    """Returns a human-readable version of OpenBlox
    This function returns a human-readable, period-seperated string
    representing OpenBlox's current version.
    """
    return '.'.join(map(str, ENGINE_VERSION))


def compatible_with(version_str):

    if len(version_str) < 1:
        raise InvalidVersionError(version_str)
    
    return map(int, version_str.split('.'))[0] == ENGINE_VERSION[0]


def init():
    """Wrapper around obengine.depman.init()
    Call this function, after importing all the modules you need.
    """

    import obengine.depman
    obengine.depman.init()


class InvalidVersionError(Exception):
    """Raised when an invalid version string is passed to obengine.compatible_with."""