#
# This module provides a Panda3D/DirectGUI-based renderer for a shutter - a
# panel-like widget that hides itself when the mouse isn't over it.
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
__date__  = "$Jul 6, 2011 7:54:48 PM$"


import uuid

import panda3d.core
import direct.gui.DirectGui
import direct.gui.DirectGuiGlobals

import obengine.datatypes
import obengine.math
import obengine.event

import widget
import utils


class ShutterView(widget.WidgetView):

    def __init__(self, position = None):

        self._widget = direct.gui.DirectGui.DirectFrame()
        self._children = obengine.datatypes.orderedset()

        widget.WidgetView.__init__(self, position)

        self._old_mouse_x = 0
        self._old_mouse_y = 0
        self.on_mouse_moved = obengine.event.Event()

        base.taskMgr.add(self._check_mouse, 'shutter_check_mouse' + str(uuid.uuid1()))

    def add(self, widget):
        self._children.add(widget)

    def remove(self, widget):
        self._children.remove(widget)
        
    def show(self):
        for child in self._children:
            child.show()

    def hide(self):
        for child in self._children:
            child.hide()

    def _check_mouse(self, task):

        if base.mouseWatcherNode.hasMouse():
            
            current_mouse_x =  base.mouseWatcherNode.getMouseX() * utils.PANDA_TO_OPENBLOX_SCALE
            current_mouse_y = base.mouseWatcherNode.getMouseY() * utils.PANDA_TO_OPENBLOX_SCALE

            if self._old_mouse_x != current_mouse_x or self._old_mouse_y != current_mouse_y:

                self._old_mouse_x = current_mouse_x
                self._old_mouse_y = current_mouse_y
                self.on_mouse_moved(current_mouse_x, current_mouse_y)

        return task.cont