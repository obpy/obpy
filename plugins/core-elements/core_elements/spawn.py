#
# <module description>
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
#
# Copyright (C) 2012 The OpenBlox Project
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
__date__ = "Mar 22, 2012 2:29:00 PM"


import obengine.vfs
import obengine.math
import obengine.element


class SpawnPointElement(obengine.element.Element):

    def __init__(self, name, position = None):

        obengine.element.Element.__init__(self, name)

        if self._position is None:
            self._position = obengine.math.Vector()

        else:
            self._position = position

        try:
            obengine.vfs.listdir('/spawn_points')

        except obengine.vfs.NonExistentMountError:
            obengine.vfs.mount('/spawn_points', obengine.vfs.RegistryFS())

        obengine.vfs.open('/spawn_points/' + str(self.nid), 'w').write(self)
