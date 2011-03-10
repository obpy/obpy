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

from obengine.elementfactory import ElementFactory
from obengine.gfx.math import *
import xml.etree.ElementTree as xmlparser

class WorldSource(list):

    def __init__(self, source):
        """
        source is a derivative of WorldSource (yes, kinda confusing...)
        Do NOT create this class! Create one of its derivatives, instead.
        """

        self.source = source

    def handle_brick(self, child):

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

        element = ElementFactory().make('brick', name, coords, rgb, size, orientation, False, anchored)

        self.append(element)

    def handle_skybox(self, child):

        element = ElementFactory().make('skybox')
        
        self.append(element)

    def handle_script(self, child):

        # Does this script tag refer to a file, or is the code included in the tag?

        if child.attrib.has_key('src'):
            element = ElementFactory().make('script', child.attrib['name'], None, child.attrib['src'])

        else:
            element = ElementFactory().make('script', child.attrib['name'], child.text)

        self.append(element)

    def parse(self):
        
        file = self.source.retrieve()

        tree = xmlparser.parse(file)
        rootnode = tree.getroot()

        supported_tags = { 'brick' : 'handle_brick', 'skybox' : 'handle_skybox', 'script' : 'handle_script' }


        for child in rootnode:

            if child.tag in supported_tags:
                getattr(self, supported_tags[child.tag])(child)

class FileWorldSource(WorldSource):
    """
    This class loads a world from a file. Supply this class to an obengine.world.World's load_world method, after calling FileWorldSource.retrieve.
    """

    def __init__(self, path):
        """
        path is the file path of the world to load.
        """

        WorldSource.__init__(self, self) # Yes, very wierd...
        self.path = path

    def retrieve(self):
        return open(self.path,'r')