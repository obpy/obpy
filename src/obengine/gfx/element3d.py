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
__date__ ="$Aug 9, 2010 11:04:13 PM$"

import obengine.element
import obengine.cfg
import obengine.gfx
import obengine.phys

from pandac.PandaModules import CompassEffect, TransparencyAttrib, Filename

class BrickPresenter(object):
    
    def __init__(self, brick, view, hidden = False, anchored = False):

        self.brick = brick
        self.view = view

        self.hidden = hidden

        self.brick.on_add = self.on_add
        self.brick.on_remove = self.on_remove

        self.name = self.brick.name

        self.anchored = anchored

        self.set_rgb(self.brick.rgb[0], self.brick.rgb[1], self.brick.rgb[2], self.brick.rgb[3])
        self.set_pos(self.brick.coords[0], self.brick.coords[1], self.brick.coords[2])
        self.set_size(self.brick.size[0], self.brick.size[1], self.brick.size[2])
        self.set_hpr(self.brick.hpr[0], self.brick.hpr[1], self.brick.hpr[2])

        self.phys_obj = obengine.phys.PhysicalObject(self, self.brick.size, anchored)
        self.view.setTransparency(TransparencyAttrib.MAlpha)

    def hide(self):

        self.hidden = True
        self.view.detachNode()

    def show(self):

        self.hidden = False
        self.view.reparentTo(obengine.gfx.get_rootwin().render)

    def set_size(self, x, y, z):

        self.brick.set_size(x, y, z)
        self.view.setScale(float(x) / 2, float(y) / 4, float(z))

    def set_hpr(self, h, p, r, update_phys = True):

        self.brick.set_hpr(h, p, r)
        self.view.setHpr(h, p, r)

        if hasattr(self, 'phys_obj'):

            self.phys_obj.set_hpr(h, p, r)

    def set_pos(self, x, y, z):

        self.brick.set_pos(x, y, z)
        self.view.setPos(x, y, z)

        if hasattr(self, 'phys_obj'):
            
            self.phys_obj.set_pos(x, y, z)

    def set_rgb(self, r, g, b, a):

        self.brick.set_rgb(r, g, b, a)
        self.view.setColor(float(r) / 255, float(g) / 255, float(b) / 255, float(a) / 255)

    def on_add(self, world):

        self.world = world
        
        self.show()

    def on_remove(self):

        self.hide()
        
class SkyboxElement(obengine.element.Element):

    def __init__(self, texture = None):

        obengine.element.Element.__init__(self, 'Skybox')

        self.sky = obengine.gfx.get_rootwin().loader.loadModel(Filename.fromOsSpecific(obengine.cfg.get_config_var('cfgdir') + '/data/sky.egg.pz'))
        self.sky.reparentTo(obengine.gfx.get_rootwin().camera)
        self.sky.setEffect(CompassEffect.make(obengine.gfx.get_rootwin().render))
        self.sky.setScale(5000)
        self.sky.setShaderOff()
        self.sky.setLightOff()

        if texture:

            self.sky.setTexture(obengine.gfx.get_rootwin().loader.loadTexture(texture))
