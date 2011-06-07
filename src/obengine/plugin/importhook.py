#
# This module provides an import hook to easily use OpenBlox plugins.
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
__date__ = "$May 2, 2011 9:09:42 AM$"


import types


PLUGIN_MODULE = 'obplugin'


class PluginImportHook(object):
    """
    Import hook for plugins.
    To use, simply append an instance of this class to sys.meta_path.
    Now, you can access plugins as if they were normal modules, like this:

        # To import the loaded scripting plugin:
        import obplugin.core.scripting

        # To import the loaded graphics plugin:
        import obplugin.core.graphics

    All plugins are under the module(s) obplugin.<virtual plugin implementation>.
    """

    def __init__(self, plugin_manager):

        self.plugin_manager = plugin_manager

        # Make our trick module
        self.obplugin = types.ModuleType(PLUGIN_MODULE)
        self.obplugin.__path__ = []

    def find_module(self, fullname, _):

        # Is this the initial call to find_module?
        if fullname == 'obplugin':

            # Set us up to be called again
            return self

        # We're now looking for a plugin
        if fullname.startswith('obplugin'):

            for plugin_name in self.plugin_manager.provided_plugins():

                # Check to see if there's a least 1 plugin that is a superset of
                # the given name
                
                if plugin_name.startswith(fullname[len(PLUGIN_MODULE) + 1:]):
                    return self

        # No matches?
        return None

    def load_module(self, fullname):

        # The initial call to load_module?
        if fullname == 'obplugin':
            return self.obplugin

        # Is this not the initial call to load_module, but no plugins match the given name?
        elif fullname.startswith('obplugin') and fullname[len(PLUGIN_MODULE) + 1:] not in self.plugin_manager.provided_plugins():

            # We're probably just looking at a category, so return our dummy module and try again
            return self.obplugin

        # There's a plugin that matches the given name!
        for plugin in self.plugin_manager.all_plugins():

            if fullname[len('obplugin.'):] in plugin.provides:
                return plugin.module

        # Normally, this won't be reached. Just in case, though...
        raise ImportError
