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
__date__ ="$May 2, 2011 1:38:18 AM$"

import sys
import atexit
from sys import _getframe as getframe


import inspect
import modulefinder

collected_modules = []
dependency_map = {}

def gendeps(modname = None, prefix = 'obengine', excludes=[]):
    """
    Use this function to record your module's dependencies.
    Call it like this at the start of your module::
        depman.gendeps(prefix = your_root_packages_name)

    If you want to exclude some modules for some reason, call it like this::
        depman.gendeps(excludes=['some.excluded.module', 'some.other_excluded.module'])

    You can ignore the other parameters; they're there for recursive calling purposes only.
    """

    package = prefix
    name = modname or getframe(1).f_globals['__name__']

    excludes.append('obengine')

    # Have we visited a module that we aren't supposed to?
    if not name.startswith(package):
        return

    # Have we already covered this module?
    if name in collected_modules:
        return

    # Have we been instructed not to consider this module:
    if name in excludes:
        return

    # We don't check ourselves!
    if name == __name__:
        return

    # Record this module, and initialize its dependency map

    collected_modules.append(name)
    dependency_map[name] = []

    # Has this module already been imported?
    # If not, we need to import it, so we can see what it depends upon

    if name not in sys.modules:
        __import__(name, globals(), locals())

    # Provide a global variable named deps to every module that
    # utilizes depman
    sys.modules[name].deps = []

    # Provide a short alias for the global variable deps inside the
    # module we're examining
    deps = sys.modules[name].deps

    # Find all the modules that the module we're examining imports
    module_finder = modulefinder.ModuleFinder()
    module_finder.run_script(inspect.getsourcefile(sys.modules[name]))

    for dependency_name in module_finder.modules.keys():

        # Is this dependency inside the same package as the module we're
        # currently examining?

        if dependency_name.startswith(package) and dependency_name != name:
            
            # Quick check to make sure we don't add ourselves!
            if dependency_name not in ['depman', 'modulefinder']:

                # This is a valid dependency, so go ahead and record it

                deps.append(dependency_name)
                dependency_map[name].append(dependency_name)

                # Also, generate its dependencies with a recursive call

                gendeps(dependency_name, package, excludes)

def _cmp_modules(module1, module2):

    # Does module2 depend upon module1?
    if module1 in dependency_map.get(module2, []):

        # Then module1 should be initalized first
        return -1

    # Then, does module1 depend on module2?
    elif module2 in dependency_map.get(module1, []):

        # In that case, module2 should be initalized first
        return 1

    # They don't depend on each other - either one goes
    else:
        return 0

def init():
    """
    Call this to initialize all modules that support depman.
    This function also deinitalizes all modules (if they request it) upon program exit.
    """

    errors = []

    collected_modules.sort(_cmp_modules)

    # Run over all the modules we collected

    for module_name in collected_modules:

        # Get each module's dependency map
        module_dependencies = dependency_map.get(module_name, [])

        # Run over all of said module's dependencies
        for module_dependency in module_dependencies:

            # And here's here all the magic comes to a focus:
            # We check to see if the module we're currently examining
            # is in the dependency map of one of its dependencies.
            # If it is, then that means we have a circular dependency.
            if module_name in dependency_map.get(module_dependency, []):

                # Let's check to make sure we haven't already sent a warning
                # about this
                if module_dependency != module_name:

                    if module_dependency + module_name not in errors:
                        
                        if module_name + module_dependency not in errors:

                            print >> sys.stderr, 'Circular dependency between %s and %s' % (module_name, module_dependency)
                            errors.append(module_name + module_dependency)

    # We just finished checking for circular dependencies, so now,
    # we can set up all the modules

    for module in collected_modules:

        # Get the actual module, instead of the name
        module = sys.modules[module]

        # Initalize this module
        # Since we iterate over modules closer to their
        # respective package's root, we know packages higher up the
        # package tree are properly initalized.
        # Pretty neat, huh?
        if hasattr(module, 'init'):
            module.init()

        # Another neat trick. atexit seems to store functions to be called on program
        # exit as a list, and every atexit.register call invokes list.append.
        # So, this means functions are called on a first-come, first-served
        # basis: the sooner they're call atexit.register, the sooner atexit.register
        # calls them, which perfectly coincides with the way we store collected
        # modules!
        elif hasattr(module, 'deinit'):
            atexit.register(module.deinit)