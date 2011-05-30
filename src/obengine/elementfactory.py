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
__author__ = "openblocks"
__date__  = "$Jan 23, 2011 7:57:35 AM$"

import obengine.async
import obengine.gfx.element3d
import obengine.element
import obengine.gfx.math
import obengine.depman

obengine.depman.gendeps()

def init():
    obengine.plugin.require('core.physics')

class ElementFactory(object):

    elements = [ 'brick', 'skybox', 'script', 'sound' ]

    def set_window(self, window):
        self.window = window

    def set_sandbox(self, sandbox):
        self.sandbox = sandbox

    def make(self, name, *args):
        """
        Creates a new element, and returns it.
        Extra arguments are passed to the
        Creatable elements are:

        * Brick
        * Skybox
        * Script
        * (NEW) Sound

        :param name: The type of element to create.
        :type name: `str`
        :returns: The created element
        :raises: `UnknownElementType` is raised if an unknown element type is given
        """

        if name in self.elements:
            return getattr(self, 'make_' + name)(*args)

        raise UnknownElementType(name)

    def make_brick(self, name, coords = None, rgb = None, size = None, hpr = None, hidden = False, anchored = False):
        
        import obplugin.core.physics

        coords = coords or obengine.gfx.math.Vector(0, 0, 0)
        rgb = rgb or obengine.gfx.math.Color(0, 0, 0, 255)
        size = size or  obengine.gfx.math.Vector(2, 4, 1)
        hpr = hpr or obengine.gfx.math.EulerAngle(0, 0, 0)

        # Create the model (not the 3D model, model as in MVC/MVP)

        model = obengine.element.BrickElement(name, coords, rgb, size, hpr)

        # Create the view and presenter

        view = obengine.gfx.element3d.BlockBrickView(size, hpr, rgb, self.window)
        view.load()

        phys_rep = obplugin.core.physics.Box(view.model, self.sandbox, None, anchored)
        presenter = obengine.gfx.element3d.BrickPresenter(model, view,  phys_rep)

        return presenter

    def make_skybox(self, texture = None):

        from obengine.gfx.element3d import SkyboxElement

        element = SkyboxElement(texture)
        return element

    def make_script(self, name, code, filename = None):
        
        from obengine.scripting.element import ScriptElement

        element = ScriptElement(name, filename, code)
        return element

    def make_sound(self, name, soundfile, autoplay = False):

        from obengine.audio.element import SoundElement

        element = SoundElement(name, soundfile, autoplay)
        return element

class UnknownElementError(Exception):
    """
    Raised when an unknown element type is passed to ElementFactory.make.
    """
    pass