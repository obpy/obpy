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

__author__="openblocks"
__date__ ="$May 2, 2011 3:50:22 PM$"

from basefs import *
from memoryfs import *
from realfs import *

import obengine.depman
obengine.depman.gendeps()

def init():
    
    global filesystem

    global mount
    global open
    global listdir
    global mkdir
    global rmdir
    global remove
    global getsyspath


    filesystem = MountFS()

    open = filesystem.open
    mount = filesystem.mount
    listdir = filesystem.listdir
    mkdir = filesystem.mkdir
    rmdir = filesystem.rmdir
    remove = filesystem.remove
    getsyspath = filesystem.getsyspath