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
        self._showing = False

        self.on_position_changed = obengine.event.Event()
        self.on_parent_changed = obengine.event.Event()
        self.on_size_changed = obengine.event.Event()
        self.on_hidden = obengine.event.Event()
        self.on_shown = obengine.event.Event()
        self.on_focus_gained = obengine.event.Event()
        self.on_focus_lost = obengine.event.Event()

        self.on_hidden += self._disable_events
        self.on_shown += self._enable_events
        
        self.on_focus_gained += self._gain_focus
        self.on_focus_lost += self._lose_focus

    def show(self):
        if self.showing is False:
            self.showing = True

    def hide(self):
        if self.showing is True:
            self.showing = False

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

    @obengine.datatypes.nested_property
    def showing():

        def fget(self):
            return self._showing

        def fset(self, showing):

            old_showing = self.showing
            self._showing = showing

            if self._showing is True and old_showing is False:
                self.on_shown()

            elif self._showing is False and old_showing is True:
                self.on_hidden()

        return locals()

    @property
    def focused(self):
        return self._focused
    
    def _disable_events(self):
        
        self.on_focus_gained.disable()
        self.on_focus_lost.disable()
        
    def _enable_events(self):
        
        self.on_focus_gained.enable()
        self.on_focus_lost.enable()

    def _gain_focus(self):
        self._focused = True

    def _lose_focus(self):
        self._focused = False


class WidgetPresenter(object):

    def __init__(self, widget_model, widget_view):

        self._model = widget_model
        self._view = widget_view

        self.on_position_changed = self._model.on_position_changed
        self.on_parent_changed = self._model.on_parent_changed
        self.on_size_changed = self._model.on_size_changed
        self.on_focus_gained = self._model.on_focus_gained
        self.on_focus_lost = self._model.on_focus_lost
        self.on_shown = self._model.on_shown
        self.on_hidden = self._model.on_hidden

        self._view.on_size_changed += self._update_size
        self._view.on_focus_gained = self._model.on_focus_gained
        self._view.on_focus_lost = self._model.on_focus_lost
        self.show = self._model.show
        self.hide = self._model.hide

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

    @obengine.datatypes.nested_property
    def showing():

        def fget(self):
            return self._model.showing

        def fset(self, show):
            self._model.showing = show

        return locals()

    def _update_size(self, new_size):
        self._model.size = new_size


class MockWidgetView(object):

    def __init__(self, position = None):

        self._position = position or obengine.math.Vector2D()
        self._size = obengine.math.Vector2D()
        self._parent = None
        self._showing = False

        self.on_size_changed = obengine.event.Event()
        self.on_focus_gained = obengine.event.Event()
        self.on_focus_lost = obengine.event.Event()

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