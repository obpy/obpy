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
        self._showing = True

        self.on_position_changed = obengine.event.Event()
        self.on_parent_changed = obengine.event.Event()
        self.on_size_changed = obengine.event.Event()
        self.on_hidden = obengine.event.Event()
        self.on_shown = obengine.event.Event()
        

    def show(self):
        self.showing = True

    def hide(self):
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


class ClickableWidget(Widget):

    def __init__(self, position = None):

        Widget.__init__(self, position)

        self.on_click = obengine.event.Event()
        self.on_hidden += self.on_click.disable
        self.on_shown += self.on_click.enable


class TextWidget(Widget):

    def __init__(self, text, position):

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


class WidgetPresenter(object):

    def __init__(self, widget_model, widget_view):

        self._model = widget_model
        self._view = widget_view

        self.on_position_changed = self._model.on_position_changed
        self.on_parent_changed = self._model.on_parent_changed
        self.on_size_changed = self._model.on_size_changed
        self.on_shown = self._model.on_shown
        self.on_hidden = self._model.on_hidden

        self._view.on_size_changed += self._update_size

    def show(self):

        self._model.show()
        self._view.show()

    def hide(self):

        self._model.hide()
        self._view.hide()

    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return self._model.position

        def fset(self, new_pos):

            self._model.position = new_pos
            self._view.position = new_pos

        return locals()

    @obengine.datatypes.nested_property
    def size():

        def fget(self):
            return self._view.size

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
            self._view.showing = show

        return locals()

    def _update_size(self, new_size):
        self._model.size = new_size


class ClickableWidgetPresenter(WidgetPresenter):

    def __init__(self, widget_model, widget_view):

        WidgetPresenter.__init__(self, widget_model, widget_view)

        self.on_click = self._model.on_click
        self._view.on_click += self.on_click


class TextWidgetPresenter(WidgetPresenter):

    def __init__(self, widget_model, widget_view):

        WidgetPresenter.__init__(self, widget_model, widget_view)
        self.on_text_changed = self._model.on_text_changed

    @obengine.datatypes.nested_property
    def text():

        def fget(self):
            return self._model.text

        def fset(self, new_text):

            self._view.text = new_text
            self._model.text = new_text

        return locals()


class MockWidgetView(object):

    def __init__(self, position = None):

        self._position = position or obengine.math.Vector2D()
        self._size = obengine.math.Vector2D()
        self._parent = None
        self._showing = False

        self.on_size_changed = obengine.event.Event()

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

        return locals()


class MockClickableWidgetView(MockWidgetView):

    def __init__(self, position = None):

        MockWidgetView.__init__(self, position)
        self.on_click = obengine.event.Event()


class MockTextWidgetView(MockWidgetView):

    _TEXT_SCALE = 0.5
    _VERTICAL_TEXT_SIZE = 0.5

    def __init__(self, text = '', position = None):

        MockWidgetView.__init__(self, position)

        self.on_text_changed = obengine.event.Event()
        self.text = text

    @obengine.datatypes.nested_property
    def text():

        def fget(self):
            return self._text

        def fset(self, new_text):

            self._text = new_text
            self._size = obengine.math.Vector2D(
            len(self.text) * MockTextWidgetView._TEXT_SCALE,
            MockTextWidgetView._VERTICAL_TEXT_SIZE)

        return locals()