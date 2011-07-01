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
from obengine.gui import ClickableWidget, TextWidget
from obengine.gui import ClickableWidgetPresenter, TextWidgetPresenter
from obengine.gui import MockClickableWidgetView, MockTextWidgetView
import obengine.depman
obengine.depman.gendeps()


class Button(ClickableWidget, TextWidget):
    """Represents a button.
    Example:

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

    def __init__(self, text, position = None, icon = None):

        ClickableWidget.__init__(self, position)
        TextWidget.__init__(self, text, position)

        self._icon = icon

    @property
    def icon(self):
        return self.icon


class ButtonPresenter(ClickableWidgetPresenter, TextWidgetPresenter):

    def __init__(self, button_model, button_view):

        ClickableWidgetPresenter.__init__(self, button_model, button_view)
        TextWidgetPresenter.__init__(self, button_model, button_view)

    @property
    def icon(self):
        return self._model.icon


class MockButtonView(MockClickableWidgetView, MockTextWidgetView):
    """A mock button view, for testing"""

    def __init__(self, text = '', position = None, icon = None):

        MockClickableWidgetView.__init__(self, position)
        MockTextWidgetView.__init__(self, text, position)

        self.icon = icon