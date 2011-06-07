#
# This module provides a simple VFS-integrated registry.
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
__date__  = "$May 28, 2011 11:30:47 PM$"


import memoryfs
import obengine.depman

obengine.depman.gendeps()


class RegistryFS(memoryfs.MemoryFS):
    """
    A simple implementation of a registry, integrated with OpenBlox's VFS.

    Example:

        >>> from obengine.vfs import *
        >>> fs = RegistryFS()
        >>> test_list = [1, 2, 3, 4, 5]
        >>> registry_file = fs.open('test_list', 'w')
        >>> registry_file.write(test_list)
        >>> print fs.open('test_list').read()
        [1, 2, 3, 4, 5]
    """

    def _create_empty_file(self):
        return RegistryFile()

    def _return_file(self, loc):
        return loc


class RegistryFile(object):

    def __init__(self):
        self._data = None
        
    def read(self):
        return self._data

    def write(self, data):
        self._data = data

    def close(self):
        pass
