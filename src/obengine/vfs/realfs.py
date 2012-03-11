#
# This module provides a hard-drive based VFS implementation.
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


import os
import shutil

import basefs


class RealFS(basefs.BaseFS):

    def __init__(self, real_loc):
        self.real_loc = os.path.normpath(real_loc)

    def open(self, path, mode = 'r'):

        self._check_path(path)

        try:
            return open(self._actual_path(path), mode)

        except IOError, message:

            if mode == 'r':
                raise basefs.ReadError(message)

            elif mode == 'w':
                raise basefs.WriteError(message)

    def listdir(self, path = ''):

        self._check_path(path)

        try:
            return os.listdir(self._actual_path(path))

        except OSError, message:
            raise basefs.FilesystemException(message)

    def mkdir(self, path):

        self._check_path(path)

        try:
            os.mkdir(self._actual_path(path))

        except OSError, message:
            raise basefs.FilesystemException(message)

    def rmdir(self, path):

        self._check_path(path)

        try:
            shutil.rmtree(self._actual_path(path))

        except OSError, message:
            raise basefs.FilesystemException(message)

    def remove(self, path):

        self._check_path(path)

        try:
            os.remove(self._actual_path(path))

        except OSError, message:
            raise basefs.FilesystemException(message)

    def getsyspath(self, path):
        return self._actual_path(path)

    def _check_path(self, path):

        if path == '':
            return

        if os.path.normpath(self._actual_path(path)).startswith(self.real_loc) is False:
            raise basefs.BadPathException('%s is outside of root directory %s' % (path, self.real_loc))

    def _actual_path(self, path):
        return os.sep.join([self.real_loc, path.replace(basefs.SEPERATOR, os.sep)])
