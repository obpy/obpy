#
# This module implements the business rules for various simple widget containers.
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
__date__  = "$Jun 9, 2011 8:00:27 PM$"


import obengine.math
import obengine.datatypes
import obengine.event
import obengine.depman
from obengine.gui import Widget


obengine.depman.gendeps()
PAD_SPACE = 0.5


class Container(Widget):
    """Represents a basic container
    This class provides the high-level algorithms required to
    implement a simple widget container.
    However, to use this class, you'll need to use a layout manager (which
    actually implements the widget partioning algorithim) first.
    The layout managers that come with OpenBlox are currently:

    * VerticalLayoutManager (just like PyGTK's VBox)
    * HorizontalLayoutManager (like PyGTK's HBox)

    Example:

        >>> from obengine.gui import *
        >>> from obengine.math import Vector2D
        >>> c = Container(HorizontalLayoutManager)
        >>> button_view_1 = MockButtonView('Click me!', size = Vector2D(2, 5))
        >>> button_model_1 = Button('Click me!', Vector2D(0, 0))
        >>> button_presenter_1 = ButtonPresenter(button_model_1, button_view_1)
        >>> button_view_2 = MockButtonView('Click me, too!', size = Vector2D(3, 6))
        >>> button_model_2 = Button('Click me, too!', Vector2D(0, 0))
        >>> button_presenter_2 = ButtonPresenter(button_model_2, button_view_2)
        >>> c.add(button_presenter_1)
        >>> c.add(button_presenter_2)
        >>> print button_presenter_1.position.x, button_presenter_1.position.y
        -3.0 0.0
        >>> print button_presenter_2.position.x, button_presenter_2.position.y
        0.0 0.0
    """

    def __init__(self, layout_manager, position = None):

        Widget.__init__(self, position)

        self._size = obengine.math.Vector2D()
        self._layout_manager = layout_manager(self)
        self.children = set()

        self.on_position_changed += self._update_layout
        self.on_hidden += self._hide_children
        self.on_shown += self._show_children

    def add(self, widget):

        widget.parent = self
        widget.position = self._layout_manager.find_space_for_widget(widget)

        self.children.add(widget)

        self._layout_manager.adjust_widgets_after_add(widget)
        self._layout_manager.adjust_size(self._size)

    def remove(self, widget):

        self.children.remove(widget)
        widget.parent = None

        self._layout_manager.adjust_widgets_after_remove(widget)
        self._layout_manager.adjust_size(self._size)

    @property
    def size(self):
        return self._size

    def _update_layout(self, new_pos):
        self._layout_manager.update_widgets_after_move(new_pos)

    def _show_children(self):
        for child in self.children:
            child.showing = True

    def _hide_children(self):
        for child in self.children:
            child.showing = False


class VerticalLayoutManager(object):
    
    def __init__(self, owning_container):
        self._owning_container = owning_container
        
    def find_space_for_widget(self, widget):
        
        best_point = obengine.math.Vector2D(self._owning_container.position.x, 0)
        
        for child_widget in self._owning_container.children:
            best_point.y += child_widget.size.y / 2.0

        if len(self._owning_container.children) > 0:

            best_point.y += widget.size.y / 2.0
            best_point.y += PAD_SPACE

        return best_point
        
    def adjust_widgets_after_add(self, new_widget):

        new_widget_y = new_widget.position.y

        for child_widget in self._owning_container.children:
            child_widget.position.y -= new_widget_y
            
    def adjust_widgets_after_remove(self, removed_widget):

        removed_widget_y = removed_widget.position.y

        for child_widget in self._owning_container.children:
            child_widget.position.y += removed_widget_y

    def adjust_widgets_after_move(self, new_pos):

        for child_widget in self._owning_container.children:
            
            child_widget.y += new_pos.y - child_widget.y
            child_widget.x += new_pos.x - child_widget.x
            
    def adjust_size(self, size):
        
        size.y = sum(map(lambda w: w.size.y + PAD_SPACE, self._owning_container.children))
        size.x = max(map(lambda w: w.size.x, self._owning_container.children))


class HorizontalLayoutManager(object):

    def __init__(self, owning_container):
        self._owning_container = owning_container

    def find_space_for_widget(self, widget):

        best_point = obengine.math.Vector2D(0, self._owning_container.position.y)

        for child_widget in self._owning_container.children:
            best_point.x += child_widget.size.x / 2.0

        if len(self._owning_container.children) > 0:

            best_point.x += widget.size.x / 2.0
            best_point.x += PAD_SPACE

        return best_point

    def adjust_widgets_after_add(self, new_widget):

        new_widget_x = new_widget.position.x

        for child_widget in self._owning_container.children:
            child_widget.position.x -= new_widget_x

    def adjust_widgets_after_remove(self, removed_widget):

        removed_widget_x = removed_widget.position.x

        for child_widget in self._owning_container.children:
            child_widget.position.x += removed_widget_x

    def adjust_widgets_after_move(self, new_pos):

        for child_widget in self._owning_container.children:

            child_widget.y += new_pos.y - child_widget.y
            child_widget.x += new_pos.x - child_widget.x

    def adjust_size(self, size):

        size.x = sum(map(lambda w: w.size.x + PAD_SPACE, self._owning_container.children))
        size.y = max(map(lambda w: w.size.y, self._owning_container.children))