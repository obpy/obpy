# Plugin import hook example - shows how to use the plugin import hook

import sys
import os

# Necessary to find the obengine package
sys.path.append(os.path.join(os.pardir, os.pardir))

import obengine
import obengine.cfg
import obengine.plugin


def found_plugin(root_dir):
	print 'found plugin %s' % root_dir


def initialized_plugin(plugin):
	print 'loaded plugin from file %s' % plugin.module.__file__


def main():

   # Necessary to find the configuration file (example-specific; you don't have
   # to do this unless you want to use a custom configuration file;
   # or your user doesn't have OpenBlox installed)

   obengine.cfg.Config().load(os.path.join(os.pardir, os.pardir, 'obconf.cfg'))
   
   obengine.init()
   
   manager = obengine.plugin.PluginManager()
   
   manager.on_plugin_found += found_plugin
   manager.on_plugin_initialized += initialized_plugin
   
   ################## END OF STOCK EXAMPLE CODE ##################

   # Here's something new: We request that an implementation of core.scripting
   # be loaded and initialized, if it isn't already.
   
   obengine.plugin.require('core.scripting')

   # It looks like a normal import - but it's not!
   # Take a look - there's no obplugin directory anywhere.
   # So how can we import something that doesn't exist?
   # Through an import hook of course! Import hooks allow you
   # to import packages and modules that don't even exist on the file system,
   # or on/through mediums from which you normally can't import (like HTTP or FTP).

   import obplugin.core.scripting

   # The rest is trivial: Set up a scripting engine (see scripting.py for more on that),
   # create a function, and execute it from Python

   scripting_engine = obplugin.core.scripting.ScriptEngine()
   scripting_engine.execute('function hello() print("Hello from Lua!"); end')
   scripting_engine.method.hello()

   # The output from this script should be the following if you're on Linux or Mac OSX:

   # found plugin ../../plugins/lupa-scripting
   # loaded plugin from file ../../plugins/lupa-scripting/lupa_backend.pyc
   # Hello from Lua!

   # If you're on Windows, it'll look like this:

   # found plugin ..\..\plugins\lupa-scripting
   # loaded plugin from file ..\..\plugins\lupa-scripting\lupa_backend.pyc
   # Hello from Lua!

if __name__ == '__main__':
      main()
