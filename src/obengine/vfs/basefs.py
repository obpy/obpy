#
# This module provides the base VFS implementation for OpenBlox.
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


SEPERATOR = '/'


class BaseFS(object):
    """
    Base file system class. Do *not* create an instance of this class!
    """

    def __init__(self):
        raise NotImplementedError

    def open(self, path, mode = 'r'):
        raise NotImplementedError

    def listdir(self, path):
        raise NotImplementedError

    def mkdir(self, path):
        raise NotImplementedError

    def rmdir(self, path):
        raise NotImplementedError

    def remove(self, path):
        raise NotImplementedError

    def getsyspath(self, path):
        raise NotImplementedError

    def exists(self, path):
        raise NotImplementedError


class MountFS(BaseFS):

    def __init__(self):
        self.mount_points = {}

    def mount(self, loc, fs):
        self.mount_points[loc] = fs

    def open(self, path, mode = 'r'):

        path, fs = self._get_best_mount_point(path)
        return fs.open(path, mode)

    def listdir(self, path):

        path, fs = self._get_best_mount_point(path)
        return fs.listdir(path)

    def mkdir(self, path):

        path, fs = self._get_best_mount_point(path)
        return fs.mkdir(path)

    def rmdir(self, path):

        path, fs = self._get_best_mount_point(path)
        return fs.rmdir(path)

    def remove(self, path):

        path, fs = self._get_best_mount_point(path)
        return fs.remove(path)

    def getsyspath(self, path):

        path, fs = self._get_best_mount_point(path)
        return fs.getsyspath(path)

    def exists(self, path):

        try:

            path, fs = self._get_best_mount_point(path)
            return fs.exists(path)

        except FilesystemException:
            return False

    def _get_best_mount_point(self, path):

        points = self.mount_points.keys()
        best_mount_point = ''

        for point in points:

            if path.startswith(point) and len(point) > len(best_mount_point):
                best_mount_point = point

        if best_mount_point:
            return path[len(best_mount_point):], self.mount_points[best_mount_point]

        raise NonExistentMountError(path)


class FilesystemException(Exception): pass
class BadPathException(FilesystemException): pass
class ReadError(FilesystemException): pass
class WriteError(FilesystemException): pass
class NonExistentMountError(FilesystemException): pass
