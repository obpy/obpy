#
# This module provides "auto-magic" dependency handling/(de)initialization facilites.
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
#
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
__date__  = "$May 2, 2011 1:38:18 AM$"


import sys
import atexit
from sys import _getframe as getframe


collected_modules = []


def gendeps(modname = None):
    """
    Use this function to record your module's dependencies.
    Call it like this at the start of your module (after all your imports -
    this is crucial):
        obengine.depman.gendeps()
    """

    # This may not seem like much, but the reason why this algorithm works
    # is very simple:
    # Each module that supports obengine.depman has a call to this method (gendeps)
    # AFTER all of its imports. This way, modules lower down "the import chain"
    # will have their gendeps call evaluated before the more dependent modules.
    # This results in the least-dependent modules being added to collected_modules
    # before the more-dependent modules.

    name = modname or getframe(1).f_globals['__name__']
    collected_modules.append(name)


def init():
    """
    Call this to initialize all modules that support depman.
    This function also deinitalizes all modules (if they request it) upon program exit.
    """

    for module in collected_modules:

        # Get the actual module, instead of the name
        module = sys.modules[module]

        # Initalize this module, if it needs to be
        
        if hasattr(module, 'init'):
            module.init()
        
        # Another neat trick. atexit seems to store functions to be called on program
        # exit as a list, and every atexit.register call invokes list.append.
        # So, this means functions are called on a first-come, first-served
        # (i.e, FIFO) basis: the sooner they're given to atexit.register,
        # the sooner atexit.register calls them, which perfectly coincides with
        # the way we store collected modules!
        
        elif hasattr(module, 'deinit'):
            atexit.register(module.deinit)
