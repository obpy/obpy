"""
Copyright (C) 2011 The OpenBlox Project

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

"""

import os
import shutil

import basefs

class RealFS(basefs.BaseFS):

    def __init__(self, real_loc):
        self.real_loc = real_loc

    def open(self, path, mode='r'):
        return open(self._actual_path(path), mode)

    def listdir(self, path=''):
        return os.listdir(self._actual_path(path))

    def mkdir(self, path):
        os.mkdir(self._actual_path(path))

    def rmdir(self, path):
        shutil.rmtree(self._actual_path(path))

    def remove(self, path):
        os.remove(self._actual_path(path))

    def getsyspath(self, path):
        return self._actual_path(path)

    def _actual_path(self, path):
        return os.sep.join([self.real_loc, path.replace(basefs.SEPERATOR, os.sep)[1:]])
