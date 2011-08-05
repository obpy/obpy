#
# This module implements the rendering code for a radio button.
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
__date__ = "$Jul 4, 2011 2:26:23 PM$"


import panda3d.core
from panda3d.core import Filename, TransparencyAttrib

import direct.gui.DirectGui
import direct.gui.DirectGuiGlobals

import obengine.datatypes
import obengine.event
import obengine.gui
import widget


class RadioView(widget.TextWidgetView):

    def __init__(self, text = '', position = None, state = None, icon = None):

        self.on_click = obengine.event.Event()
        self.on_state_changed = obengine.event.Event()

        self._old_state = state or obengine.gui.Radio.DISABLED

        self._widget = direct.gui.DirectGui.DirectRadioButton(
        scale = widget.WIDGET_SCALE,
        text_align = panda3d.core.TextNode.ACenter,
        #relief = direct.gui.DirectGuiGlobals.FLAT,
        textMayChange = True,
        command = self._fire
        )

        self.state = state or obengine.gui.Radio.DISABLED

        if icon is not None:
            self.icon = icon

        widget.TextWidgetView.__init__(self, text, position)

    @obengine.datatypes.nested_property
    def state():

        def fget(self):

            panda_to_openblox_state = {
            0 : obengine.gui.Radio.DISABLED,
            1 : obengine.gui.Radio.ENABLED
            }

            try:
                return panda_to_openblox_state[self._widget['indicatorValue']]

            except AttributeError:
                return obengine.gui.Radio.DISABLED

        def fset(self, new_state):

            openblox_to_panda_state = {
            obengine.gui.Radio.DISABLED : 0,
            obengine.gui.Radio.ENABLED : 1
            }

            if new_state not in openblox_to_panda_state:
                raise ValueError('Invalid radio button state')

            self._widget['indicatorValue'] = openblox_to_panda_state[new_state]
            self._widget.setIndicatorValue()

        return locals()

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

    def _fire(self):

        self.on_click()

        cur_state = self.state
        if cur_state != self._old_state:
            self.on_state_changed(cur_state)

        self._old_state = cur_state
