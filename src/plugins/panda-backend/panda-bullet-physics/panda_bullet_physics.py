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
__date__ = "Dec 29, 2011 3:51:21 PM"


import uuid

import panda3d.core
import panda3d.bullet


import obengine.math
import obengine.event
import obengine.datatypes
import obengine.async
from obplugin.panda_utils import PandaConverter


EARTH_GRAVITY = -9.81
DEFAULT_GRAVITY = EARTH_GRAVITY
STEP_SIZE = 1 / 30.0
DEFAULT_FRICTION = 0.7

class World(object):

    def __init__(self, gravity = DEFAULT_GRAVITY):

        self.on_loaded = obengine.event.Event()
        self.on_body_added = obengine.event.Event()
        self.on_paused = obengine.event.Event()
        self.on_unpaused = obengine.event.Event()

        self._gravity = gravity
        self._paused = True

        self.loaded = False

    def load(self):

        self.world_manager = panda3d.bullet.BulletWorld()
        self.world_manager.setGravity(panda3d.core.Vec3(0, 0, self._gravity))
        self.panda_node = render.attachNewNode('Bullet physics world')

        base.taskMgr.add(self._update_physics, 'Bullet simulation task')

        self.loaded = True
        self.on_loaded()

    def add(self, body):

        self.world_manager.attachRigidBody(body.object)
        self.on_body_added(body)

    def remove(self, body):

        self.world_manager.removeRigidBody(body.object)

    def pause(self):

        self._paused = True
        self.on_paused()

    def unpause(self):

        self._paused = False
        self.on_unpaused

    def _update_physics(self, task):

        if self._paused is False:
            self.world_manager.doPhysics(STEP_SIZE)

        return task.cont


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
        self._disabled = True

    def load(self):
        self.scheduler.add(obengine.async.AsyncCall(self._actual_load, 10))

    def enable(self):

        if self._disabled is True:

            self._disabled = False
            self.world.add(self)

    def disable(self):

        if self._disabled is False:

            self._disabled = True
            self.world.remove(self)

    @property
    def loaded(self):
        return self._loaded

    @obengine.datatypes.nested_property
    def rotation():

        def fget(self):
            return PandaConverter.convert_quat(self.panda_node.getQuat())

        def fset(self, new_rotation):
            self.panda_node.setQuat(PandaConverter.convert_angle(new_rotation))

        return locals()

    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return PandaConverter.convert_vec3(self.panda_node.getPos())

        def fset(self, new_position):
            self.panda_node.setPos(PandaConverter.convert_vector(new_position))

    @obengine.datatypes.nested_property
    def anchored():

        def fget(self):
            return self._anchored

        def fset(self, anchored):

            self._anchored = anchored

            if self.anchored is True:
                self.object.setMass(0.0)

            else:
                self.object.setMass(self.weight)

        return locals()

    def _actual_load(self):

        self.object = panda3d.bullet.BulletBoxShape(PandaConverter.convert_vector(self._size))
        self.object.setFriction(DEFAULT_FRICTION)

        if self.anchored is False:
            self.object.setMass(self.weight)

        self.panda_node = self.world.panda_node.attachNewNode(self.object)
        self.panda_node.setPos(PandaConverter.convert_vector(self.model.position))
        self.panda_node.setQuat(PandaConverter.convert_angle(self.model.rotation))

        self._uuid = 'physics-update-%s' % str(uuid.uuid1())

        base.taskMgr.add(self._update_object, self._uuid)

    def _update_object(self, task):

        if self._disabled is False:

            self.model.position = PandaConverter.convert_vec3(self.panda_node.getPos())
            self.model.rotation = PandaConverter.convert_quat(self.panda_node.getQuat())

        return task.cont


class CharacterCapsule(object):

    def __init__(self, world, owner, scheduler):

        self.on_loaded = obengine.event.Event()
        self.on_collision = obengine.event.Event()

        self.world = world
        self.owner = owner
        self.scheduler = scheduler

        self._loaded = False

    def jump(self):
        self.object.doJump()

    def load(self):
        self.scheduler.add(obengine.async.AsyncCall(self._actual_load, 10))

    @property
    def loaded(self):
        return self._loaded

    @obengine.datatypes.nested_property
    def rotation():

        def fget(self):
            return PandaConverter.convert_quat(self.panda_node.getQuat())

        def fset(self, new_rotation):
            self.panda_node.setQuat(PandaConverter.convert_angle(new_rotation))

        return locals()

    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return PandaConverter.convert_vec3(self.panda_node.getPos())

        def fset(self, new_position):
            self.panda_node.setPos(PandaConverter.convert_vector(new_position))

    def _actual_load(self):

        height = 10
        radius = 3
        step_height = 3

        self._uuid = str(uuid.uuid1())

        self._shape = panda3d.bullet.BulletCapsuleShape(height = height, radius = radius, panda3d.bullet.ZUp)
        self.object = panda3d.bullet.BulletCharacterControllerNode(self._shape, step_height, self._uuid)

        self.panda_node = self.world.panda_node.attachNewNode(self.object)
