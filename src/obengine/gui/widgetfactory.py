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


import obengine.plugin
import obengine.depman

from obengine.gui import GuiException

from button import *
from radio import *
from checkbox import *
from container import *
from shutter import *
from label import *
from entry import *
from pulldown import *
from scrolledlist import *

obengine.depman.gendeps()


def init():
    obengine.plugin.require('core.gui')


class WidgetFactory(object):
    """A factory for making widgets.
    """

    def __init__(self):

        self._widget_handlers = {}

        self._widget_handlers['button'] = self._make_button
        self._widget_handlers['radio'] = self._make_radio
        self._widget_handlers['checkbox'] = self._make_checkbox

        self._widget_handlers['container'] = self._make_container
        self._widget_handlers['shutter'] = self._make_shutter
        self._widget_handlers['menu'] = self._make_menu
        self._widget_handlers['pulldown'] = self._make_pulldown
        self._widget_handlers['scrolledlist'] = self._make_scrolledlist

        self._widget_handlers['label'] = self._make_label
        self._widget_handlers['entry'] = self._make_entry


    def make(self, widget_type, *args, **kwargs):

        try:
            factory_handler = self._widget_handlers[widget_type]

        except KeyError:
            raise UnknownWidgetError(widget_type)

        return factory_handler(*args, **kwargs)

    def _make_button(self, text, position = None, icon = None):

        import obplugin.core.gui

        model = Button(text, position, icon)
        view = obplugin.core.gui.ButtonView(text, position, icon)
        presenter = ButtonPresenter(model, view)

        return presenter

    def _make_radio(self, text, position = None):

        import obplugin.core.gui

        model = Radio(text, position)
        view = obplugin.core.gui.RadioView(text, position)
        presenter = RadioPresenter(model, view)

        return presenter

    def _make_checkbox(self, text, position = None):

        import obplugin.core.gui

        model = Checkbox(text, position)
        view = obplugin.core.gui.CheckboxView(text, position)
        presenter = CheckboxPresenter(model, view)

        return presenter

    def _make_container(self, layout_manager = VerticalLayoutManager, position = None, margin = None):

        container = Container(layout_manager, position, margin)
        return container

    def _make_shutter(self, layout_manager = HorizontalLayoutManager, position = None, margin = None):
        
        import obplugin.core.gui

        model = Shutter(layout_manager, position, margin)
        view = obplugin.core.gui.ShutterView(position)
        presenter = ShutterPresenter(model, view)

        return presenter

    def _make_scrolledlist(self, position = None):

        import obplugin.core.gui

        model = ScrolledList(position)
        view = obplugin.core.gui.ScrolledListView(position)
        presenter = ScrolledListPresenter(model, view)

        return presenter

    def _make_label(self, text, position = None):

        import obplugin.core.gui

        model = Label(text, position)
        view = obplugin.core.gui.LabelView(text, position)
        presenter = LabelPresenter(model, view)

        return presenter
    
    def _make_entry(self, initial_text = '', position = None):
        
        import obplugin.core.gui
        
        model = Entry(initial_text, position)
        view = obplugin.core.gui.EntryView(initial_text, position)
        presenter = EntryPresenter(model, view)
        
        return presenter

    def _make_pulldown(self, initial_text = '', position = None):

        button = self.make('button', initial_text, position)
        container = self.make('container')
        pulldown = Pulldown(button, container)

        return pulldown

    def _make_menu(self, text, position = None):
        raise NotImplementedError('Menu support in OpenBlox is not finished')


class UnknownWidgetError(GuiException):
    pass