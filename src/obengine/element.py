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
__date__ ="$Jul 13, 2010 6:13:05 PM$"

import event
import scenegraph

class Element(scenegraph.SceneNode):
    """
    The base class for all elements(i.e, scripts, bricks, etc...).
    You shouldn't make an instance of this class.
    """

    def __init__(self, name, parent = None):

        scenegraph.SceneNode.__init__(self, name, parent)
        
        self.on_add = event.Event()
        self.on_remove = event.Event()
        self.on_world_loaded = event.Event()

class BrickElement(Element):
    
    def __init__(self, name, coords, rgb, size, hpr, parent = None):

        Element.__init__(self, name, parent)

        self.coords = coords
        self.size = size
        self.hpr = hpr
        self.rgb = rgb

    def set_size(self, newsize):
        self.size = newsize

    def set_pos(self, newpos):
        self.coords =  newpos

    def set_hpr(self, newhpr):
        self.hpr = newhpr

    def set_rgb(self, newrgb):
        self.rgb = newrgb