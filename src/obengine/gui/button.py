#
# This module implements the business rules for a simple button widget.
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
__date__  = "$Jun 9, 2011 12:58:53 AM$"


import obengine.math
import obengine.datatypes
import obengine.event
from obengine.gui import Widget
import obengine.depman
obengine.depman.gendeps()


class Button(Widget):
    """Represents a button.
    Example:

        >>> from obengine.math import Vector2D
        >>> b = Button('Click me!')
        >>> print b.text
        Click me!
        >>> def test_click():
        ...     print 'Button pressed!'
        ...
        >>> b.on_click += test_click
        >>> b.on_click()
        Button pressed!
    """

    def __init__(self, text, position = None):

        Widget.__init__(self, position)

        self._text = text

        self.on_click = obengine.event.Event()
        self.on_text_changed = obengine.event.Event()

    @obengine.datatypes.nested_property
    def text():

        def fget(self):
            return self._text

        def fset(self, new_text):

            self._text = new_text
            self.on_text_changed(new_text)

        return locals()


class ButtonPresenter(object):

    def __init__(self, button_model, button_view):

        self._model = button_model
        self._view = button_view

        self.on_click = self._model.on_click
        self.on_position_changed = self._model.on_position_changed

        self._view.on_click += self.on_click

    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return self._model.position

        def fset(self, new_pos):

            self._model.position = new_pos
            self._view.position = new_pos

        return locals()

    @obengine.datatypes.nested_property
    def text():

        def fget(self):
            return self._model.text

        def fset(self, new_text):

            self._model.text = new_text
            self._view.text = new_text

        return locals()

    @property
    def size(self):
        return self._view.size

class MockButtonView(object):
    """A mock button view, for testing"""

    def __init__(self, text = '', position = None, size = None):

        self.position = position or obengine.math.Vector2D()
        self.size = size or obengine.math.Vector2D()

        self.on_click = obengine.event.Event()
        self.text = text