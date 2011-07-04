#
# This module provides the base logic for rendering GUI widgets with Panda3D/DirectGUI.
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
__date__  = "$Jul 1, 2011 2:57:27 PM$"


import uuid

import obengine.math
import obengine.datatypes
import obengine.event
import utils


WIDGET_SCALE = 0.05
PANDA_TO_OPENBLOX_SCALE = 100.0


class WidgetView(object):

    def __init__(self, position = None):

        self.on_size_changed = obengine.event.Event()
        self.position = position or obengine.math.Vector2D()
        base.taskMgr.add(self._update_pos, 'widget_pos' + str(uuid.uuid1()))

    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return self._position

        def fset(self, new_pos):

            self._position = new_pos
            panda_vector = utils.openblox_to_panda_pos(new_pos)
            self._widget.setPos(render2d, panda_vector)

        return locals()

    @obengine.datatypes.nested_property
    def size():

        def fget(self):

            width = (self._widget.getWidth()) * WIDGET_SCALE * PANDA_TO_OPENBLOX_SCALE
            height = (self._widget.getHeight()) * WIDGET_SCALE * PANDA_TO_OPENBLOX_SCALE

            return obengine.math.Vector2D(width, height)

        return locals()

    def _update_pos(self, task):
        self.position = self.position
        return task.cont


class TextWidgetView(WidgetView):

    def __init__(self, text = '', position = None):

        WidgetView.__init__(self, position)
        self.text = text

    @obengine.datatypes.nested_property
    def text():

        def fget(self):
            return self._widget['text']

        def fset(self, new_text):

            old_size = self.size
            self._widget['text'] = new_text
            self._widget.setText()
            self._widget.resetFrameSize()
            new_size = self.size

            if old_size.x != new_size.x or old_size.y != new_size.y:
                self.on_size_changed(new_size)

        return locals()