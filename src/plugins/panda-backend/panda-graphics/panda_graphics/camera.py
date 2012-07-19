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
__date__ = "Jul 19, 2012 6:03:00 PM"


import obengine.math
import obengine.event
import obengine.datatypes
import obplugin.panda_utils


class Camera(object):

    def __init__(self, window):

        self.on_loaded = obengine.event.Event()

        self.window = window
        self.camera = self.window.panda_window.camera
        self.panda_node = self.camera
        self._parent = None

    def load(self):
        self.on_loaded()

    def look_at(self, model):
        self.camera.lookAt(model.panda_node)

    def look_at_point(self, point):
        self.camera.lookAt(obplugin.panda_utils.PandaConverter.convert_vector_to_point3(point))

    def move(self, vector):
        self.camera.setPos(self.camera, vector.x, vector.y, vector.z)

    @property
    def position(self):

        cam_vec = self.camera.getPos()
        return obengine.math.Vector(cam_vec.getX(), cam_vec.getY(), cam_vec.getZ())

    @position.setter
    def position(self, pos):

        if isinstance(pos, tuple):
            pos = obengine.math.Vector(*pos)

        self.camera.setPos(pos.x, pos.y, pos.z)

    @obengine.datatypes.nested_property
    def rotation():

        def fget(self):
            return obplugin.panda_utils.PandaConverter.convert_quat(self.camera.getQuat())

        def fset(self, new_angle):

            quat = obplugin.panda_utils.PandaConverter.convert_angle(new_angle)
            self.camera.setQuat(quat)

        return locals()

    @obengine.datatypes.nested_property
    def parent():

        def fget(self):
            return self._parent

        def fset(self, new_parent):

            self._parent = new_parent
            self.camera.reparentTo(self.parent.panda_node)

        return locals()
