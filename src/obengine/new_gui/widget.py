#
# <module description>
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
#
# Copyright (C) 2012 The OpenBlox Project
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
__date__ = "Jun 9, 2012 10:15:20 PM"


import ConfigParser

import obengine.datatypes
import obengine.event
import obengine.cfg
import obengine.math
import obengine.vfs
import obengine.plugin
import obengine.depman

obengine.depman.gendeps()


def init():

    theme_location = obengine.cfg.Config().get_str('cfgdir') + '/data/themes'
    obengine.vfs.mount('/themes', obengine.vfs.RealFS(theme_location))

    obengine.plugin.require('core.gui')


def set_theme(theme):
    ThemeManager.theme = theme


def get_current_theme():
    return ThemeManager.theme


def add_theme_search_path(path):
    ThemeManager.theme_search_path.insert(0, path)


class ThemeManager(object):

    _theme = None
    theme_search_path = ['/themes']
    THEME_IMAGE_EXTENSION = '.png'
    THEME_INFO_FILE = 'theme.ini'

    @classmethod
    def get_theme(cls):

        if cls._theme is None:
            cls.theme = 'default'

        return cls._theme

    @classmethod
    def set_theme(cls):

        import obplugin.core.gui

        theme_path = cls._vfs_path_to_theme(theme)
        font_path = obengine.vfs.join(theme_path, 'fonts')
        fonts = obengine.vfs.listdir(font_path)

        for font in fonts:
            obplugin.core.gui.load_font(obengine.vfs.getsyspath(obengine.vfs.join(font_path, font)))

        cls._theme = theme

    @classmethod
    def get_theme_info(cls, theme):

        base_theme_path = cls.vfs_path_to_current_theme()
        theme_cfg_path = obengine.vfs.join(base_theme_path, cls.THEME_INFO_FILE)

        theme_cfg_parser = ConfigParser.ConfigParser()
        theme_cfg_parser.read(obengine.vfs.getsyspath(theme_cfg_path))
        return dict(theme_cfg_parser.items('theme'))

    @classmethod
    def vfs_path_to_current_theme(cls):
        return cls._vfs_path_to_theme(cls.theme)

    @classmethod
    def get_image_for(cls, widget, state):

        theme_path = cls.vfs_path_to_current_theme()
        widget_specific_path = obengine.vfs.join(theme_path, 'widgets', widget, state + cls.THEME_IMAGE_EXTENSION)

        if obengine.vfs.exists(widget_specific_path):
            return obengine.vfs.getsyspath(widget_specific_path)

        else:

            default_widget_state_image = obengine.vfs.join(theme_path, 'widgets', 'default', state + cls.THEME_IMAGE_EXTENSION)
            assert obengine.vfs.exists(default_widget_state_image)
            return default_widget_state_image

    @classmethod
    def _vfs_path_to_theme(cls, theme):

        for possible_theme_path in cls.theme_search_path:

            vfs_path = obengine.vfs.join(possible_theme_path, theme)

            if obengine.vfs.exists(vfs_path):
                return vfs_path


class WidgetBase(object):

    states = ['normal', 'highlight', 'clicked', 'disabled']

    def __init__(self, widget_type, view):

        self._widget_type = widget_type
        self._view = view

        for state in self.states:
            self._configure_state(state)

    @property
    def view(self):
        return self._view

    def _configure_state(self, state):

        image = self._get_image_for(self._widget_type, state)
        self.view.set_image_for_state(state, image)

    def _get_image_for(self, widget_type, state):
        return ThemeManager.get_image_for(widget_type, state)


class Widget(WidgetBase):

    def __init__(self, widget_type, parent, view):

        WidgetBase.__init__(self, widget_type, view)

        self._parent = parent

        self._showing = True
        self.on_hidden = obengine.event.Event()
        self.on_shown = obengine.event.Event()

    @property
    def parent(self):
        return self._parent

    @property
    def view(self):
        return self._view

    @obengine.datatypes.nested_property
    def showing():

        def fget(self):
            return self.view.showing

        def fset(self, showing):

            old_showing = self.showing
            self.view.showing = showing

            if self.showing is True and old_showing is False:
                self.on_shown()

            elif self.showing is False and old_showing is True:
                self.on_hidden()

        return locals()


class ClickableWidget(Widget):

    def __init__(self):

        self.on_click = obengine.event.Event()

        self.view.on_click += self.on_click
        self.on_hidden += self.on_click.disable
        self.on_shown += self.on_click.enable


class TextWidget(Widget):

    def __init__(self, text):

        self._text = text
        self.on_text_changed = obengine.event.Event()

    @obengine.datatypes.nested_property
    def text():

        def fget(self):
            return self.view.text

        def fset(self, new_text):

            self.view.text
            self.on_text_changed(new_text)

        return locals()


class TopLevelWidget(WidgetBase):

    def __init__(self, position, widget_type, view):

        WidgetBase.__init__(self, widget_type, view)

        self.view.position = position or obengine.math.Vector2D()
        self.on_position_changed = obengine.event.Event()

        self.view.showing = True
        self.on_shown = obengine.event.Event()
        self.on_hidden = obengine.event.Event()

        self._children = set()

    def add(self, widget):

        widget.parent = self
        self._children.add(widget)

    def remove(self, widget):

        self._children.remove(widget)
        widget.parent = None

    @property
    def view(self):
        return self._view

    @obengine.datatypes.nested_property
    def showing():

        def fget(self):
            return self.view.showing

        def fset(self, showing):

            old_showing = self.showing
            self.view.showing = showing

            if self.showing is True and old_showing is False:
                self.on_shown()

            elif self.showing is False and old_showing is True:
                self.on_hidden()

        return locals()

    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return self.view.position

        def fset(self, position):
            self.view.position = position

        return locals()

    def __contains__(self, item):
        return item in self._children
