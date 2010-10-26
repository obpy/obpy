"""
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
__author__="alexander"
__date__ ="$Sep 9, 2010 4:12:59 PM$"

from obengine.gfx import get_phys_world, get_phys_space, get_phys_cg, register_phys_obj, get_rootwin

from pandac.PandaModules import OdeBody, OdeMass, OdeBoxGeom
from pandac.PandaModules import BitMask32, Vec3, Quat

class PhysicalObject(object):

    def __init__(self, model, size = [1, 1, 1], anchored = False):

        self.model = model
        self.size = size

        self.anchored = anchored

        if self.anchored == False:

            self.mass = OdeMass()
            self.geom = OdeBoxGeom(get_phys_space(), self.size[0], self.size[1], self.size[2] * 1.99) # Don't ask me why 1.99
            self.body = OdeBody(get_phys_world())

            self.geom.setCollideBits(BitMask32(0x0001))
            self.geom.setCategoryBits(BitMask32(0x0001))

            self.mass.setBox(self.size[0] * self.size[1] * self.size[2], self.size[0], self.size[1], self.size[2])

            self.body.setMass(self.mass)
            self.body.setPosition(self.model.getPos(get_rootwin().render))
            self.body.setQuaternion(self.model.getQuat(get_rootwin().render))


            self.geom.setBody(self.body)

            register_phys_obj(self)

        else:

            self.geom = OdeBoxGeom(get_phys_space(), self.size[0], self.size[1], self.size[2] * 1.99)

            self.geom.setCollideBits(BitMask32(0x0001))
            self.geom.setCategoryBits(BitMask32(0x0001))

            self.geom.setPosition(self.model.getPos(get_rootwin().render))
            self.geom.setQuaternion(self.model.getQuat(get_rootwin().render))


    def set_pos(self, x, y, z):

        if self.anchored == False:

            self.body.setPosition(Vec3(x, y, z))

        else:

            self.geom.setPosition(Vec3(x, y, z))

    def set_hpr(self, h, p, r):

        quat = Quat()

        quat.setHpr(Vec3(h, p, r))
        self.body.setQuaternion(quat)


    def update(self):
            
        self.model.setPosQuat(get_rootwin().render, self.body.getPosition(), Quat(self.body.getQuaternion()))