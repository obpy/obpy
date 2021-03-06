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
__date__ = "$Jun 30, 2011 12:06:54 AM$"


import panda3d.core
from panda3d.core import TransparencyAttrib, Filename

import direct.gui
import direct.gui.DirectGui
import direct.gui.DirectGuiGlobals

import obengine.datatypes
import obengine.event
import widget


class ButtonView(widget.TextWidgetView):

    def __init__(self, text = '', position = None, icon = None):

        self.on_click = obengine.event.Event()

        self._widget = direct.gui.DirectGui.DirectButton(
        scale = widget.WIDGET_SCALE,
        text_align = panda3d.core.TextNode.ACenter,
        #relief = direct.gui.DirectGuiGlobals.FLAT,
        textMayChange = True,
        command = self.on_click
        )

        if icon is not None:
            self.icon = icon

        widget.TextWidgetView.__init__(self, text, position)

    @obengine.datatypes.nested_property
    def icon():

        def fget(self):
            return self._widget['image']

        def fset(self, new_image):

            old_size = self.size
            self._widget['image'] = str(Filename.fromOsSpecific(new_image))

            if new_image is not None:
                self._widget['image_pos'] = (-2.5, 0, 0)

            else:
                self._widget['image_pos'] = (0, 0, 0)

            self._widget.setImage()

            for state in range(0, 4):
                self._widget.component('image' + str(state)).setTransparency(TransparencyAttrib.MAlpha)

            self._check_size(old_size)

        return locals()
