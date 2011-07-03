#
# This module provides a simple way of representing an OpenBlox plugin.
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
__date__  = "$Jun 2, 2011 1:03:00 AM$"


import sys


class Plugin(object):
    """
    Represents a loaded plugin.
    This is mostly an class that should just be used by PluginManager,
    though there could be other uses.
    """

    def __init__(self, name, root_module, root_dir, provides, requires = []):
        """
        Arguments:
         * name - the name of this plugin
         * root_module - the Python module to import; it must be inside root_dir
         * root_dir - the path (absolute or relative) to the directory containing the plugin's plugin.ini file
         * provides - the list of facilites (virtual plugins) that this plugin provides
         * requires - the list of plugins (possibly virtual) that this plugin
                      requires to run
        """

        self.name = name
        self.root_module = root_module
        self.root_dir = root_dir
        self.provides = provides
        self.requires = requires

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
