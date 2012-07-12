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
__date__ = "Jun 11, 2012 8:38:42 PM"


import widget
import obengine.event
import obengine.datatypes


class Checkbox(widget.ClickableWidget, widget.TextWidget):

    CHECKED, NOT_CHECKED = range(2)
    states = ['checked', 'unchecked', 'disabled']

    def __init__(self, parent, text, view):

        widget.Widget.__init__(self, 'checkbox', parent, view)
        widget.ClickableWidget.__init__(self)
        widget.TextWidget.__init__(self, text)

        self.on_state_changed = obengine.event.Event()

        self.on_click += self._toggle_state

    @obengine.datatypes.nested_property
    def state():

        def fget(self):
            return self.view.state

        def fset(self, state):

            old_state = self.state
            self.state = state

            if self.state != old_state:
                self.on_state_changed()

        return locals()

    def _toggle_state(self):
        self.state = not self.state
