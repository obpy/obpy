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
from obengine.gui import TextWidget, TextWidgetPresenter, MockTextWidgetView
obengine.depman.gendeps()


class Entry(TextWidget):

    def __init__(self, initial_text = '', position = None):

        TextWidget.__init__(self, initial_text, position)
        self.on_submitted = obengine.event.Event()

    def submit(self):
        self.on_submitted()


class EntryPresenter(TextWidgetPresenter):

    def __init__(self, entry_model, entry_view):

        TextWidgetPresenter.__init__(self, entry_model, entry_view)

        self._view.on_submitted += self._update_model_text
        self._view.on_submitted += self._model.submit

        self.on_submitted = self._model.on_submitted
        self.on_text_changed = self._model.on_text_changed

    def submit(self):
        self._view.submit()

    def _update_model_text(self, new_text):
        self._model.text = new_text


class MockEntryView(MockTextWidgetView):

    def __init__(self, initial_text = '', position = None):
        
        MockTextWidgetView.__init__(self, initial_text, position)
        self.on_submitted = obengine.event.Event()

    def submit(self):
        self.on_submitted()
