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
__date__ ="$Apr 14, 2011 3:33:49 AM$"

import inspect

def _implements(obj, interface):

    obj_set = set(dir(obj))
    interface_set = set(dir(interface))

    if interface_set.issubset(obj_set) is False:
        raise InterfaceOmissionError, tuple(interface_set - obj_set)

    for interface_method in filter(inspect.ismethod, map(interface.__dict__.__getitem__, interface_set)):

        obj_method = getattr(obj, interface_method)

        if inspect.ismethod(obj_method) is False:
            raise InterfaceMethodError, interface_method

        interface_method = getattr(interface, interface_method)

        if inspect.getargspec(interface_method) != inspect.getargspec(obj_method):
            raise InterfaceMethodError, interface_method

def implements(*args):

    args = list(args)
    obj = args.pop(0)

    if hasattr(obj, '__implements__'):

        while args:

            if args.pop(0) not in obj.__implements__:
                return False

        return True

    else:

        obj.__implements__ = []

        try:
            
            while args:

                interface = args.pop(0)
                _implements(obj, interface)

                obj.__implements__.append(interface)


        except:
            return False

        else:
            return True

class InterfaceOmissionError(Exception): pass
class InterfaceMethodError(Exception): pass
