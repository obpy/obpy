#
# This module provides base classes for all OpenBlox widgets.
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
__date__  = "$Jun 11, 2011 1:07:32 AM$"


import obengine.datatypes
import obengine.event
import obengine.math
import obengine.depman
obengine.depman.gendeps()


class Widget(object):
    """Base class for all widgets
    This class meant to be used as a base class, not as-is.
    """

    def __init__(self, position = None):

        self._position = position or obengine.math.Vector2D()
        self._size = obengine.math.Vector2D()
        self._parent = None

        self.on_position_changed = obengine.event.Event()
        self.on_parent_changed = obengine.event.Event()
        self.on_size_changed = obengine.event.Event()

    @obengine.datatypes.nested_property
    def size():

        def fget(self):
            return self._size

        def fset(self, new_size):

            self._size = new_size
            self.on_size_changed(new_size)

        return locals()

    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return self._position

        def fset(self, new_pos):

            if isinstance(new_pos, tuple):
                self._position = obengine.math.Vector2D(*new_pos)

            else:
                self._position = new_pos

            self.on_position_changed(self._position)

        return locals()

    @obengine.datatypes.nested_property
    def parent():

        def fget(self):
            return self._parent

        def fset(self, new_parent):

            self._parent = new_parent
            self.on_parent_changed(new_parent)

        return locals()


class WidgetPresenter(object):

    def __init__(self, widget_model, widget_view):

        self._model = widget_model
        self._view = widget_view

        self.on_position_changed = self._model.on_position_changed
        self.on_parent_changed = self._model.on_parent_changed

        self._view.on_size_changed += self._update_size

    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return self._model.position

        def fset(self, new_pos):

            self._model.position = new_pos
            self._view.position = new_pos

        return locals()

    @obengine.datatypes.nested_property
    def parent():

        def fget(self):
            return self._model.parent

        def fset(self, new_parent):

            self._view.parent = new_parent
            self._model.parent = new_parent

        return locals()

    def _update_size(self, new_size):
        self._model.size = new_size

class MockWidgetView(object):

    def __init__(self, position = None):

        self._position = position or obengine.math.Vector2D()
        self._size = obengine.math.Vector2D()
        self._parent = None
        self.on_size_changed = obengine.event.Event()
        self._showing = False

    @obengine.datatypes.nested_property
    def parent():

        def fget(self):
            return self._parent

        def fset(self, new_parent):

            self._parent = new_parent

            if new_parent:
                self._showing = True

            else:
                self._showing = False

        return locals()

    @obengine.datatypes.nested_property
    def size():

        def fget(self):
            return self._size

        def fset(self, new_size):

            self._size = new_size
            self.on_size_changed(new_size)

        return locals()

    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return self._position

        def fset(self, new_pos):

            if isinstance(new_pos, tuple):
                self._position = obengine.math.Vector2D(*new_pos)

            else:
                self._position = new_pos

            self.on_position_changed(self._position)

        return locals()