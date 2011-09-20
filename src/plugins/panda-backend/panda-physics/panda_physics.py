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
__date__ = "$May 2, 2011 12:30:08 PM$"


from copperode import odeWorldManager
from copperode import staticObject, dynamicObjectNoCCD, kinematicCharacterController

import obengine.event
import obengine.datatypes
import obengine.async
import obengine.plugin
import obengine.gfx.math
import obengine.log
from obplugin.panda_utils import PandaConverter


class World(object):

    def __init__(self, gravity = -9.81):

        self.on_loaded = obengine.event.Event()
        self.on_body_added = obengine.event.Event()
        self.on_paused = obengine.event.Event()
        self.on_unpaused = obengine.event.Event()

        self._gravity = gravity

        self.loaded = False

    def load(self):

        # It is the perversity of Panda3D's __builtin__ assignments that means
        # a Panda3D window must be created before this method can be called

        self.world_manager = odeWorldManager(self._gravity)
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

    def __init__(self, model, world, owner, scheduler, anchored = False, weight = None, size = None):

        self.model = model
        self.on_loaded = obengine.event.Event()
        self.on_collision = obengine.event.Event()
        self.scheduler = scheduler

        self.world = world
        self._anchored = anchored
        self._size = size
        self.weight = weight or (
                                 (self.model.scale.x * 5 or 1.0) * \
                                 (self.model.scale.y * 5 or 1.0) * \
                                 (self.model.scale.z * 5 or 1.0))

        self._loaded = False

    def load(self):
        self.scheduler.add(obengine.async.AsyncCall(self._actual_load, 10))

    def _actual_load(self):

        if self._anchored is False:

            self.object = dynamicObjectNoCCD(self.world.world_manager)
            self._init_dynamic_object()

        else:

            self.object = staticObject(self.world.world_manager)
            self._init_static_object()

        self._general_init()

        self._loaded = True

        self.world.add(self)
        self.on_loaded()

    def update_size(self):

        self.destroy()

        if self._anchored is False:

            self.object = dynamicObjectNoCCD(self.world.world_manager)
            self._init_dynamic_object()

        elif self._anchored is True:

            self.object = staticObject(self.world.world_manager)
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
        self.object.setPos(PandaConverter.convert_vector(new_pos))

    @property
    def loaded(self):
        return self._loaded

    @obengine.datatypes.nested_property
    def anchored():

        def fget(self):
            return self._anchored

        def fset(self, anchored):

            self._anchored = anchored
            self.destroy()

            if self._anchored is False:

                self.object = dynamicObjectNoCCD(self.world.world_manager)
                self._init_dynamic_object()

            else:

                self.object = staticObject(self.world.world_manager)
                self._init_static_object()

        return locals()

    @obengine.datatypes.nested_property
    def owner():

        def fget(self):
            return self.object.owner

        def fset(self, new_owner):
            self.object.owner = new_owner

        return locals()

    def _general_init(self):

        self.object.collisionCallback = self._translate_collision_cb
        # self.world.world_manager.addObject(self.object)

    def _init_dynamic_object(self):

        if self._size is not None:
            self.object.setBoxGeom(PandaConverter.convert_vector(self._size))
        else:
            self.object.setBoxGeomFromNodePath(self.model.panda_node, remove = False)

        self.object.setNodePath(self.model.panda_node)
        self.object.setBoxBody(self.weight, self.object.boxSize)
        self.object.setPos(PandaConverter.convert_vector(self.model.position))
        self.object.setQuat(PandaConverter.convert_angle(self.model.rotation))

    def _init_static_object(self):

        self.object.setNodePath(self.model.panda_node)

        if self._size is not None:
            self.object.setBoxGeom(PandaConverter.convert_vector(self._size))
        else:
            self.object.setBoxGeomFromNodePath(self.model.panda_node, remove = False)

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

        self.on_collision(second_subject)


class CharacterCapsule(object):

    def __init__(self, world, owner, scheduler):

        self.on_loaded = obengine.event.Event()
        self.on_collision = obengine.event.Event()

        self.world = world
        self.owner = owner
        self.scheduler = scheduler

        self._loaded = False

    def jump(self):
        self.object.jump()

    def load(self):
        self.scheduler.add(obengine.async.AsyncCall(self._actual_load, 10))

    @property
    def loaded(self):
        return self._loaded

    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return PandaConverter.convert_vec3(self.object.getPos())

        def fset(self, new_pos):
            self.object.setPos(PandaConverter.convert_vector(new_pos))

        return locals()

    @obengine.datatypes.nested_property
    def rotation():

        def fget(self):
            return PandaConverter.convert_quat(self.object.getQuat())

        def fset(self, new_rot):
            self.object.setQuat(PandaConverter.convert_angle(new_rot))

        return locals()

    @obengine.datatypes.nested_property
    def linear_velocity():

        def fget(self):
            return PandaConverter.convert_vec3(self.object.linearVelocity)

        def fset(self, vel):
            self.object.linearVelocity = PandaConverter.convert_vector(vel)

        return locals()

    @obengine.datatypes.nested_property
    def rotational_velocity():

        def fget(self):
            return self._rotational_velocity

        def fset(self, vel):
            self._rotational_velocity = vel

        return locals()

    def _actual_load(self):

        self.object = kinematicCharacterController(self.world.world_manager, (5, 4))

        self.scheduler.add(
        obengine.async.Task(self._update_rotational_vel, priority = 5))
        self._rotational_velocity = obengine.math.EulerAngle()

        self._loaded = True
        self.on_loaded()

    def _update_rotational_vel(self, task):

        rotation = self.rotation
        rot_velocity = self.rotational_velocity

        rotation.h += rot_velocity.h
        #rotation.h = rotation.h % 360
        rotation.p += rot_velocity.p
        #rotation.p = rotation.p % 360
        rotation.r += rot_velocity.r
        #rotation.r = rotation.r % 360

        self.rotation = rotation

        return task.AGAIN
