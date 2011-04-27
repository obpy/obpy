"""
Copyright (C) 2011 The OpenBlox Project

This file is part of The OpenBlox Game Engine.

    The OpenBlox Game Engine is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    The OpenBlox Game Engine is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with The OpenBlox Game Engine.  If not, see <http://www.gnu.org/licenses/>.

"""

__author__="openblocks"
__date__ ="$Apr 27, 2011 3:22:28 PM$"

import os
import sys
import ConfigParser

import obengine.cfg
import obengine.event

PLUGIN_CFG_NAME = 'plugin.ini'

class PluginManager(object):
    """
    Simple plugin manager framework.

    Events:
     * on_plugin_found - gives the root directory of the found plugin
     * on_plugin_loaded - gives the actual module of the loaded plugin

    See the dummy plugin (in plugins/dummy-plugin) to see how to write an actual plugin.
    """

    def __init__(self):

        self.search_path = os.path.join(obengine.cfg.get_config_var('cfgdir'), 'plugins')

        self.on_plugin_found = obengine.event.Event()
        self.on_plugin_loaded = obengine.event.Event()

        self.plugins = []

    def find_plugins(self):

        for root_dir, child_dirs, files in os.walk(self.search_path):

            if PLUGIN_CFG_NAME in files:

                self.on_plugin_found(root_dir)
                self.parse_plugin_dir(root_dir)

    def load_all_plugins(self):

        for plugin in self.plugins:

            plugin.init()
            self.on_plugin_loaded(plugin)

    def parse_plugin_dir(self, root_dir):

        parser = ConfigParser.ConfigParser()
        parser.read(os.path.join(root_dir, PLUGIN_CFG_NAME))

        location = parser.get('core', 'module')
        provides = parser.has_option('core', 'provides') and parser.get('core', 'provides').split() or ['none']

        sys.path.insert(0, root_dir)

        __import__(location, globals(), locals())

        plugin = sys.modules[location]

        for provision in filter(lambda name: name != 'none', provides):
            sys.modules[provision] = plugin

        sys.path.pop(0)

        self.plugins.append(plugin)

    @property
    def search_path(self):
        return self._search_path

    @search_path.setter
    def search_path(self, path):
        self._search_path = path