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

    This module contains all of the 3D elements, including the Brick View(s) and Presenter, and Skybox.
"""
__author__="openblocks"
__date__ ="$Aug 9, 2010 11:04:13 PM$"

import obengine.element
import obengine.cfg
import obengine.gfx
import obengine.phys
import obengine.gfx.math
from obengine.cfg import get_config_var

from panda3d.core import CompassEffect, TransparencyAttrib, Filename

import os

class BrickView(object):
    """
    Base view for all different sorts of bricks.
    To use, simply create a variable called type in your subclcass, that corresponds to a model file in data/.
    Then, implement set_size, set_hpr, set_pos, and set_color methods
    that take obengine.gfx.math.Vector, obengine.gfx.math.EulerAngle, or obengine.gfx.math.Color as arguments.
    """

    def __init__(self, size, hpr, color):

        self.model = obengine.gfx.get_rootwin().loader.loadModel(Filename.fromOsSpecific(get_config_var('cfgdir') + os.path.join(os.sep + 'data', self.type)))
        self.model.setTransparency(TransparencyAttrib.MAlpha)
        
        self.set_size(size)
        self.set_hpr(hpr)
        self.set_color(color)

    def hide(self):
        self.model.detachNode()

    def show(self):
        self.model.reparentTo(obengine.gfx.get_rootwin().render)

class BlockBrickView(BrickView):

    type = 'brick'

    def set_pos(self, vector):
        self.model.setPos(float(vector.x), float(vector.y), float(vector.z))

    def set_size(self, size):
        self.model.setScale(float(size.x) / 2, float(size.y) / 4, float(size.z))

    def set_hpr(self, hpr):
        self.model.setHpr(hpr.h, hpr.p, hpr.r)

    def set_color(self, rgb):
        self.model.setColor(float(rgb.r) / 255, float(rgb.g) / 255, float(rgb.b) / 255, float(rgb.a) / 255)

class BrickPresenter(object):
    
    def __init__(self, brick, view, hidden = False, anchored = False):

        self.brick = brick
        self.view = view

        self.hidden = hidden

        self.on_add = self.brick.on_add
        self.on_remove = self.brick.on_remove

        self.on_add += self.presenter_on_add
        self.on_remove += self.presenter_on_remove

        self.name = self.brick.name

        self.anchored = anchored

        self.set_rgb(obengine.gfx.math.Color(self.brick.rgb.r, self.brick.rgb.g, self.brick.rgb.b, self.brick.rgb.a))
        self.set_pos(obengine.gfx.math.Vector(self.brick.coords.x, self.brick.coords.y, self.brick.coords.z))
        self.set_size(obengine.gfx.math.Vector(self.brick.size.x, self.brick.size.y, self.brick.size.z))
        self.set_hpr(obengine.gfx.math.EulerAngle(self.brick.hpr.h, self.brick.hpr.p, self.brick.hpr.r))

        self.phys_obj = obengine.phys.PhysicalObject(self, self.brick.size, anchored)
        self.on_add += self.phys_obj.phys_on_add
        self.on_remove += self.phys_obj.phys_on_remove

    def hide(self):

        self.hidden = True
        self.view.hide()

    def show(self):

        self.hidden = False
        self.view.show()

    def set_size(self, size):

        self.brick.set_size(size)
        self.view.set_size(size)

    def set_hpr(self, hpr, update_phys = True):

        self.brick.set_hpr(hpr)
        self.view.set_hpr(hpr)

        if hasattr(self, 'phys_obj'):
            self.phys_obj.set_hpr(hpr.h, hpr.p, hpr.r)

    def set_pos(self, vector):

        self.brick.set_pos(vector)
        self.view.set_pos(vector)

        if hasattr(self, 'phys_obj'):
            self.phys_obj.set_pos(vector.x, vector.y, vector.z)

    def set_rgb(self, color):

        self.brick.set_rgb(color)
        self.view.set_color(color)

    def presenter_on_add(self, world):

        self.world = world
        self.show()

    def presenter_on_remove(self):
        self.hide()
        
class SkyboxElement(obengine.element.Element):

    def __init__(self, texture = None):

        obengine.element.Element.__init__(self, 'Skybox')

        # Create the skybox (although the actual model is currently a skysphere!)

        self.texture = texture
        self.sky = obengine.gfx.get_rootwin().loader.loadModel(Filename.fromOsSpecific(obengine.cfg.get_config_var('cfgdir') +  os.path.join(os.sep + 'data','sky.egg.pz')))

        self.on_add += self.sky_on_add
        self.on_remove += self.sky_on_remove

    def sky_on_add(self, world):

        self.sky.reparentTo(obengine.gfx.get_rootwin().camera)
        self.sky.setEffect(CompassEffect.make(obengine.gfx.get_rootwin().render))
        self.sky.setScale(5000)
        self.sky.setShaderOff()
        self.sky.setLightOff()

        # Did the user specifiy a texture to use instead?

        if self.texture:
            self.sky.setTexture(obengine.gfx.get_rootwin().loader.loadTexture(texture))

    def sky_on_remove(self):
        self.sky.detachNode()