#
# This plugin provides some Panda3D utilities common to the entire OpenBlox Panda3D
# back-end.
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
__date__ = "$Jul 1, 2011 10:36:46 AM$"


from panda3d.core import Vec3, Vec4, Point2, Point3, Quat, Filename

import obengine.event
import obengine.math
import obengine.vfs


COLOR_SCALER = 255.0
PANDA_TO_OPENBLOX_SCALE = 100.0

class PandaResource(object):
    """
    Base resource class containing various OpenBlox-to-Panda3D conversion utilities.
    It also provides a common, guaranteed interface for all Panda3D resources.
    """

    def __init__(self):
        self.on_loaded = obengine.event.Event()

    def panda_path(self, path):

        if obengine.vfs.SEPERATOR in path:
            return Filename.fromOsSpecific(obengine.vfs.get_global_filesystem().getsyspath(path))

        else:
            return path

    def convert_color(self, color):
        return Vec4(*map(lambda i : i / COLOR_SCALER, [color.r, color.g, color.b, color.a]))

    def convert_vector(self, vector):
        return Vec3(vector.x, vector.y, vector.z)

    def convert_vector2d(self, vector):
        return Point2(vector.x, vector.y)

    def convert_euler_angle(self, angle):
        return [angle.h, angle.p, angle.r]


class PandaConverter(object):

    @staticmethod
    def convert_vector(vector):
        return Vec3(vector.x, vector.y, vector.z)

    @staticmethod
    def convert_vector_to_point3(vector):
        return Point3(vector.x, vector.y, vector.z)

    @staticmethod
    def convert_vector2d(vector):
        return Vec3(vector.x, 0, vector.y)

    @staticmethod
    def convert_angle(angle):

        q = Quat()
        q.setHpr(Vec3(angle.h, angle.p, angle.r))
        return q

    @staticmethod
    def convert_vec3(vector):
        return obengine.math.Vector(vector.getX(), vector.getY(), vector.getZ())

    @staticmethod
    def convert_vec2(vector):
        return obengine.math.Vector2D(vector.getX(), vector.getZ())

    @staticmethod
    def convert_quat(quat):

        hpr = quat.getHpr()
        return obengine.math.EulerAngle(hpr.getX(), hpr.getY(), hpr.getZ())
