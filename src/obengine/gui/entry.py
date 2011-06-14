#
# This module implements a simple text-entry widget. Note that you could use
# a multi-line entry or a single-line entry just by changing the view.
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
__date__  = "$Jun 14, 2011 2:26:44 AM$"


import obengine.event
import obengine.datatypes
import obengine.depman
from obengine.gui import Widget, WidgetPresenter, MockWidgetView


obengine.depman.gendeps()

class Entry(Widget):

    def __init__(self, initial_text = '', position = None):

        Widget.__init__(self, position)

        self._text = initial_text

        self.on_text_changed = obengine.event.Event()
        self.on_submitted = obengine.event.Event()

    @obengine.datatypes.nested_property
    def text():

        def fget(self):
            return self._text

        def fset(self, new_text):

            self._text = new_text
            self.on_text_changed(self.text)

        return locals()

    def submit(self):
        self.on_submitted()


class EntryPresenter(WidgetPresenter):

    def __init__(self, entry_model, entry_view):

        WidgetPresenter.__init__(self, entry_model, entry_view)

        self._view.on_submitted += self._model.submit
        self._view.on_text_changed += self._update_model_text

        self.on_submitted = self._model.on_submitted
        self.on_text_changed = self._model.on_text_changed

    def submit(self):
        self._view.submit()

    @obengine.datatypes.nested_property
    def text():

        def fget(self):
            return self._model.text

        def fset(self, new_text):

            # Why don't we update our model's text
            # here, too? Because in __init__, we bound our _update_model_text
            # handler, that automatically updates our model's text whenever
            # our view's text changes.

            self._view.text = new_text

        return locals()

    def _update_model_text(self, new_text):
        self._model.text = new_text


class MockEntryView(MockWidgetView):

    def __init__(self, initial_text = '', position = None):

        MockWidgetView.__init__(self, position)

        self._text = initial_text

        self.on_submitted = obengine.event.Event()
        self.on_text_changed = obengine.event.Event()

    def submit(self):
        self.on_submitted()

    @obengine.datatypes.nested_property
    def text():

        def fget(self):
            return self._text

        def fset(self, new_text):

            self._text = new_text
            self.on_text_changed(self.text)

        return locals()
