#
# This module implements a pulldown - a shutter-like widget that is hidden/shown
# by the touch of a button.
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
__date__  = "$Jul 11, 2011 12:26:46 PM$"


import obengine.datatypes
import obengine.event
import obengine.depman
import obengine.math
from obengine.gui import Widget

obengine.depman.gendeps()


class Pulldown(Widget):

    SPACING = 2.0

    def __init__(self, button, container, position = None):

        self._button = button
        if position is not None:
            self._button.position = position

        Widget.__init__(self, position)

        self._container = container
        container_pos = obengine.math.Vector2D(self._button.position.x,self._button.position.y)
        container_pos.y -= self._button.size.y + Pulldown.SPACING
        self._container.position = container_pos
        
        self.on_text_changed = self._button.on_text_changed
        self.on_click = self._button.on_click
        self.on_click += self._toggle_status
        
        self.on_hidden += self._container.hide
        self.on_shown += self._container.show
        self.pulldown_showing = False

    def add(self, widget):

        new_container_pos = obengine.math.Vector2D(self._container.position.x, self._container.position.y)
        new_container_pos.y -= widget.size.y
        self._container.position = new_container_pos
        
        self._container.add(widget)


    def remove(self, widget):
        
        new_container_pos = obengine.math.Vector2D(self._container.position.x, self._container.position.y)
        new_container_pos.y += widget.size.y
        self._container.position = new_container_pos

        self._container.remove(widget)
        
    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return self._button.position

        def fset(self, new_pos):

            self._button.position = new_pos
            self._container.position = Vector2D(new_pos.x, new_pos.y + self._button.size.y)
            self.on_position_changed(self._position)

        return locals()

    @obengine.datatypes.nested_property
    def text():

        def fget(self):
            return self._button.text

        def fset(self, new_text):
            self._button.text = new_text

        return locals()

    @obengine.datatypes.nested_property
    def pulldown_showing():

        def fget(self):
            return self._container.showing

        def fset(self, show):
            self._container.showing = show

        return locals()

    @obengine.datatypes.nested_property
    def showing():

        def fget(self):
            return self._showing

        def fset(self, show):

            self.pulldown_showing = show
            self._button.showing = show

        return locals()

    @property
    def size(self):
        return self._button.size

    def _toggle_status(self):
        self.pulldown_showing = not self.pulldown_showing