#
# This module implements an extensible widget factory.
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
__date__  = "$Jun 16, 2011 12:00:53 AM$"


from obengine.gui import *


class WidgetFactory(object):
    """A factory for making widgets.
    Example:
        >>> w = WidgetFactory()
        >>> m = w.make('menu', 'A test menu!')
    """

    def __init__(self):

        self._widget_handlers = {}

        self._widget_handlers['button'] = self._make_button
        self._widget_handlers['menu'] = self._make_menu

    def make(self, widget_type, *args, **kwargs):

        try:
            factory_handler = self._widget_handlers[widget_type]

        except KeyError:
            raise UnknownWidgetError(widget_type)

        return factory_handler(*args, **kwargs)

    def _make_button(self, text, position = None, icon = None):

        model = Button(text, position, icon)
        view = MockButtonView(text, position, icon)
        presenter = ButtonPresenter(model, view)

        return presenter

    def _make_menu(self, text, position = None, **kwargs):

        menu_button = self.make('button', text, position)
        model = Menu(menu_button, position, **kwargs)
        return model


class UnknownWidgetError(GuiException):
    pass