#
# This plugin provides a Panda3D/ODE/copperode-based physics backend.
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
__date__  = "$May 2, 2011 12:30:08 PM$"


from panda3d.core import Vec3, Quat
from copperode import odeWorldManager
from copperode import staticObject, dynamicObject

import obengine.event
import obengine.async
import obengine.gfx.math
import obengine.log
import obengine.depman

obengine.depman.gendeps()


class PandaConverter(object):

    @staticmethod
    def convert_vector(vector):
        return Vec3(vector.x, vector.y, vector.z)

    @staticmethod
    def convert_angle(angle):

        q = Quat()
        q.setHpr(Vec3(angle.h, angle.p, angle.r))
        return q

    @staticmethod
    def convert_vec3(vector):
        return obengine.gfx.math.Vector(vector.getX(), vector.getY(), vector.getZ())

    @staticmethod
    def convert_quat(quat):

        vec = Vec3(quat)
        return PandaConverter.convert_vec3(vec)


class World(object):
    
    def __init__(self):

        self.on_loaded = obengine.event.Event()
        self.on_body_added = obengine.event.Event()
        self.on_paused = obengine.event.Event()
        self.on_unpaused = obengine.event.Event()

        self.loaded = False

    def load(self):

        # It is the perversity of Panda3D's __builtin__ assignments that means
        # a Panda3D window must be created before this method can be called
        
        self.world_manager = odeWorldManager()
        self.world_manager.stepSize = 1 / 60.0

        self.loaded = True
        self.on_loaded()

    def add(self, obj):

        self.world_manager.addObject(obj.object)
        self.on_body_added(obj)

    def pause(self):

        self.world_manager.pause()
        self.on_paused()

    def unpause(self):

        self.world_manager.unpause()
        self.on_unpaused()


class Box(object):

    def __init__(self, model, world, owner, scheduler, anchored = False, weight = None):

        self.model = model
        self.on_loaded = obengine.event.Event()
        self.on_collision = obengine.event.Event()
        self.scheduler = scheduler

        self.world = world
        self.owner = owner
        self.anchored = anchored
        self.weight = weight or ((self.model.scale.x or 1.0) * (self.model.scale.y or 1.0) * (self.model.scale.z or 1.0))

        self._loaded = False

    def load(self):
        self.scheduler.add(obengine.async.AsyncCall(self._actual_load, 10))

    def _actual_load(self):

        if self.anchored is False:

            self.object = dynamicObject(self.world.world_manager)
            self._init_dynamic_object()

        else:

            self.object = staticObject(self.world.world_manager)
            self._init_static_object()

        self._general_init()

        self._loaded = True
        
        self.world.add(self)
        self.on_loaded()

    def update_size(self):

        if self.anchored is False:
            self._init_dynamic_object()

        elif self.anchored is True:
            self._init_static_object()

    def enable(self):
        self.object.enable()

    def disable(self):
        self.object.disable()

    def destroy(self):
        self.object.destroy()

    @property
    def rotation(self):
        return PandaConverter.convert_quat(self.object.getQuat())

    @rotation.setter
    def rotation(self, new_rot):
        self.object.setQuat(PandaConverter.convert_angle(new_rot))

    @property
    def position(self):
        return PandaConverter.convert_vec3(self.object.getPos())

    @position.setter
    def position(self, new_pos):
        self.object.setPos(PandaConverter.convert_vec3(new_pos))

    @property
    def loaded(self):
        return self._loaded

    def _general_init(self):

        self.object.setCatColBits('general')
        self.object.collisionCallback = self._translate_collision_cb
        self.object.owner = self.owner

    def _init_dynamic_object(self):

        self.object.setBoxGeomFromNodePath(self.model.panda_node, remove = False)
        self.object.setNodePath(self.model.panda_node)
        self.object.setBoxBody(self.weight, self.object.boxSize)
        self.object.setPos(PandaConverter.convert_vector(self.model.position))
        self.object.setQuat(PandaConverter.convert_angle(self.model.rotation))

    def _init_static_object(self):

        self.object.setNodePath(self.model.panda_node)

        self.object.setBoxGeomFromNodePath(self.model.panda_node)
        self.object.setPos(PandaConverter.convert_vector(self.model.position))
        self.object.setQuat(PandaConverter.convert_angle(self.model.rotation))

    def _translate_collision_cb(self, entry, object1, object2):

        try:
            first_subject = object1.owner

        except AttributeError:
            first_subject = object1

        try:
            second_subject = object2.owner

        except AttributeError:
            second_subject = object2

        self.on_collision(first_subject, second_subject)
