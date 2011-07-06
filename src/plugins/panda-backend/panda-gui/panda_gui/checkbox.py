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
__date__  = "$Jul 5, 2011 12:58:23 PM$"


import panda3d.core

import direct.gui
import direct.gui.DirectGui
import direct.gui.DirectGuiGlobals

import obengine.gui
import obengine.datatypes
import obengine.event
import widget


class CheckboxView(widget.TextWidgetView):

    def __init__(self, text = '', position = None, state = None):

        state = state or obengine.gui.Checkbox.NOT_CHECKED
        self.on_click = obengine.event.Event()

        self._widget = direct.gui.DirectGui.DirectCheckButton(
        scale = widget.WIDGET_SCALE,
        text_align = panda3d.core.TextNode.ACenter,
        #relief = direct.gui.DirectGuiGlobals.FLAT,
        textMayChange = True,
        command = self._fire_click_event,
        )

        self.state = state
        widget.TextWidgetView.__init__(self, text, position)

    @obengine.datatypes.nested_property
    def state():

        def fget(self):

            panda_to_openblox_state = {
            True : obengine.gui.Checkbox.NOT_CHECKED,
            False : obengine.gui.Checkbox.CHECKED
            }

            return panda_to_openblox_state[self._widget['indicatorValue']]
        
        def fset(self, new_state):
            
            openblox_to_panda_state = {
            obengine.gui.Checkbox.NOT_CHECKED : True,
            obengine.gui.Checkbox.CHECKED : False
            }

            if new_state not in openblox_to_panda_state:
                raise ValueError('Invalid checkbox state')

            self._widget['indicatorValue'] = openblox_to_panda_state[new_state]
            self._widget.setIndicatorValue()

        return locals()

    def _fire_click_event(self, _):
        self.on_click()