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
import obengine.utils
import obengine.event

PLUGIN_CFG_NAME = 'plugin.ini'

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
         * provides - the list of facilites (virtual plugins) that this plugin provides
        """

        self.name = name
        self.root_module = root_module
        self.root_dir = root_dir
        self.provides = provides

    def load(self):
        """
        Loads this plugin; adds the root module to sys.modules,
        and adds this plugin as the implementation for all the virtual plugins it provides
        """

        # Add the root directory, so we can easily import the root module
        sys.path.insert(0, self.root_dir)

        __import__(self.root_module, globals(), locals())

        self.module = sys.modules[self.root_module]

        # Does this plugin provide any facilites (virtual plugins)?
        if self.provides != ['none']:
        
            for provision in self.provides:

                # Set ourselves as the implementation of each virtual plugin we provide
                sys.modules[provision] = self.module

        # Remove the root directory of this plugin, so we don't pollute sys.path
        sys.path.pop(0)
        
    def init(self):

        # Merely delegate to the root module
        self.module.init()

class PluginManager(object):
    """
    Simple plugin manager framework.

    Events:
     * on_plugin_found - gives the root directory of the found plugin
     * on_plugin_loaded - gives the actual module of the loaded plugin

    See the dummy plugin (in plugins/dummy-plugin) to see how to write an actual plugin.
    """

    def __init__(self, search_path = None):
        """
        Arguments:
         * search_path (optional) - the path to search for plugins. If not given, OPENBLOX_DIR/plugins is used
        """

        self.search_path = search_path or os.path.join(obengine.cfg.get_config_var('cfgdir'), 'plugins')

        # Various events, for extensibilty purposes
        self.on_plugin_found = obengine.event.Event()
        self.on_plugin_loaded = obengine.event.Event()

        self.plugins = []

    def find_plugins(self):
        """
        Finds all plugins under the set search path, and sets them up to be loaded.
        Note that conflicting plugins are not checked at this stage!
        """

        # Find every plugin under our search path

        for root_dir, child_dirs, files in os.walk(self.search_path):

            # Does this directory constitute a valid plugin?
            
            if PLUGIN_CFG_NAME in files:
                self.load_plugin(root_dir)

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

                if name in self.parse_plugin_dir(root_dir):
                    return root_dir

    def load_plugin(self, root_dir):
        """
        Loads a plugin. The name is slightly misleading, as the plugin is not acutally initalized,
        just put in the initialization queue.
        Arguments:
         * root_dir - the root directory of the plugin to load
        """

        self.on_plugin_found(root_dir)
        self.parse_plugin_dir(root_dir)

    def load_all_plugins(self, exclusion_list = []):
        """
        Initalizes all found plugins.
        Arguments:
         * exclusion_list - if given, specifies plugins to not load
        """

        for plugin in filter(lambda p: p.name not in exclusion_list, self.plugins):

            plugin.load()
            plugin.init()
            self.on_plugin_loaded(plugin)

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

    def parse_plugin_dir(self, root_dir):
        """
        Parses a plugin, and adds it to the initialization queue.

        Arguments:
         * root_dir - the root directory of the plugin to be parsed

        Returns:
        The list of virtual plugins the newly loaded plugin provides
        """

        parser = ConfigParser.ConfigParser()
        parser.read(os.path.join(root_dir, PLUGIN_CFG_NAME))

        module = parser.get('core', 'module')
        name = parser.get('core', 'name')
        provides = self._get_optional_split_option(parser, 'core', 'provides', ['none'])
        depends = self._get_optional_split_option(parser, 'core', 'depends', ['none'])
        conflicts = self._get_optional_split_option(parser, 'core', 'conflicts', ['none'], ',')

        for possible_conflict in conflicts:

            if possible_conflict in self.provided_plugins() or possible_confict in self.all_plugin_names:

                message = 'Conflict between %s and %s' % (name, possible_confict)
                obengine.utils.critical(message)
                raise PluginConflictError(message)

        if depends != ['none']:

            for dependency in depends:

                if dependency in self.provided_plugins():
                    continue

                self.load_plugin(self.find_plugin(dependency))

        plugin = Plugin(name, module, root_dir, provides)

        self.plugins.append(plugin)

        return provides

    def _get_optional_option(self, config_parser, section, option, default = None):
        return config_parser.has_option(section, option) and config_parser.get(section, option) or default

    def _get_optional_split_option(self, config_parser, section, option, default = None, splitter = ' '):

        val = self._get_optional_option(config_parser, section, option, default)

        if val != default:
            val = val.split(splitter)

        return val

class PluginConfictException(Exception):
    """
    Raised when two conflicting plugins (two graphics front-ends, for example) are loaded.
    """