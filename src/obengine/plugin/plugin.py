# obengine.plugin.plugin
# ======================
#
# Provides a simple method of OO-izing a plugin.
#
# Copyright (C) 2011 The OpenBlox Project
# License: GNU GPL v3
#
# See <TODO: No Sphinx docs yet - add some!> for the primary source of documentation
# for this module.

__author__ = "openblocks"
__date__  = "$Jun 2, 2011 1:03:00 AM$"

import sys

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