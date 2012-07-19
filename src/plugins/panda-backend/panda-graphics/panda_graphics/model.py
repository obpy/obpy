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
__date__ = "Jul 19, 2012 5:58:15 PM"


import uuid

from panda3d.core import *

import obengine.math
import obengine.event
import obengine.datatypes
import obplugin.panda_utils


CLICKABLE_BITMASK = BitMask32(0x101)

# TODO: Get rid of the need for this variable - it's very ugly!
loaded_models = {}


class Model(obplugin.panda_utils.PandaResource):
    """
    Represents a Panda3D model.
    NOTE: Textures loaded at runtime are currently NOT supported!
    
    """

    on_model_loaded = obengine.event.Event()

    def __init__(self, model_path, window, position = None, rotation = None, scale = None, color = None, clickable = True, cast_shadows = True, compress = True):

        obplugin.panda_utils.PandaResource.__init__(self)

        self.model_path = model_path
        self.panda_model_path = self.panda_path(model_path)
        self.panda_node = None
        self.load_okay = False
        self.window = window
        self._showing = False
        self.on_click = obengine.event.Event()
        self.cast_shadows = cast_shadows
        self.compress = compress

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

    def load(self, async = True):
        """
        Loads this model.
        Note that instead of waiting for this method to return,
        listen for this Model's on_loaded event. When that event is fired,
        the model is ready to be used.
        """

        self.window.panda_window.loader.loadModel(self.panda_model_path, callback = self._set_load_okay)

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

        Model.on_model_loaded(self)
        self.on_loaded()

    def _set_alpha(self, alpha = None):

        if alpha is None:
            alpha = self.color.a

        if alpha == 0:
            self.panda_node.setTransparency(TransparencyAttrib.MNone, True)
        else:
            self.panda_node.setTransparency(TransparencyAttrib.MAlpha, True)

        self.panda_node.setColor(self.color.r / obplugin.panda_utils.COLOR_SCALER, self.color.g / obplugin.panda_utils.COLOR_SCALER, self.color.b / obplugin.panda_utils.COLOR_SCALER, self.color.a / obplugin.panda_utils.COLOR_SCALER)


class Empty(object):

    def __init__(self):
        self.panda_node = NodePath('empty node')

    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return obplugin.panda_utils.PandaConverter.convert_vec3(self.panda_node.getPos())

        def fset(self, new_pos):
            self.panda_node.setPos(obplugin.panda_utils.PandaConverter.convert_vector(new_pos))

        return locals()

    @obengine.datatypes.nested_property
    def rotation():

        def fget(self):
            return obplugin.panda_utils.PandaConverter.convert_quat(self.panda_node.getPos())

        def fset(self, new_angle):
            self.panda_node.setHpr(obplugin.panda_utils.PandaConverter.convert_angle(new_angle))

        return locals()

    @obengine.datatypes.nested_property
    def parent():

        def fget(self):
            return self._parent

        def fset(self, parent):

            self._parent = parent
            self.panda_node.reparentTo(parent.panda_node)

        return locals()


class ModelCollector(obengine.datatypes.Borg):

    class RbcWrapper(object):

        def __init__(self, name):

            self._name = name
            self._combiner = RigidBodyCombiner(self._name)
            self.panda_node = NodePath(self._combiner)
            self.panda_node.setAttrib(RescaleNormalAttrib.make(RescaleNormalAttrib.MNormalize))

        def collect(self):
            self._combiner.collect()

    _model_combiners = []
    _model_batch = []
    _model_count = 0
    _MODELS_PER_COMBINER = 400
    _MODEL_BATCH_COUNT = 25

    assert _MODELS_PER_COMBINER % _MODEL_BATCH_COUNT == 0

    def __init__(self):

        if self._collect_model not in Model.on_model_loaded.handlers:
            Model.on_model_loaded += self._collect_model

    def _collect_model(self, model):

        if model.compress is False:
            return

        if len(self._model_combiners) == 0:
            self._create_new_combiner()

        if len(self._model_batch) >= self._MODEL_BATCH_COUNT:

            while len(self._model_batch) > 0:
                self._add_model(self._model_batch.pop())

            latest_combiner = self._model_combiners[-1]
            latest_combiner.collect()

            self._model_count += self._MODEL_BATCH_COUNT

        else:
            self._model_batch.append(model)

        if self._model_count >= self._MODELS_PER_COMBINER:

            self._create_new_combiner()
            self._model_count = 0

    def _create_new_combiner(self):

        combiner_name = 'rbc-%d' % (len(self._model_combiners))
        combiner = ModelCollector.RbcWrapper(combiner_name)

        self._model_combiners.append(combiner)
        combiner.panda_node.reparentTo(render)

    def _add_model(self, model):

        latest_combiner = self._model_combiners[-1]
        model.parent = latest_combiner
        model.on_parent_changed += lambda _: self._recollect_model(model, latest_combiner)
        model.on_hidden += latest_combiner.collect
        model.on_shown += latest_combiner.collect

    def _recollect_model(self, model, combiner):

        if model.parent == combiner:
            return

        model_parent = model.parent
        model_parent.parent = combiner
        combiner.collect()
