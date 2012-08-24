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
__date__ = "Aug 20, 2012 7:15:16 PM"


import uuid

from panda3d.core import *

import obengine.math
import obengine.event
import obengine.datatypes
import obplugin.panda_utils


CLICKABLE_BITMASK = BitMask32(0x101)

# TODO: Get rid of the need for this variable - it's very ugly!
loaded_models = {}


class ModelBase(obplugin.panda_utils.PandaResource):

    on_model_loaded = obengine.event.Event()

    def __init__(self, window, position = None, rotation = None, scale = None, color = None, clickable = True, compress = True):

        self.panda_node = None
        self.load_okay = False
        self.on_loaded = obengine.event.Event()
        self.window = window
        self.on_click = obengine.event.Event()
        self.compress = compress
        self._showing = False

        self._texture = None
        self._parent = None
        self._position = position or obengine.math.Vector()
        self._setup_position()
        self._color = color or obengine.math.Color()
        self._setup_color()
        self._rotation = rotation or obengine.math.EulerAngle()
        self._setup_rotation()
        self._scale = scale or obengine.math.Vector()
        self._setup_scale()

        self.on_parent_changed = obengine.event.Event()
        self.on_shown = obengine.event.Event()
        self.on_hidden = obengine.event.Event()

        self._clickable = clickable


    @property
    def bounds(self):

        point1 = Point3()
        point2 = Point3()

        self.panda_node.calcTightBounds(point1, point2)
        point1 = obplugin.panda_utils.PandaConverter.convert_vec3(point1)
        point2 = obplugin.panda_utils.PandaConverter.convert_vec3(point2)

        x_bounds = point2.x - point1.x
        y_bounds = point2.y - point1.y
        z_bounds = point2.z - point1.z

        return obengine.math.Vector(x_bounds, y_bounds, z_bounds)

    @property
    def showing(self):
        return self._showing

    @showing.setter
    def showing(self, val):

        if val is True:

            self.panda_node.show()
            self.on_shown()

        elif val is False:

            self.panda_node.hide()
            self.on_hidden()

        else:
            raise ValueError('val must be either True or False (was %s)' % val)

    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return self._position

        def fset(self, pos):

            if isinstance(pos, tuple):
                  self._position = obengine.math.Vector(*pos)
                  self.panda_node.setPos(self.convert_vector(self._position))

            else:
                  self._position.x = pos.x
                  self._position.y = pos.y
                  self._position.z = pos.z

        return locals()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, new_scale):

        if isinstance(new_scale, tuple):

            self._scale = obengine.math.Vector(*new_scale)
            self.panda_node.setScale(*self.convert_vector(self._scale))

        else:

            self._scale.x = new_scale.x
            self._scale.y = new_scale.y
            self._scale.z = new_scale.z

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rot):

        if isinstance(rot, tuple):

            self._rotation = rot
            self.panda_node.setHpr(*self.convert_euler_angle(self._rotation))

        else:

            self._rotation.h = rot.h
            self._rotation.p = rot.p
            self._rotation.r = rot.r

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):

        if isinstance(color, tuple):
            self._color = obengine.math.Color(*color)

        else:

            self._color.r = color.r
            self._color.g = color.g
            self._color.b = color.b
            self._color.a = color.a

        self.panda_node.setColor(self.convert_color(self._color))
        self._set_alpha(self._color.a)

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, tex):

        self._texture = tex
        self.panda_node.setTexture(tex.texture)

    @obengine.datatypes.nested_property
    def parent():

        def fget(self):
            return self._parent

        def fset(self, parent):

            self._parent = parent
            self.panda_node.reparentTo(parent.panda_node)

            self.on_parent_changed(self.parent)

        return locals()

    def _setup_position(self):

        self._position.on_x_changed += lambda x: self.panda_node.setX(x)
        self._position.on_y_changed += lambda y: self.panda_node.setY(y)
        self._position.on_z_changed += lambda z: self.panda_node.setZ(z)

    def _setup_scale(self):

        self._scale.on_x_changed += lambda x: self.panda_node.setScale(self._scale.x, self._scale.y, self._scale.z)
        self._scale.on_y_changed += lambda y: self.panda_node.setScale(self._scale.x, self._scale.y, self._scale.z)
        self._scale.on_z_changed += lambda z: self.panda_node.setScale(self._scale.x, self._scale.y, self._scale.z)

    def _setup_rotation(self):

        self._rotation.on_h_changed += lambda h: self.panda_node.setH(h)
        self._rotation.on_p_changed += lambda p: self.panda_node.setP(p)
        self._rotation.on_r_changed += lambda r: self.panda_node.setR(r)

    def _setup_color(self):

        self._color.on_r_changed += lambda r: self.panda_node.setColor(r / obplugin.panda_utils.COLOR_SCALER, self._color.g, self._color.b)
        self._color.on_g_changed += lambda g: self.panda_node.setColor(self._color.r, g / obplugin.panda_utils.COLOR_SCALER, self._color.b)
        self._color.on_b_changed += lambda b: self.panda_node.setColor(self._color.r, self._color.g, b / obplugin.panda_utils.COLOR_SCALER)
        self._color.on_a_changed += lambda a: self._set_alpha(a)

    def _check_mouse(self):

        if self.window.panda_window.mouseWatcherNode.hasMouse() is False:
            return

        mouse_pos = self.window.panda_window.mouseWatcherNode.getMouse()
        self.window.picker_ray.setFromLens(
        self.window.panda_window.camNode,
        mouse_pos.getX(),
        mouse_pos.getY())

        self.window.mouse_traverser.traverse(self.window.panda_window.render)

        if self.window.collision_queue.getNumEntries() > 0:

            self.window.collision_queue.sortEntries()
            picked_node = self.window.collision_queue.getEntry(0).getIntoNodePath().findNetTag('clickable-flag')

            picked_node_uuid = picked_node.getTag('clickable-flag')

            if picked_node_uuid == self._uuid:
                self.on_click()

    def _set_load_okay(self, model):

        self.load_okay = True
        self._uuid = str(uuid.uuid1())
        loaded_models[self._uuid] = self

        self.panda_node = model
        self.panda_node.setTag('clickable-flag', self._uuid)
        self.panda_node.reparentTo(self.window.panda_window.render)
        self.showing = True

        if self._clickable is True:
            self.panda_node.setCollideMask(CLICKABLE_BITMASK)

        ModelBase.on_model_loaded(self)
        self.on_loaded()

    def _set_alpha(self, alpha = None):

        if alpha is None:
            alpha = self.color.a

        if alpha == 0:
            self.panda_node.setTransparency(TransparencyAttrib.MNone, True)
        else:
            self.panda_node.setTransparency(TransparencyAttrib.MAlpha, True)

        self.panda_node.setColor(self.color.r / obplugin.panda_utils.COLOR_SCALER, self.color.g / obplugin.panda_utils.COLOR_SCALER, self.color.b / obplugin.panda_utils.COLOR_SCALER, self.color.a / obplugin.panda_utils.COLOR_SCALER)
