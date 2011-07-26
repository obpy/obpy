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
__date__  = "$Jul 26, 2011 10:36:43 AM$"


import direct.gui.DirectGui

import obengine.math

import widget


class ScrolledListView(widget.WidgetView):

    def __init__(self, position = None):

        position = position or obengine.math.Vector2D()

        self._widget = direct.gui.DirectGui.DirectScrolledFrame(
        canvasSize = (-2, 2, -2, 2),
        frameSize = (-0.50, 0.50, -0.25, 0.25)) # TODO: Replace this with a dynamically
        # resizing frame!

        widget.WidgetView.__init__(self, position)

    def add(self, widget):

        widget._view.parent = self
        widget._view._widget.reparentTo(self._widget.getCanvas())

    def remove(self, widget):

        widget._view.parent = None
        widget._view._widget.reparentTo(aspect2d)