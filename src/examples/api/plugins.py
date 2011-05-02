# Plugins example - shows how to load plugins, and demos
# the automagic dependency handler

import sys
import os

# Necessary to find the obengine package
sys.path.append(os.path.join(os.pardir, os.pardir))

import obengine
import obengine.plugin

def found_plugin(root_dir):
	print 'found plugin %s' % root_dir

def initialized_plugin(plugin):
	print 'loaded plugin from file %s' % plugin.module.__file__

# Set up all the modules we've imported - even sets up implicit/nested dependencies!
obengine.init()

manager = obengine.plugin.PluginManager()

manager.on_plugin_found += found_plugin
manager.on_plugin_initialized += initialized_plugin

manager.find_plugins()
manager.initialize_all_plugins()
