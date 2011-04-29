import sys
import os

sys.path.append(os.path.join(os.pardir, os.pardir))

import obengine.cfg
import obengine.plugin

def found_plugin(root_dir):
	print 'found plugin %s' % root_dir

def loaded_plugin(plugin):
	print 'loaded plugin from file %s' % plugin.module.__file__

obengine.cfg.init()

manager = obengine.plugin.PluginManager()

manager.on_plugin_found += found_plugin
manager.on_plugin_loaded += loaded_plugin

manager.find_plugins()
manager.load_all_plugins()
