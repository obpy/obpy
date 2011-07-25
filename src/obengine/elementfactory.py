#
# This module provides a simple way (using factories) to create various elements, instead of
# directly instantiating them.
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
#
#
# Copyright (C) 2011 The OpenBlox Project
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
__date__  = "$Jan 23, 2011 7:57:35 AM$"

import obengine.async
import obengine.gfx.element3d
import obengine.element
import obengine.gfx.math
import obengine.depman

obengine.depman.gendeps()

def init():

    obengine.plugin.require('core.physics')
    obengine.plugin.require('core.graphics')

class ElementFactory(object):

    def __init__(self):

        self.element_handlers = {
        'brick' : self.make_brick,
        'skybox' : self.make_skybox,
        'script' : self.make_script,
        'sound' : self.make_sound,
        'light' : self.make_light
        }

    def add_element_handler(self, element_type, handler):
        self.element_handlers[element_type] = handler

    def set_window(self, window):
        ElementFactory.window = window

    def set_sandbox(self, sandbox):
        ElementFactory.sandbox = sandbox

    def make(self, name, *args, **kwargs):
        """
        Creates a new element, and returns it.
        Extra arguments are passed to that element's respective handler.
        Creatable elements are:

        * Brick
        * Skybox
        * Script
        * **(NEW)** Sound
        * **(NEW)** Light

        UnknownElementType is raised if an unknown element type is given.
        """

        try:
            handler = self.element_handlers[name]

        except KeyError:
            raise UnknownElementError(name)

        return handler(*args, **kwargs)

    def make_brick(self, name, coords = None, color = None, size = None, rotation = None, anchored = False):
        
        import obplugin.core.physics

        coords = coords or obengine.gfx.math.Vector(0, 0, 0)
        color = color or obengine.gfx.math.Color(0, 0, 0, 255)
        size = size or  obengine.gfx.math.Vector(2, 4, 1)
        rotation = rotation or obengine.gfx.math.EulerAngle(0, 0, 0)

        view = obengine.gfx.element3d.BlockBrickView(size, rotation, color, self.window)
        view.load()

        scheduler = self.window.scheduler

        while view.loaded is False:
            scheduler.step()

        phys_rep = obplugin.core.physics.Box(view.model, self.sandbox, None, scheduler, anchored)
        phys_rep.load()
        
        while phys_rep.loaded is False:
            scheduler.step()

        controller = obengine.gfx.element3d.BrickPresenter(name, coords, color, size, rotation, view,  phys_rep)
        return controller

    def make_skybox(self, texture = None):

        import obplugin.core.graphics
        from obengine.gfx.element3d import SkyboxElement

        camera = obplugin.core.graphics.Camera(self.window)
        element = SkyboxElement(self.window, camera, texture)
        
        return element

    def make_script(self, name, code, filename = None):
        
        from obengine.scripting.element import ScriptElement

        element = ScriptElement(name, filename, code)
        return element

    def make_sound(self, name, soundfile, autoplay = False):

        from obengine.audio.element import SoundElement

        element = SoundElement(name, soundfile, autoplay)
        return element

    def make_light(self, name, type = None, color = None, rotation = None):

        from obengine.gfx.element3d import LightElement

        element = LightElement(name, self.window, type, color, rotation)
        return element

class UnknownElementError(Exception):
    """
    Raised when an unknown element type is passed to ElementFactory.make.
    """
    pass