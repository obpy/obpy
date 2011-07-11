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
from obengine.gui import Container

obengine.depman.gendeps()


class Pulldown(Container):

    def __init__(self, button, position):

        self._button = button
        
        if position is not None:
            self._button.position = position

        container_pos = obengine.math.Vector2D(self._button.position.x, self._button.position.y)
        container_pos.y += self._button.size.y

        Container.___init__(self, container_pos)
        
        self.on_text_changed = self._button.on_text_changed
        self.on_click = self._button.on_click
        self.on_click += self._toggle_status
        
    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return self._button.position

        def fset(self, new_pos):

            self._button.position = new_pos
            self._position = Vector2D(new_pos.x, new_pos.y + self._button.size.y)

            # Note that the menu display's position is used for
            # Widget.on_position_changed, insted of our button's position.
            # This might cause problems!
            
            self.on_position_changed(self._position)

        return locals()

    @obengine.datatypes.nested_property
    def text():

        def fget(self):
            return self._button.text

        def fset(self, new_text):
            self._button.text = new_text

        return locals()

    @property
    def size(self):
        return self._button.size

    def _toggle_status(self):

        if self.showing is True:
            self.showing = False

        else:
            self.showing = True