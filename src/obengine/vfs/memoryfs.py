#
# This module provides a VFS implementation that exists in memory.
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


__author__ = "openblocks"


import StringIO
import basefs


class MemoryFS(basefs.BaseFS):

    def __init__(self):
        self.fs = {}

    def open(self, path, mode = 'r'):

        # The algorithm we use to open the given path is quite simple:
        # * For each directory in the given path:
        #  * Check to make sure that that directory exists
        #   * If it doesn't (and we're in write mode), create it
        #   * If it doesn't exist (and we're in read mode), raise an error
        #  * Change directories to that directory
        # * Check to make sure the given filename exists inside the current directory!
        # * Return the file, in an appropriate mode

        # cur_node - our "current directory"
        cur_node = self.fs

        # We assume the filename *is* the path (in case the file is located
        # in the root directory
        filename = path

        if path.count(basefs.SEPERATOR) > 0:

            components = path.split(basefs.SEPERATOR)

            filename = components.pop(-1)

            for index, node in enumerate(components):

                # Does the directory we're examining contain this directory?
                if not cur_node.has_key(node):

                    if mode == 'r':
                        raise basefs.ReadError(path)

                    # We're in write mode, so create the directory
                    if cur_node != self.fs:
                        self.mkdir(node, components[index - 1])

                    else:
                        self.mkdir(node)

                # "Change directories" to this directory
                cur_node = cur_node[node]

        # Does the current directory contain our file?
        if cur_node.has_key(filename) is False and mode == 'r':
            raise basefs.ReadError(path)

        elif cur_node.has_key(filename):

            # The sneaky user tried to read/write a directory!
            if isinstance(cur_node[filename], dict):
                raise basefs.BadPathException(path)

        # Create a new, empty file if we're in write mode
        elif mode == 'w':

            cur_node[filename] = self._create_empty_file()
            return cur_node[filename]

        # The default case (occurs when we're in read mode and the given path exists)
        return self._return_file(cur_node[filename])

    def mkdir(self, path):

        components = path.split(basefs.SEPERATOR)
        cur_node = self.fs

        while components:

            directory = components.pop(0)

            if cur_node.has_key(directory):
                continue

            else:
                cur_node[directory] = {}

            cur_node = cur_node[directory]

    def rmdir(self, path):

        try:
            del self.fs[path]

        except KeyError:
            raise basefs.BadPathException(path)

    def listdir(self, path = basefs.SEPERATOR):

        if path == basefs.SEPERATOR:
            return self.fs.keys()

        try:

            cur_node = self.fs

            for directory in path.split(basefs.SEPERATOR):
                cur_node = cur_node[directory]

            return cur_node.keys()

        except KeyError, AttributeError:
            raise basefs.BadPathException(path)

    def exists(self, path):

        try:

            self.open(path)
            return True

        except basefs.FilesystemException:
            return False

    def _create_empty_file(self):
        return StringIO.StringIO('')

    def _return_file(self, loc):
        return StringIO.StringIO(loc.getvalue())
