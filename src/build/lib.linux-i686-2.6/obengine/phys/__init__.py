__author__="alexander"
__date__ ="$Sep 9, 2010 4:12:59 PM$"

from obengine.gfx import get_phys_world, get_phys_space, get_phys_cg, register_phys_obj, get_rootwin

from pandac.PandaModules import OdeBody, OdeMass, OdeBoxGeom
from pandac.PandaModules import BitMask32, Vec4, Quat

class PhysicalObject(object):

    def __init__(self, model, size = [1, 1, 1], anchored = False):

        self.model = model
        self.size = size

        self.anchored = anchored

        print size

        if self.anchored == False:

            self.mass = OdeMass()
            self.geom = OdeBoxGeom(get_phys_space(), self.size[0], self.size[1], self.size[2] * 1.99) # Don't ask me why 1.99
            self.body = OdeBody(get_phys_world())

            self.geom.setCollideBits(BitMask32(0x0001))
            self.geom.setCategoryBits(BitMask32(0x0001))

            self.mass.setBox(25, self.size[0], self.size[1], self.size[2])

            self.body.setMass(self.mass)
            self.body.setPosition(self.model.getPos(get_rootwin().render))
            self.body.setQuaternion(self.model.getQuat(get_rootwin().render))


            self.geom.setBody(self.body)

            register_phys_obj(self)

        else:

            self.geom = OdeBoxGeom(get_phys_space(), self.size[0], self.size[1], self.size[2] * 2)

            self.geom.setCollideBits(BitMask32(0x0001))
            self.geom.setCategoryBits(BitMask32(0x0001))

            self.geom.setPosition(self.model.getPos(get_rootwin().render))
            self.geom.setQuaternion(self.model.getQuat(get_rootwin().render))



    def update(self):
            
        self.model.setPosQuat(get_rootwin().render, self.body.getPosition(), Quat(self.body.getQuaternion()))