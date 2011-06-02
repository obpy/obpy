# OpenBlox interface checker (obengine.interface)
# ===============================================
#
# Provides a simple interface checker.
#
# Copyright (C) 2011 The OpenBlox Project
# License: GNU GPL v3
#
# See <TODO: No Sphinx docs yet - add some!> for the primary source of documentation
# for this module.

__author__ = "openblocks"
__date__  = "$Apr 14, 2011 3:33:49 AM$"

import inspect

def _implements(obj, interface):

    obj_set = set(dir(obj))
    interface_set = set(dir(interface))

    if interface_set.issubset(obj_set) is False:
        raise InterfaceOmissionError, tuple(interface_set - obj_set)

    for attr in interface_set:

        interface_attr = getattr(interface, attr)

        if inspect.ismethod(interface_attr) is False:
            continue

        interface_method = interface_attr
        obj_method = getattr(obj, attr)

        interface_method_argspec = inspect.getargspec(interface_method)
        obj_method_argspec = inspect.getargspec(obj_method)

        if interface_method_argspec != obj_method_argspec:
            raise InterfaceMethodError, interface_method

def implements(*args):
    """
    Checks to see if a class implements a list of interfaces.

    Example:

        >>> from obengine.interface import *
        >>> class TestClass(object):
        ...     def __init__(self, a, b, c):
        ...         pass
        ...     def do_x(self, x):
        ...         pass
        ...     def do_y(self, y):
        ...         pass
        ...     def do_z(self, z):
        ...         pass
        ...
        >>> class TestInterface1(object):
        ...     def do_z(self, z):
        ...         pass
        ...
        >>> class TestInterface2(object):
        ...     def __init__(self, a, b, c):
        ...         pass
        ...     def do_x(self, x):
        ...         pass
        ...
        >>> class TestInterface3(object):
        ...     def __init__(self, a, b, c, d):
        ...         pass
        >>> implements(TestClass, TestInterface1)
        True
        >>> implements(TestClass, TestInterface2)
        True
        >>> implements(TestClass, TestInterface3)
        False

    As you can see, `implements` checks not only for defined attributes, it checks
    method signatures as well.

    You can also check for compliance with multiple interfaces at once:

        >>> implements(TestClass, TestInterface1, TestInterface2)
        True
        >>> implements(TestClass, TestInterface1, TestInterface3)
        False

    `implements` will return `True` if *and only if* the class in question implements
    *all* of the requested interfaces. Otherwise, `implements` will return `False`.
    """

    args = list(args)
    obj = args.pop(0)

    try:

        while args:

            interface = args.pop(0)
            _implements(obj, interface)

    except InterfaceException:
        return False

    else:
        return True

class InterfaceException(Exception): pass
class InterfaceOmissionError(InterfaceException): pass
class InterfaceMethodError(InterfaceException): pass