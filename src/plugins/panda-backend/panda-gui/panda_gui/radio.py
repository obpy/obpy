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
__date__  = "$Jul 4, 2011 2:26:23 PM$"


import panda3d.core

import direct.gui.DirectGui
import direct.gui.DirectGuiGlobals

import obengine.datatypes
import obengine.event
import obengine.gui
import widget


class RadioView(widget.TextWidgetView):

    def __init__(self, text = '', state = None, position = None):
        
        self.on_click = obengine.event.Event()

        self._widget = direct.gui.DirectGui.DirectRadioButton(
        scale = widget.WIDGET_SCALE,
        text_align = panda3d.core.TextNode.ACenter,
        #relief = direct.gui.DirectGuiGlobals.FLAT,
        textMayChange = True,
        command = self.on_click
        )

        self.state = state or obengine.gui.Radio.DISABLED
        widget.TextWidgetView.__init__(self, text, position)

    @obengine.datatypes.nested_property
    def state():

        def fget(self):

            panda_to_openblox_state = {
            0 : obengine.gui.Radio.DISABLED,
            1 : obengine.gui.Radio.ENABLED
            }

            return  panda_to_openblox_state[self._widget['state']]

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