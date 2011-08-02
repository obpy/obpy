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
__date__ = "$Jul 2, 2011 3:20:40 PM$"


import panda3d.core

import direct.gui.DirectGui
import direct.gui.DirectGuiGlobals

import obengine.math
import obengine.datatypes
import obengine.event
import widget


class EntryView(widget.WidgetView):

    def __init__(self, text = '', position = None, length = 20):

        font = loader.loadFont('cmtt12')

        self.on_submitted = obengine.event.Event()
        self._widget = direct.gui.DirectGui.DirectEntry(
        scale = widget.WIDGET_SCALE,
        relief = direct.gui.DirectGuiGlobals.SUNKEN,
        text_align = panda3d.core.TextNode.ACenter,
        entryFont = font,
        width = length / 2 + (1, 0.5)[length % 2 == 0],
        command = self.on_submitted,
        initialText = text
        )

        widget.WidgetView.__init__(self, position)

    @obengine.datatypes.nested_property
    def text():

        def fget(self):
            return self._widget.get(plain = True)

        def fset(self, new_text):
            self._widget.enterText(new_text)

        return locals()
