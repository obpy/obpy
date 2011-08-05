#
# This module provides a radio button widget.
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
__date__ = "$Jun 22, 2011 6:45:12 PM$"


import obengine.datatypes
import obengine.event
import obengine.math
from obengine.gui import Widget, WidgetPresenter, MockWidgetView


class Radio(Widget):
    """Business rules for a radio button
    Example:

        >>> r = Radio('Radio button')
        >>> print r.text
        Radio button
        >>> r.state = Radio.ENABLED
        >>> r.state == Radio.ENABLED
        True
        >>> def on_state_changed(new_state):
        ...     print 'State changed!'
        ...
        >>> r.on_state_changed += on_state_changed
        >>> r.state = Radio.DISABLED
        State changed!
        >>> r.state = Radio.DISABLED
        >>> r.state = Radio.ENABLED
        State changed!
    """

    ENABLED, DISABLED = range(2)

    def __init__(self, label, position = None, state = None):

        Widget.__init__(self, position)

        self.on_state_changed = obengine.event.Event()
        self.on_text_changed = obengine.event.Event()

        self._state = state or Radio.DISABLED
        self._text = label

    @obengine.datatypes.nested_property
    def state():

        def fget(self):
            return self._state

        def fset(self, new_state):
            self.set_state(new_state)

        return locals()

    @obengine.datatypes.nested_property
    def text():

        def fget(self):
            return self._text

        def fset(self, new_text):

            self._text = new_text
            self.on_text_changed(self.text)

        return locals()

    def set_state(self, new_state, propagate = True):

        print 'Setting state to', bool(new_state)

        if new_state == self.state:
            return

        self._state = new_state
        self.on_state_changed(self.state)

        if propagate is True:
            if self.parent is not None:
                for child in filter(lambda w: w is not self, self.parent.children):

                    try:
                        child.state

                    except AttributeError:
                        continue

                    child.set_state(not new_state, False)


class RadioPresenter(WidgetPresenter):

    def __init__(self, model, view):

        WidgetPresenter.__init__(self, model, view)

        self.on_text_changed = self._model.on_text_changed
        self.on_state_changed = self._model.on_state_changed

        self.on_text_changed += self._update_view_text
        self.on_state_changed += self._update_view_state

        self._view.on_state_changed += self._update_model_state

        self.on_click = self._view.on_click

    def set_state(self, state, propagate = True):

        self._model.set_state(int(state), propagate)

    @obengine.datatypes.nested_property
    def text():

        def fget(self):
            return self._model.text

        def fset(self, new_text):
            self._model.text = new_text

        return locals()

    @obengine.datatypes.nested_property
    def state():

        def fget(self):
            return self._model.state

        def fset(self, new_state):
            self._model.state = new_state

        return locals()

    @obengine.datatypes.nested_property
    def icon():

        def fget(self):
            return self._view.icon

        def fset(self, new_icon):
            self._view.icon = new_icon

        return locals()

    def _update_view_state(self, new_state):
        self._view.state = new_state

    def _update_view_text(self, new_text):
        self._view.text = new_text

    def _update_model_state(self, new_state):
        self._model.state = new_state


class MockRadioView(MockWidgetView):

    _VERTICAL_TEXT_SIZE = 0.5
    _TEXT_SCALE = 0.5

    def __init__(self, text, position = None):

        MockWidgetView.__init__(self, position)

        self._text = text
        self._state = Radio.DISABLED

        self.size = obengine.math.Vector2D(
        len(self.text) * MockRadioView._TEXT_SCALE,
        MockRadioView._VERTICAL_TEXT_SIZE
        )

    @obengine.datatypes.nested_property
    def text():

        def fget(self):
            return self._text

        def fset(self, new_text):

            self._text = new_text
            self.size = obengine.math.Vector2D(
            len(self.text) * MockRadioView._TEXT_SCALE,
            MockRadioView._VERTICAL_TEXT_SIZE
            )

        return locals()
