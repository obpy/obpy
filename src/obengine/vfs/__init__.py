#
# This is the base package for OpenBlox's VFS implementation.
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
__date__ = "$May 2, 2011 3:50:22 PM$"


from basefs import *
from memoryfs import *
from realfs import *
from registryfs import *
from zipfs import *

import obengine.depman
obengine.depman.gendeps()


filesystem = None


def mount(loc, fs):
    get_global_filesystem().mount(loc, fs)


def open(path, mode = 'r'):
    return get_global_filesystem().open(path, mode)


def listdir(path):
    return get_global_filesystem().listdir(path)


def mkdir(path):
    get_global_filesystem().mkdir(path)


def rmdir(path):
    get_global_filesystem().rmdir(path)


def remove(path):
    get_global_filesystem().remove(path)


def getsyspath(path):
    return get_global_filesystem().getsyspath(path)


def exists(path):
    return get_global_filesystem().exists(path)


def join(*components):

    path = SEPERATOR.join(components)

    if path.startswith(SEPERATOR) is False:
        path = SEPERATOR + path

    return path

def init():

    global filesystem
    filesystem = MountFS()


def get_global_filesystem():

    global filesystem
    if filesystem is None:
        raise RuntimeError('VFS access was attempted before initialization took place')

    return filesystem
