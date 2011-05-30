"""
Copyright (C) 2010 The OpenBlox Project

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
__date__ ="$Aug 9, 2010 10:43:40 PM$"

import obengine

from obengine.elementfactory import ElementFactory
from obengine.gfx.math import *

import xml.etree.ElementTree as xmlparser

class WorldSource(list):

    def __init__(self, factory):
        """
        Do NOT create this class! Create one of its derivatives, instead.
        """

        self.factory = factory

    def retrieve(self):

        # This method needs to be overrid
        raise NotImplementedError

    def handle_brick(self, child):

        # Create the different brick attributes, with defaults

        rgb = Color()
        coords = Vector()
        orientation = EulerAngle()
        size = Vector()
        anchored = False

        # Remove all empty space first, to make string to number conversion easy

        coordstr = child.attrib['coords'].replace(' ','')
        rgbstr = child.attrib['rgb'].replace(' ','')
        orient_str = child.attrib['orientation'].replace(' ','')
        size_str = child.attrib['size'].replace(' ','')
        name = child.attrib['name']

        # Is the brick anchored?

        if child.attrib.has_key('anchored'):

            if child.attrib['anchored'] == 'yes':
                anchored = True

        # Fill the coordinate, size, RGB, and HPR arrays


        coords.x = float(coordstr.split(',')[0])
        coords.y = float(coordstr.split(',')[1])
        coords.z = float(coordstr.split(',')[2])

        rgb.r = int(rgbstr.split(',')[0])
        rgb.g = int(rgbstr.split(',')[1])
        rgb.b = int(rgbstr.split(',')[2])
        rgb.a = int(rgbstr.split(',')[3])

        orientation.h = float(orient_str.split(',')[0])
        orientation.p = float(orient_str.split(',')[1])
        orientation.r = float(orient_str.split(',')[2])

        size.x = int(size_str.split(',')[0])
        size.y = int(size_str.split(',')[1])
        size.z = int(size_str.split(',')[2])

        # Finally, create the brick!

        element = self.factory.make('brick', name, coords, rgb, size, orientation, False, anchored)

        self.append(element)

    def handle_skybox(self, child):

        # Create a skybox, optionally with a custom texture
        element = self.factory.make('skybox', child.attrib.get('src'))

        # Add it
        self.append(element)

    def handle_script(self, child):

        # Does this script tag refer to a file, or is the code included in the tag?

        if child.attrib.has_key('src'):
            element = self.factory.make('script', child.attrib['name'], None, child.attrib['src'])

        else:
            element = self.factory.make('script', child.attrib['name'], child.text)

        self.append(element)

    def handle_sound(self, child):
        """
        Creates a sound from a XML element.
        """

        # We need to convert "yes" and "no" to True/False, so we do it with a dict
        yes_no = { 'yes' : True, 'no' : False}

        # Retrieve the scene graph name, filename, and autoplay (play on added)
        name = child.attrib['name']
        src = child.attrib['src']
        autoplay = yes_no[child.attrib.get('autoplay', False)]

        # Create the element
        element = self.factory.make('sound', name, src, autoplay)

        self.append(element)

    def parse(self):
        """
        Parses a world.
        Exceptions:
        * UnknownWorldTagError when an unknown tag is encountered.
        * InsufficientVersionError if the "version" attribute of the world tag is greater than this engine's version
        """

        # self.retrieve returns a file-like object
        file = self.retrieve()

        tree = xmlparser.parse(file)
        rootnode = tree.getroot()

        # Check the version. We use 0.6.2 as the default, as that was the last version of OpenBlox
        # to not have this feature
        game_version = tuple(int(v) for v in rootnode.attrib.get('version', '0.6.2').split('.'))

        # We can't load this game if it's for a non-compatible version of OpenBlox
        if game_version[0] != obengine.ENGINE_VERSION[0]:
            raise InsufficientVersionError, rootnode.attrib.get('version', '0.6.2')

        supported_tags = {
        'brick' : 'handle_brick',
        'skybox' : 'handle_skybox',
        'script' : 'handle_script',
        'sound' : 'handle_sound'
        }

        # Run over all the children of the top-level "world" tag
        for child in rootnode:

            # Do we know how to handle this tag?
            if child.tag in supported_tags:
                getattr(self, supported_tags[child.tag])(child)

            # We don't. Raise an exception
            else:
                raise UnknownWorldTagError, child.tag

class FileWorldSource(WorldSource):
    """
    This class loads a world from a file.
    Supply this class to an obengine.world.World's load_world method, after calling FileWorldSource.parse.
    """

    def __init__(self, factory, path):
        """
        path is the file path of the world to load.
        """

        WorldSource.__init__(self, factory)
        self.path = path

    def retrieve(self):
        return open(self.path,'r')

class UnknownWorldTagError(Exception): pass
class InsufficientVersionError(Exception): pass