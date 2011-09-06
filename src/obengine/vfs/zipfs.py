#
# <module description>
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
__date__ = "Sep 3, 2011 4:54:04 PM"


import zipfile

import basefs


class ZipFS(basefs.BaseFS):

    def __init__(self, zip_archive):

        self._write_archive = zipfile.ZipFile(zip_archive, 'a')
        self._read_archive = zipfile.ZipFile(zip_archive)

    def open(self, path, mode = 'r'):
        return ZipFile(self, path, mode)


class ZipFile(object):

    def __init__(self, fs, path, mode):

        self._fs = fs
        self._path = path[1:]
        self._mode = mode

        if self._mode == 'r':

            try:
                self._file = self._fs._read_archive.open(self._path, self._mode)

            except IOError:
                raise basefs.BadPathException(self._path)

    def read(self):

        if self._mode != 'r':
            raise basefs.ReadError('File not opened for reading')

        return self._file.read()

    def write(self, data):

        if self._mode != 'w':
            raise RuntimeError('File not opened for writing')

        self._fs._write_archive.writestr(self._path, data)
