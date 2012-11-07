#
# This module provides the base Element class, for other world elements to
# inherit from.
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
#
#
# Copyright (C) 2010-2011 The OpenBlox Project
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
__date__ = "$Jul 13, 2010 6:13:05 PM$"


import functools

import obengine.datatypes
import obengine.event
import obengine.scenegraph


class Element(obengine.scenegraph.SceneNode, obengine.datatypes.ExtensibleObjectMixin):
    """
    The base class for all elements(i.e, scripts, bricks, etc...).
    You shouldn't make an instance of this class.
    """

    def __init__(self, name, parent = None):

        obengine.scenegraph.SceneNode.__init__(self, name, parent)
        obengine.datatypes.ExtensibleObjectMixin.__init__(self)

        self.set_extension('xml', NullXmlExtension)
        self.on_world_loaded = obengine.event.Event()

    def get_properties(self):

        properties = []

        for attribute_name, attribute in self.__class__.__dict__.iteritems():
            if attribute.__class__.__name__ == 'ElementProperty':
                properties.append((attribute_name, attribute))

        return properties


class NullXmlExtension(object):

    def __init__(self, _):
        pass

    @property
    def xml_element(self):
        return None


class XmlElementParser(object):

    tag = ''

    def __init__(self, element_factory):
        self._element_factory = element_factory

    def parse(self, node):
        raise NotImplementedError


class XmlParseError(Exception):
    pass


class ElementMaker(object):

    element_name = ''

    def make(self, name, parent = None):
        raise NotImplementedError


def element_property(property_name = None, property_settable = True):

    class ElementProperty(property):

        def __init__(self, func, name, settable):

            self.name = name

            func_locals = func()

            try:
                fget = func_locals['get']
            except KeyError:
                raise TypeError('getter function for nested property must be defined')

            fset = func_locals.get('set')
            if fset is None:
                settable = False
                self.settable = settable

            fdel = func_locals.get('del_')

            property.__init__(self, fget, fset, fdel)

    return functools.partial(ElementProperty, name = property_name, settable = property_settable)
