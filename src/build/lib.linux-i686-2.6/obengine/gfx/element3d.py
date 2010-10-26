__author__="openblocks"
__date__ ="$Aug 9, 2010 11:04:13 PM$"

from obengine.element import *
from obengine.cfg import cfgdir
from obengine.gfx import get_rootwin

from obengine.phys import PhysicalObject

from pandac.PandaModules import CompassEffect
from direct.task import Task

class BrickPresenter(object):
    
    def __init__(self, brick, view, hidden = False, anchored = False):

        self.brick = brick
        self.view = view

        self.hidden = hidden

        self.brick.on_add = self.on_add
        self.brick.on_remove = self.on_remove

        self.name = self.brick.name

        self.anchored = anchored

        self.set_rgb(self.brick.rgb[0], self.brick.rgb[1], self.brick.rgb[2])
        self.set_pos(self.brick.coords[0], self.brick.coords[1], self.brick.coords[2])
        self.set_size(self.brick.size[0], self.brick.size[1], self.brick.size[2])
        self.set_hpr(self.brick.hpr[0], self.brick.hpr[1], self.brick.hpr[2])

        self.phys_obj = PhysicalObject(self.view, self.brick.size, anchored)

        print 'Created brick', self.name, 'at position', self.brick.coords

    def hide(self):

        self.hidden = True
        self.view.detachNode()

    def show(self):

        self.hidden = False
        self.view.reparentTo(get_rootwin().render)

    def set_size(self, x, y, z):

        self.brick.set_size(x, y, z)
        self.view.setScale(float(x) / 2, float(y) / 4, float(z))

    def set_hpr(self, h, p, r):

        self.brick.set_hpr(h, p, r)
        self.view.setHpr(h, p, r)

    def set_pos(self, x, y, z):

        self.brick.set_pos(x, y, z)
        self.view.setPos(x, y, z)

    def set_rgb(self, r, g, b):

        self.brick.set_rgb(r, g, b)
        self.view.setColor(float(r) / 255, float(g) / 255, float(b) / 255)

    def on_add(self):

       self.show()

    def on_remove(self):

        self.hide()
        
class SkyboxElement(Element):

    def __init__(self, texture = None):

        Element.__init__(self, 'Skybox')

        self.sky = get_rootwin().loader.loadModel(cfgdir + '/data/sky.egg.pz')
        self.sky.reparentTo(get_rootwin().camera)
        self.sky.setEffect(CompassEffect.make(get_rootwin().render))
        self.sky.setScale(5000)
        self.sky.setShaderOff()
        self.sky.setLightOff()

        if texture:

            self.sky.setTexture(get_rootwin().loader.loadTexture(texture))
