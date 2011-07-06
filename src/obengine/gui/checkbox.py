#
# This module provides the business rules to implement a checkbox widget.
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
__date__  = "$Jul 5, 2011 10:24:39 AM$"


import obengine.datatypes
import obengine.event
import obengine.math
from obengine.gui import ClickableWidget, TextWidget
from obengine.gui import ClickableWidgetPresenter, TextWidgetPresenter
from obengine.gui import MockClickableWidgetView, MockTextWidgetView
import obengine.depman
obengine.depman.gendeps()


class Checkbox(ClickableWidget, TextWidget):

    CHECKED, NOT_CHECKED = range(2)

    def __init__(self, text = '', position = None, state = NOT_CHECKED):

        ClickableWidget.__init__(self, position)
        TextWidget.__init__(self, text, position)

        self.on_state_changed = obengine.event.Event()
        self._state = state
        self.state = state
        self.on_click += self._toggle_state

    @obengine.datatypes.nested_property
    def state():

        def fget(self):
            return self._state

        def fset(self, new_state):

            if self.state != new_state:

                self._state = new_state
                self.on_state_changed(self.state)

        return locals()

    def _toggle_state(self):
        self.state = not self.state


class CheckboxPresenter(ClickableWidgetPresenter, TextWidgetPresenter):

    def __init__(self, model, view):

        ClickableWidgetPresenter.__init__(self, model, view)
        TextWidgetPresenter.__init__(self, model, view)

        self.on_state_changed = self._model.on_state_changed
        self.on_state_changed += self._update_view_state

    @obengine.datatypes.nested_property
    def state():

        def fget(self):
            return self._model.state

        def fset(self, new_state):
            self._model.state = new_state

        return locals()

    def _update_view_state(self, new_state):
        self._view.state = new_state


class MockCheckboxView(MockClickableWidgetView, MockTextWidgetView):

    def __init__(self, text = '', position = None, state = Checkbox.NOT_CHECKED):

        MockClickableWidgetView.__init__(self, position)
        MockTextWidgetView.__init__(self, text, position)

        self.state = state

    @obengine.datatypes.nested_property
    def state():

        def fget(self):
            return self._state

        def fset(self, new_state):
            self._state = new_state

        return locals()