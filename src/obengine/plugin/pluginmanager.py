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
import obengine.log
import obengine.datatypes
import obengine.event
import obengine.depman

from obengine.plugin.importhook import PluginImportHook

obengine.depman.gendeps()

PLUGIN_CFG_NAME = 'plugin.ini'

def init():
    sys.meta_path.append(PluginImportHook(PluginManager()))

def require(plugin_name):
    """Checks if a virtual plugin is implemented
    Wrapper around PluginManager, to check if a plugin (given by plugin_name) is currently loaded.
    If not, it attempts to load an implementation of said plugin, throwing PluginNotFoundException if the operation fails.

    Call this function at the start of your module, for every plugin your module requires.
    *If* the plugins are available, require will load them. Otherwise, require will raise PluginNotFoundException.
    """

    pm = PluginManager()

    if plugin_name not in pm.provided_plugins():

        plugin = pm.find_plugin(plugin_name)
        plugin = pm.load_plugin(plugin)
        pm.initialize_plugin(plugin)


class Plugin(object):
    """
    Represents a loaded plugin.
    This is mostly an class that should just be used by PluginManager,
    though there could be other uses.
    """

    def __init__(self, name, root_module, root_dir, provides):
        """
        Arguments:
         * name - the name of this plugin
         * root_module - the Python module to import; it must be inside root_dir
         * root_dir - the path (absolute or relative) to the directory containing the plugin's plugin.ini file
         * provides - the list of facilites (virtual plugins) that this plugin provides.
        """

        self.name = name
        self.root_module = root_module
        self.root_dir = root_dir
        self.provides = provides

    def load(self):
        """
        Loads this plugin; adds the root module to sys.modules,
        and adds this plugin as the implementation for all the virtual plugins it provides.
        """

        # Add the root directory, so we can easily import the root module
        sys.path.insert(0, self.root_dir)

        __import__(self.root_module, globals(), locals())

        self.module = sys.modules[self.root_module]

        # Remove the root directory of this plugin, so we don't pollute sys.path
        sys.path.pop(0)
        
    def init(self):

        # Merely delegate to the root module

        if hasattr(self.module, 'init'):
            self.module.init()

class PluginManager(object):
    """
    Simple plugin manager framework.

    Events:
    * on_plugin_found - gives the root directory of the found plugin
    * on_plugin_initalized - gives the actual module of the initalized plugin
    """

    search_path = None
    plugins = []
    on_plugin_found = obengine.event.Event()
    on_plugin_initialized = obengine.event.Event()
    _logger = obengine.log.Logger()

    def __init__(self, search_path = None):
        """
        Arguments:
        * search_path (optional) - the path to search for plugins. If not given, OPENBLOX_DIR/plugins is used
        """

        self._config_src = obengine.cfg.Config()

        if self.search_path is None:
            self.search_path = search_path or os.path.join(self._config_src.get_str('cfgdir'), 'plugins')

        elif search_path is not None:
            self.search_path = search_path or os.path.join(self._config_src.get_str('cfgdir'), 'plugins')

    def find_plugin(self, name):
        """
        Finds a plugin, with a given name.
        Arguments:
         * name - name of the plugin to find
        Returns:
        The root directory of the plugin with the given name; None, if no such plugin was found.
        """


        for root_dir, child_dirs, files in os.walk(self.search_path):

            if PLUGIN_CFG_NAME in files:

                if name in self._parse_plugin_dir(root_dir).provides:
                    return root_dir

        raise PluginNotFoundException(name)

    def load_plugin(self, root_dir):
        """
        Loads a plugin. The name is slightly misleading, as the plugin is not acutally initalized,
        just put in the initialization queue.
        Arguments:
        * root_dir - the root directory of the plugin to load
        """

        self._logger.debug('Loading plugin from directory %s' % root_dir)
        self.on_plugin_found(root_dir)

        plugin = self._parse_plugin_dir(root_dir)
        plugin.load()

        self.add_plugin(plugin)
        return plugin

    def initialize_plugin(self, plugin):
        
        self._logger.debug('Initalizing plugin %s' % plugin.name)
        
        plugin.init()
        self.on_plugin_initialized(plugin)

        self._logger.info('Plugin %s initalized' % plugin.name)


    def all_plugins(self):
        """
        A generator, that yields every found plugin.
        Returns:
        A generator, containing all found plugins, represented as instances of Plugin.
        """

        for plugin in self.plugins:
            yield plugin

    def provided_plugins(self):
        """
        A generator that yields all provided virtual plugin names.
        """

        for plugin in self.all_plugins():

            for provision in filter(lambda p: p != ['none'], plugin.provides):
                yield provision

    def all_plugin_names(self):
        """
        A generator that yields the names of all currently loaded (not neccessarily initalized!) plugins.
        """

        for plugin in self.all_plugins():
            yield plugin.name

    def add_plugin(self, plugin):
        self.plugins.append(plugin)

    def _parse_plugin_dir(self, root_dir):

        parser = ConfigParser.ConfigParser()
        parser.read(os.path.join(root_dir, PLUGIN_CFG_NAME))

        name = parser.get('core', 'name')
        module = parser.get('core', 'module')
        provides = self._get_optional_split_option(parser, 'core', 'provides', ['none'], ',')

        plugin = Plugin(name, module, root_dir, provides)
        return plugin

    def _get_optional_option(self, config_parser, section, option, default = None):
        return config_parser.has_option(section, option) and config_parser.get(section, option) or default

    def _get_optional_split_option(self, config_parser, section, option, default = None, splitter = ' '):

        val = self._get_optional_option(config_parser, section, option, default)

        if val != default:
            val = val.split(splitter)

        return val

class PluginConflictException(Exception):
    """
    Raised when two conflicting plugins (two graphics front-ends, for example) are loaded.
    """

class PluginNotFoundException(Exception):
    """
    Raised when a requested/required plugin isn't found.
    """