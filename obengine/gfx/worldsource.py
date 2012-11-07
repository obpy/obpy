#
# This module provides the ability to load a world from an XML file or file-like
# object.
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
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
__date__ = "$Aug 9, 2010 10:43:40 PM$"


import xml
import xml.etree.ElementTree as xmlparser

import obengine.gfx.element3d


class WorldSource(list):

    _element_handlers = {}
    _element_parsers = {}

    def __init__(self, factory):
        """
        Do *not* create this class! Create one of its derivatives, instead.
        """

        self.factory = factory

    @staticmethod
    def add_element_parser(parser_cls):

        assert WorldSource._element_parsers.get(parser_cls.tag) is None

        WorldSource._element_parsers[parser_cls.tag] = parser_cls

    def supported_tag(self, tag):
        return tag in self.supported_tags()

    def supported_tags(self):
        return self._element_parsers.keys()

    def retrieve(self):

        # This method needs to be overridden in a derivative
        raise NotImplementedError

    def parse(self):
        """
        Parses a world.
        Exceptions:
        * UnknownWorldTagError when an unknown tag is encountered.
        * InsufficientVersionError if the "version" attribute of the world tag is greater than this engine's version
        """

        # self.retrieve should return a file-like object
        file = self.retrieve()

        try:
            tree = xmlparser.parse(file)

        except xml.parsers.expat.ExpatError, message:
            raise BadWorldError(message)

        rootnode = tree.getroot()

        # Check the version. We use 0.6.2 as the default, as that was the last version of OpenBlox
        # to not have this feature
        game_version = rootnode.attrib.get('version', '0.6.2')

        # We can't load this game if it's for a non-compatible version of OpenBlox
        if obengine.compatible_with(game_version) is False:
            raise InsufficientVersionError, game_version

        # Run over all the children of the top-level "world" tag
        for child in rootnode:
            self._handle_node(child)

        # TODO: Replace the below line with something more extensible
        self.append(obengine.gfx.element3d.CameraElement(self.factory.window))

    def _handle_node(self, node):

        if self.supported_tag(node.tag):

            tag_parser_cls = self._element_parsers[node.tag]
            parser_instance = tag_parser_cls(self.factory)
            parsed_element = parser_instance.parse(node)

            self.append(parsed_element)

        else:
            raise UnknownWorldTagError, node.tag


class FileWorldSource(WorldSource):
    """
    This class loads a world from a file.
    Supply this class to an obengine.world.World's load_world method,
    after calling FileWorldSource.parse.
    """

    def __init__(self, path, factory):
        """
        path is the file path of the world to load.
        """

        WorldSource.__init__(self, factory)
        self.path = path

    def retrieve(self):
        return open(self.path, 'r')


class WorldSourceException(Exception):
    pass


class UnknownWorldTagError(WorldSourceException):
    pass


class InsufficientVersionError(WorldSourceException):
    pass


class BadWorldError(WorldSourceException):
    pass
