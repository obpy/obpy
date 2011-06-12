#
# This module implements a simple text label.
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
__date__  = "$Jun 10, 2011 4:44:38 PM$"


import obengine.datatypes
import obengine.event
import obengine.depman
from obengine.gui import Widget, WidgetPresenter, MockWidgetView


obengine.depman.gendeps()


class Label(Widget):
    """Represents a simple label"""

    def __init__(self, text, position = None):

        Widget.__init__(self, position)
        self._text = text

        self.on_text_changed = obengine.event.Event()

    @obengine.datatypes.nested_property
    def text():

        def fget(self):
            return self._text

        def fset(self, new_text):

            self._text = new_text
            self.on_text_changed(new_text)

        return locals()


class LabelPresenter(WidgetPresenter):

    def __init__(self, label_model, label_view):

        WidgetPresenter.__init__(self, label_model, label_view)

        self.on_text_changed = self._model.on_text_changed
        self._view.on_text_changed += self._update_text

    @obengine.datatypes.nested_property
    def text():

        def fget(self):
            return self._model.text

        def fset(self, new_text):

            self._view.text = text
            self._model.text = text

        return locals()

    def _update_text(self, new_text):
        self.text = new_text


class MockLabelView(MockWidgetView):

    def __init__(self, text, position = None):

        MockWidgetView.__init__(position)
        self._text = text
        
        self.on_text_changed = obengine.event.Event()

    @obengine.datatypes.nested_property
    def text():

        def fget(self):
            return self._text

        def fset(self, new_text):

            self._text = new_text
            self.on_text_changed(new_text)

        return locals()