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


class NullXmlExtension(object):

    def __init__(self, _):
        pass

    @property
    def xml_element(self):
        return None


class XmlElementParser(object):

    tag = ''

    def parse(tag):
        raise NotImplementedError


class ElementMaker(object):

    element_name = ''

    def make(name, parent = None):
        raise NotImplementedError

