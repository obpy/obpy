"""
Copyright (C) 2010 The OpenBlox Project

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

import obengine.gfx
import obengine.utils

from pandac.PandaModules import OdeBody, OdeMass, OdeBoxGeom, OdeWorld, OdeSimpleSpace, OdeJointGroup
from pandac.PandaModules import BitMask32, Vec3, Quat

phys_world = None
phys_space = None
phys_cg = None
phys_objs = []

class PhysicalObject(object):

    def __init__(self, model, size = [1, 1, 1], anchored = False):

        self.model = model
        self.size = size

        self.anchored = anchored

        if self.anchored == False:

            self.mass = OdeMass()
            self.geom = OdeBoxGeom(get_phys_space(), self.size[0], self.size[1], self.size[2] * 2) # Don't ask me why 1.99
            self.body = OdeBody(get_phys_world())

            self.geom.setCollideBits(BitMask32(0x0001))
            self.geom.setCategoryBits(BitMask32(0x0001))

            self.mass.setBox(self.size[0] * self.size[1] * self.size[2], self.size[0], self.size[1], self.size[2])

            self.body.setMass(self.mass)
            self.body.setPosition(*self.model.brick.coords)
            q = Quat()
            q.setHpr(Vec3(*self.model.brick.hpr))
            self.body.setQuaternion(q)


            self.geom.setBody(self.body)

            register_phys_obj(self)

        else:

            self.geom = OdeBoxGeom(get_phys_space(), self.size[0], self.size[1], self.size[2] * 2)

            self.geom.setCollideBits(BitMask32(0x0001))
            self.geom.setCategoryBits(BitMask32(0x0001))

            self.geom.setPosition(Vec3(*self.model.brick.coords))

            q = Quat()
            q.setHpr(Vec3(*self.model.brick.hpr))

            self.geom.setQuaternion(q)


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

        self.model.set_pos(*self.body.getPosition())
        self.model.set_hpr(*Quat(self.body.getQuaternion()).getHpr())

def init():

    obengine.utils.info('Initializing physics subsystem...')

    setup_physics()

    obengine.utils.info('Physics subsystem initialized!')

def get_phys_world():
    """
    Returns the physical representation of our sandbox.
    For internal API use only!
    """
    return phys_world

def get_phys_space():
    return phys_space

def get_phys_cg():
    return phys_cg

def update_physics(task):

    global phys_objs

    get_phys_space().autoCollide()

    phys_world.quickStep(1.0 / (obengine.cfg.get_config_var('fps')))

    for obj in phys_objs:

        obj.update()

    get_phys_cg().empty()

    return task.cont

def register_phys_obj(obj):

    global phys_objs

    phys_objs.append(obj)

def setup_physics():

    global phys_world
    global phys_space
    global phys_cg

    # Create the physical representation of our world

    phys_world = OdeWorld()
    phys_world.setGravity(0, 0, -9.81)

    phys_space = OdeSimpleSpace()
    phys_space.setAutoCollideWorld(phys_world)

    phys_cg = OdeJointGroup()

    phys_space.setAutoCollideJointGroup(phys_cg)

    # We use autoCollide for automatic collisions, so we initalize the surface table here
    # See http://www.panda3d.org/manual/index.php/Collision_Detection_with_ODE for more info

    phys_world.initSurfaceTable(1)
    phys_world.setSurfaceEntry(0, 0, 150, 0.0, 9.1, 0.9, 0.00001, 0.0, 0.002)
    
    obengine.gfx.get_rootwin().taskMgr.add(update_physics, 'update_physics')