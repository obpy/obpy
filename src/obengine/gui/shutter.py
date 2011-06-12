#
# This module implements a shutter - a panel/container that disappears when the mouse
# is outside its bounding box.
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
__date__  = "$Jun 12, 2011 2:01:44 AM$"


import obengine.datatypes
import obengine.event
import obengine.utils
import obengine.depman
from obengine.gui import Container, WidgetPresenter, MockWidgetView


obengine.depman.gendeps()


class Shutter(Container):

    def __init__(self, layout_manager, position):
        
        Container.__init__(self, layout_manager, position)

        self._showing = False

        self.on_hide = obengine.event.Event()
        self.on_show = obengine.event.Event()

    def hide(self):

        self._showing = False
        self.on_hide()

    def show(self):

        self._showing = True
        self.on_show()


class ShutterPresenter(WidgetPresenter):

    def __init__(self, shutter_model, shutter_view):

        WidgetPresenter.__init__(self, shutter_model, shutter_view)

        self._view.on_mouse_move += self._update_model
        self.on_hide = self._model.on_hide
        self.on_show = self._model.on_show

        self.on_hide += self._view.hide
        self.on_show += self._view.show

    @property
    def showing(self):
        return self._view.showing

    def _update_model(self, mouse_x, mouse_y):

        if self._check_in_range(mouse_x, self._model.position.x, self._model.size.x) is True:
            if self._check_in_range(mouse_y, self._model.position.y, self._model.size.y) is True:
                if self.showing is False:

                    self.on_show()
                    return

        if self.showing is True:
            self.on_hide()

    def _check_in_range(self, mouse_pos, axis, size):
        return abs(mouse_pos) in range(abs(axis), abs(axis + size) + 1)


class MockShutterView(MockWidgetView):

    def __init__(self, position = None):

        MockWidgetView.__init__(position)

        self._showing = False
        self.on_mouse_move = obengine.event.Event()

    def hide(self):
        self._showing = False

    def show(self):
        self._showing = True

    @property
    def showing(self):
        return self._showing