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
__date__ = "Aug 1, 2011 9:22:46 PM"


import os

import obengine.vfs
import obengine.depman

obengine.depman.gendeps()


def init():

    data_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'data')
    obengine.vfs.mount('/bloxworks-data', obengine.vfs.RealFS(data_dir))

    obengine.vfs.mount('/bloxworks-registry', obengine.vfs.RegistryFS())
