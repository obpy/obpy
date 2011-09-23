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

import obengine.math
import obengine.gfx.element3d


class WorldSource(list):

    _element_handlers = {}

    def __init__(self, factory):
        """
        Do *not* create this class! Create one of its derivatives, instead.
        """

        self.factory = factory

        self.add_element_handler('brick', self.handle_brick)
        self.add_element_handler('script', self.handle_script)
        self.add_element_handler('skybox', self.handle_skybox)
        self.add_element_handler('sound', self.handle_sound)
        self.add_element_handler('light', self.handle_light)

    def add_element_handler(self, tag, handler, local = True):

        handler_owner = self

        if local is False:
            handler_owner = WorldSource

        handler_owner._element_handlers.setdefault(tag, []).append(handler)

    def supported_tag(self, tag):
        return tag in self.supported_tags()

    def supported_tags(self):
        return self._element_handlers.keys()

    def retrieve(self):

        # This method needs to be overridden in a derivative
        raise NotImplementedError

    def handle_brick(self, _, child, factory):

        # Create the different brick attributes, with defaults

        rgb = obengine.math.Color()
        coords = obengine.math.Vector()
        orientation = obengine.math.EulerAngle()
        size = obengine.math.Vector()
        anchored = False

        # Remove all empty space first, to make string to number conversion easy

        try:

            coordstr = child.attrib['coords'].replace(' ', '')
            rgbstr = child.attrib['rgb'].replace(' ', '')
            orient_str = child.attrib['orientation'].replace(' ', '')
            size_str = child.attrib['size'].replace(' ', '')
            name = child.attrib['name']

        except KeyError, message:
            raise BadWorldError(message)

        # Is the brick anchored?

        if child.attrib.has_key('anchored'):

            if child.attrib['anchored'] == 'yes':
                anchored = True

        # Fill the coordinate, size, RGB, and HPR arrays

        try:

            coords.x = float(coordstr.split(',')[0])
            coords.y = float(coordstr.split(',')[1])
            coords.z = float(coordstr.split(',')[2])

            rgb.r = float(rgbstr.split(',')[0])
            rgb.g = float(rgbstr.split(',')[1])
            rgb.b = float(rgbstr.split(',')[2])
            rgb.a = float(rgbstr.split(',')[3])

            orientation.h = float(orient_str.split(',')[0])
            orientation.p = float(orient_str.split(',')[1])
            orientation.r = float(orient_str.split(',')[2])

            size.x = float(size_str.split(',')[0])
            size.y = float(size_str.split(',')[1])
            size.z = float(size_str.split(',')[2])

        except IndexError, message:
            raise BadWorldError(message)

        # Finally, create the brick!

        element = factory.make('brick', name, coords, rgb, size, orientation, anchored)
        self.append(element)

    def handle_skybox(self, _, child, factory):

        # Create a skybox, optionally with a custom texture
        element = factory.make('skybox', child.attrib.get('src'),)

        # Add it
        self.append(element)

    def handle_script(self, _, child, factory):

        # Does this script tag refer to a file, or is the code included in the tag?

        if child.attrib.has_key('src'):
            element = factory.make('script', child.attrib['name'], None, child.attrib['src'])

        else:
            element = factory.make('script', child.attrib['name'], child.text)

        self.append(element)

    def handle_sound(self, _, child, factory):
        """
        Creates a sound from a XML element.
        """

        # We need to convert "yes" and "no" to True/False, so we do it with a dict
        yes_no = { 'yes' : True, 'no' : False}

        # Retrieve the scene graph name, filename, and autoplay (play on added)
        try:

            name = child.attrib['name']
            src = child.attrib['src']
            autoplay = yes_no[child.attrib.get('autoplay', 'no')]

        except KeyError, message:
            raise BadWorldError(message)

        # Create the element
        element = factory.make('sound', name, src, autoplay)

        self.append(element)

    def handle_light(self, _, child, factory):

        try:

            name = child.attrib['name']
            type = child.attrib['type']

            light_rotation = map(lambda s: float(s), child.attrib['orientation'].strip().split(','))
            rotation = obengine.math.EulerAngle(*light_rotation)

            light_color = map(lambda s: float(s), child.attrib['rgb'].strip().split(','))
            color = obengine.math.Color(*light_color)

            position = None
            if type == 'point':

                light_position = map(lambda s: float(s), child.attrib['coords'].strip().split(','))
                position = obengine.math.Vector(*light_position)

            yes_no = { 'yes' : True, 'no' : False}
            cast_shadows = yes_no[child.attrib.get('cast_shadows', 'no')]

        except (KeyError, ValueError), message:
            raise BadWorldError(message)

        element = factory.make('light', name, type, color, position, rotation, cast_shadows)
        self.append(element)

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

        self.append(obengine.gfx.element3d.CameraElement(self.factory.window))

    def _handle_node(self, node):

        if self.supported_tag(node.tag):
            for handler in self._element_handlers[node.tag]:
                handler(self, node, self.factory)

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
