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

import modelbase


CLICKABLE_BITMASK = BitMask32(0x101)

# TODO: Get rid of the need for this variable - it's very ugly!
loaded_models = {}


class Model(modelbase.ModelBase):
    """
    Represents a Panda3D model.
    NOTE: Textures loaded at runtime are currently NOT supported!
    
    """

    on_model_loaded = obengine.event.Event()

    def __init__(self, model_path, window, position = None, rotation = None, scale = None, color = None, clickable = True, compress = True):

        modelbase.ModelBase.__init__(self, window, position , rotation, scale, color, clickable, compress)
        self.panda_model_path = self.panda_path(model_path)

    def load(self, async = True):
        """
        Loads this model.
        Note that instead of waiting for this method to return,
        listen for this Model's on_loaded event. When that event is fired,
        the model is ready to be used.
        """

        if async is True:
            self.window.panda_window.loader.loadModel(self.panda_model_path, callback = self._set_load_okay)

        else:
            self._set_load_okay(self.window.panda_window.loader.loadModel(self.panda_model_path))


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
