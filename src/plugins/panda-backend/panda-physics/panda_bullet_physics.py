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
import obplugin.panda_utils


EARTH_GRAVITY = -9.81
DEFAULT_GRAVITY = EARTH_GRAVITY * 7.0
MAX_STEP_SIZE = 1 / 60.0
MAX_SUBSTEPS = 10
DEFAULT_FRICTION = 0.7

class World(object):

    def __init__(self, gravity = DEFAULT_GRAVITY):

        self.on_loaded = obengine.event.Event()
        self.on_body_added = obengine.event.Event()
        self.on_paused = obengine.event.Event()
        self.on_unpaused = obengine.event.Event()

        self._bodies = set()

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
        self._bodies.add(body)
        self.on_body_added(body)

    def remove(self, body):

        self.world_manager.removeRigidBody(body.object)
        self._bodies.remove(body)

    def pause(self):

        self._paused = True
        self.on_paused()

    def unpause(self):

        self._paused = False
        self.on_unpaused

    @property
    def gravity(self):
        return self._gravity

    def _update_physics(self, task):

        if self._paused is False:

            dt = globalClock.getDt()
            self.world_manager.doPhysics(dt, MAX_SUBSTEPS, MAX_STEP_SIZE)

            for body in self._bodies:
                body.update()

        return task.cont


class Box(object):

    def __init__(self, model, world, owner, scheduler, anchored = False, weight = None, size = None):

        self.model = model
        self.on_loaded = obengine.event.Event()
        self.on_collision = obengine.event.Event()
        self.scheduler = scheduler
        self.owner = owner

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

    @property
    def enabled(self):
        return self._disabled is False

    @obengine.datatypes.nested_property
    def rotation():

        def fget(self):
            return obplugin.panda_utils.PandaConverter.convert_quat(self.panda_node.getQuat())

        def fset(self, new_rotation):
            self.panda_node.setQuat(obplugin.panda_utils.PandaConverter.convert_angle(new_rotation))

        return locals()

    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return obplugin.panda_utils.PandaConverter.convert_vec3(self.panda_node.getPos())

        def fset(self, new_position):
            self.panda_node.setPos(obplugin.panda_utils.PandaConverter.convert_vector(new_position))

        return locals()

    @obengine.datatypes.nested_property
    def size():

        def fget(self):
            return self._size

        def fset(self, new_size):

            was_disabled = self.enabled is False

            self.disable()
            self.panda_node.detachNode()
            del self.object

            self._size = new_size

            self._make_object()

            if was_disabled is False:
                self.enable()

        return locals()

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

        self._uuid = 'physics-update-%s' % str(uuid.uuid1())
        self._make_object()

        self._disabled = False
        self._loaded = True

    def _make_object(self):

        if self._size is None:
            self._size = self.model.bounds

        self._size.x /= 2
        self._size.y /= 2

        self._shape = panda3d.bullet.BulletBoxShape(obplugin.panda_utils.PandaConverter.convert_vector(self._size))
        self.object = panda3d.bullet.BulletRigidBodyNode(self._uuid)
        if self.anchored is False:
            self.object.setMass(self.weight)
        self.object.addShape(self._shape)
        self.object.setFriction(DEFAULT_FRICTION)

        self.panda_node = self.world.panda_node.attachNewNode(self.object)
        self.panda_node.setPythonTag('owner', self)
        self.panda_node.setPos(obplugin.panda_utils.PandaConverter.convert_vector(self.model.position))
        self.panda_node.setQuat(obplugin.panda_utils.PandaConverter.convert_angle(self.model.rotation))
        self.panda_node.setCollideMask(panda3d.core.BitMask32.allOn())

        self.world.add(self)

    def update(self):

        if self._disabled is False:

            self.model.position = obplugin.panda_utils.PandaConverter.convert_vec3(self.panda_node.getPos())
            self.model.rotation = obplugin.panda_utils.PandaConverter.convert_quat(self.panda_node.getQuat())

            contacting_models = self.world.world_manager.contactTest(self.object)

            for contact in contacting_models.getContacts():

                contact_owner = contact.getNode0().getPythonTag('owner').owner
                self.on_collision(contact_owner)


class CharacterCapsule(object):

    def __init__(self, world, owner, scheduler, height = 4.0, radius = 1.0, step_height = 3.0, jump_velocity = 25.0):

        self.on_loaded = obengine.event.Event()
        self.on_collision = obengine.event.Event()

        self.world = world
        self.owner = owner
        self.scheduler = scheduler

        self._loaded = False

        self._height = height
        self._radius = radius
        self._step_height = step_height
        self._jump_velocity = jump_velocity

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
            return obplugin.panda_utils.PandaConverter.convert_quat(self.panda_node.getQuat())

        def fset(self, new_rotation):
            self.panda_node.setQuat(obplugin.panda_utils.PandaConverter.convert_angle(new_rotation))

        return locals()

    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return obplugin.panda_utils.PandaConverter.convert_vec3(self.panda_node.getPos())

        def fset(self, new_position):
            self.panda_node.setPos(obplugin.panda_utils.PandaConverter.convert_vector(new_position))

        return locals()

    @obengine.datatypes.nested_property
    def linear_velocity():

        def fget(self):
            return self._linear_velocity

        def fset(self, new_linear_velocity):

            self._linear_velocity = new_linear_velocity
            self.object.setLinearMovement(obplugin.panda_utils.PandaConverter.convert_vector(new_linear_velocity), True)

        return locals()

    @obengine.datatypes.nested_property
    def rotational_velocity():

        def fget(self):
            return self._rotational_velocity

        def fset(self, new_rotational_velocity):

            self._rotational_velocity = new_rotational_velocity
            self.object.setAngularMovement(self._rotational_velocity.h)

        return locals()

    def _actual_load(self):

        self._uuid = str(uuid.uuid1())

        self._shape = panda3d.bullet.BulletCapsuleShape(self._height, self._radius, panda3d.bullet.ZUp)
        self.object = panda3d.bullet.BulletCharacterControllerNode(self._shape, self._step_height, self._uuid)
        self.object.setGravity(-self.world.gravity)
        self.object.setJumpSpeed(self._jump_velocity)

        self.world.world_manager.attachCharacter(self.object)

        self.panda_node = self.world.panda_node.attachNewNode(self.object)
        position_offset = obengine.math.Vector(self.owner.position.x,
                                               self.owner.position.y,
                                               self.owner.position.z)
        position_offset.z *= self._height / 2.0
        self.panda_node.setPos(obplugin.panda_utils.PandaConverter.convert_vector(position_offset))
        #self.panda_node.setQuat(obplugin.panda_utils.PandaConverter.convert_angle(self.owner.rotation))
        self.panda_node.setCollideMask(panda3d.core.BitMask32.allOn())

        self._linear_velocity = obengine.math.Vector(0, 0, 0)
        self._rotational_velocity = obengine.math.EulerAngle(0, 0, 0)

        self._loaded = True
        self.on_loaded()
