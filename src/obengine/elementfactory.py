"""
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
__date__ ="$Jan 23, 2011 7:57:35 AM$"

import obengine.gfx.math

class ElementFactory(object):

    elements = [ 'brick', 'skybox', 'script' ]

    def make(self, name, *args):
        """
        Creates a new element, and returns it.

        Creatable elements are:

        * Brick
        * Skybox
        * Script

        If an unknown element type is given, UnknownElementType is raised.
        """

        if name in self.elements:
            return getattr(self, 'make_' + name)(*args)

        raise UnknownElementType(name)

    def make_brick(self, name, coords = obengine.gfx.math.Vector(0, 0, 0), rgb = obengine.gfx.math.Color(0, 0, 0, 255), size = obengine.gfx.math.Vector(2, 4, 1), hpr = obengine.gfx.math.EulerAngle(0, 0, 0), hidden = False, anchored = False):

        import obengine.gfx
        import obengine.gfx.element3d
        
        from obengine.cfg import get_config_var
        from obengine.element import BrickElement

        import os
        
        from panda3d.core import Filename

        # Create the model (not the 3D model, model as in MVC/MVP)

        model = BrickElement(name, coords, rgb, size, hpr)

        # Create the view and presenter

        view = obengine.gfx.element3d.BlockBrickView(size, hpr, rgb)
        presenter = obengine.gfx.element3d.BrickPresenter(model, view, hidden, anchored)

        return presenter

    def make_skybox(self, texture = None):

        from obengine.gfx.element3d import SkyboxElement

        element = SkyboxElement(texture)

        return element

    def make_script(self, name, code, filename = None):
        
        from obengine.scripting.element import ScriptElement

        element = ScriptElement(name, filename, code)

        return element

class UnknownElementTypeException(Exception):
    """
    Raised when an unknown element type is passed to ElementFactory.make.
    """

    def __init__(self, message):
        Exception.__init__(self, message)