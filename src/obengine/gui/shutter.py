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

    def __init__(self, layout_manager, position = None):
        Container.__init__(self, layout_manager, position)

    def update(self, mouse_x, mouse_y):

        if self._check_in_range(mouse_x, self.position.x, self.size.x) is True:
            if self._check_in_range(mouse_y, self.position.y, self.size.y) is True:
                if self.showing is False:

                    self.show()
                    return

        if self.showing is True:
            self.hide()

    def _check_in_range(self, mouse_pos, axis, size):
        return abs(mouse_pos) in range(abs(axis), abs(axis + size) + 1)


class ShutterPresenter(WidgetPresenter):
    """Binds the shutter model and view together.
    Example:
        >>> from obengine.gui import VerticalLayoutManager
        >>> s = Shutter(VerticalLayoutManager)
        >>> msv = MockShutterView()
        >>> sp = ShutterPresenter(s, msv)
        >>> msv.on_mouse_move(0, 0)
        >>> sp.showing
        True
        >>> msv.on_mouse_move(1, 0)
        >>> sp.showing
        False
    """

    def __init__(self, shutter_model, shutter_view):

        WidgetPresenter.__init__(self, shutter_model, shutter_view)

        self._view.on_mouse_move += self._model.update
        self.on_hidden = self._model.on_hidden
        self.on_shown = self._model.on_shown

        self.on_hidden += self._view.hide
        self.on_shown += self._view.show

    @property
    def showing(self):
        return self._model.showing


class MockShutterView(MockWidgetView):

    def __init__(self, position = None):

        MockWidgetView.__init__(self, position)

        self._showing = False
        self.on_mouse_move = obengine.event.Event()

    def hide(self):
        self._showing = False

    def show(self):
        self._showing = True

    @property
    def showing(self):
        return self._showing