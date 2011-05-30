# <obengine.vfs.registryfs>
# ===================
#
# Basic VFS-based implementation of a registry.
#
# Copyright (C) 2011 The OpenBlox Project
# License: GNU GPL v3
#
# See <TODO: No Sphinx docs yet - add some!> for the primary source of documentation
# for this module.

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