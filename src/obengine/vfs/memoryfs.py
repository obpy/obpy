#
# This module provides a VFS implementation that exists in memory.
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

    def open(self, path, mode='r'):

        cur_node = self.fs
        filename = path
      
        if path.count(basefs.SEPERATOR) > 0:

            components = path.split(basefs.SEPERATOR)
            filename = components.pop(-1)
            
            for index, node in enumerate(components):
                if not cur_node.has_key(node):

                    if mode == 'r':
                        raise IOError(path)

                    if cur_node != self.fs:
                        self._mkdir(node, components[index - 1])

                    else:
                        self._mkdir(node)

                cur_node = cur_node[node]

        if not cur_node.has_key(filename) and mode == 'r':
            raise IOError(path)

        elif mode == 'w':

            cur_node[filename] = self._create_empty_file()
            return cur_node[filename]

        elif cur_node.has_key(filename):

            if isinstance(cur_node[filename], dict):
                raise IOError(path)

        return self._return_file(cur_node[filename])

    def _create_empty_file(self):
        return StringIO.StringIO('')

    def _return_file(self, loc):
        return StringIO.StringIO(loc.getvalue())
      
    def mkdir(self, path):
        
        if path.count(basefs.SEPERATOR) > 0:

            components = path.split(basefs.SEPERATOR)

            for index, directory in enumerate(components):

                if index == 0:
                    self._mkdir(directory)

                else:
                    self._mkdir(directory, components[index - 1])

        else:
            self._mkdir(path)

    def rmdir(self, path):
        
        try:
            del self.fs[path]

        except:
            raise IOError(path)

    def listdir(self, path):

        if path == '':
            return self.fs.keys()
         
        try:
            return self.fs[path].keys()

        except:
            raise IOError(path)

    def _mkdir(self, path, parent=None):
   
        if parent == None:

            if self.fs.has_key(path):
                return
         
            self.fs[path] = {}

        else:

            if self.fs.has_key(parent) and self.fs[parent].has_key(path):
                return
            
            self.fs[parent][path] = {}
