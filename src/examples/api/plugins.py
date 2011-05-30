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

def main():

   # Necessary to find the configuration file (example-specific; you don't have to do this unless you want to use a custom configuration file;
   # or your user doesn't have OpenBlox installed)
   obengine.cfg.Config().load(os.path.join(os.pardir, os.pardir, 'obconf.cfg'))

   # Set up all the modules we've imported - even sets up implicit/nested dependencies!
   obengine.init()

   manager = obengine.plugin.PluginManager()

   manager.on_plugin_found += found_plugin
   manager.on_plugin_initialized += initialized_plugin

   # Load the scripting plugin
   obengine.plugin.require('core.scripting')

   # Load the graphics plugin
   obengine.plugin.require('core.graphics')

   # Load the physics plugin
   obengine.plugin.require('core.physics')

   # The output if you're on *nix should look like the following:
   #
   # found plugin <some path>plugins/lupa-scripting
   # loaded plugin from file <some path>plugins/lupa-scripting/lupa_backend.pyc
   # found plugin <some path>/plugins/panda-backend/panda-graphics
   # loaded plugin from file <some path>/plugins/panda-backend/panda-graphics/panda_graphics.pyc
   # found plugin <some path>/plugins/panda-backend/panda-physics
   # loaded plugin from file <some path>/plugins/panda-backend/panda-physics/panda_physics.pyc

if __name__ == '__main__':
   main()
