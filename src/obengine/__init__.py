"""
Copyright (C) 2010 The OpenBlox Project

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


This is the base OpenBlox Python package. Look at this package's subpackages for the actual code/documentation.
"""

__author__="openblocks"
__date__ ="$Jul 12, 2010 7:59:47 PM$"

ENGINE_VERSION = (0, 7, 0)

def init():
    """
    Wrapper around obengine.depman.init().
    Call this function, after importing all the modules you need.
    """

    import depman

    depman.gendeps()
    depman.init()