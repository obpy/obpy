#
# Legacy module - will probably be removed/partitioned in the near future.
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
#
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
__date__  = "$Aug 9, 2010 11:04:13 PM$"


import functools

import obengine.element
import obengine.depman
import obengine.plugin
import obengine.deprecated
import obengine.gfx.math

obengine.depman.gendeps()


DEFAULT_X_SIZE = 2.0
DEFAULT_Y_SIZE = 4.0
DEFAULT_Z_SIZE = 1.0


def init():
    obengine.plugin.require('core.graphics')


class BrickView(object):
    """
    Base view for all different sorts of bricks.
    To use, simply create a variable called type in your subclass, that corresponds to a model file in data/.
    Then, implement set_size, set_hpr, set_pos, and set_color methods
    that take obengine.gfx.math.Vector, obengine.gfx.math.EulerAngle, or obengine.gfx.math.Color as arguments.
    """

    def __init__(self, size, rotation, color, window):

        import obplugin.core.graphics

        self.model = obplugin.core.graphics.Model(self.type + '-new', window)
        self.on_loaded = self.model.on_loaded

        self.on_loaded += functools.partial(self._init_attrs, size, rotation, color)

    @property
    def showing(self):
        return self.model.showing

    @showing.setter
    def showing(self, show):
        self.model.showing = show

    @obengine.deprecated.deprecated
    def hide(self):
        self.showing = False

    @obengine.deprecated.deprecated
    def show(self):
        self.showing = True

    def load(self, async = True):
        self.model.load(async)

    @property
    def loaded(self):
        return self.model.load_okay

    def _init_attrs(self, size, rotation, color):

        self.size = size
        self.rotation = rotation
        self.color = color


class BlockBrickView(BrickView):

    type = 'brick'

    @property
    def position(self):
        return self.model.position

    @position.setter
    def position(self, new_pos):
        self.model.position = new_pos

    @property
    def size(self):

        size = self.model.size
        brick_size = obengine.gfx.math.Vector(
        size.x * DEFAULT_X_SIZE,
        size.y * DEFAULT_Y_SIZE,
        size.z * DEFAULT_Z_SIZE
        )
        
        return brick_size

    @size.setter
    def size(self, new_size):
        self.model.scale = new_size.x / DEFAULT_X_SIZE, new_size.y / DEFAULT_Y_SIZE, new_size.z / DEFAULT_Z_SIZE

    @property
    def rotation(self):
        return self.model.rotation

    @rotation.setter
    def rotation(self, new_rot):
        self.model.rotation = new_rot

    @property
    def color(self):
        return self.model.color

    @color.setter
    def color(self, new_color):
        self.model.color = new_color

    @obengine.deprecated.deprecated
    def set_pos(self, vector):
        self.position = vector

    @obengine.deprecated.deprecated
    def set_size(self, size):
        self.size = size

    @obengine.deprecated.deprecated
    def set_hpr(self, hpr):
        self.rotation = hpr

    @obengine.deprecated.deprecated
    def set_color(self, rgb):
        self.color = rgb


class BrickPresenter(object):
    
    def __init__(self, brick, view, phys_rep):

        self.brick = brick
        self.view = view

        self.on_add = self.brick.on_add
        self.on_remove = self.brick.on_remove
        self.on_name_changed = self.brick.on_name_changed
        self.on_parent_changed = self.brick.on_parent_changed

        self.brick.on_add += self.presenter_on_add
        self.brick.on_remove += self.presenter_on_remove

        self.phys_rep = phys_rep
        self.phys_rep.owner = self

    @obengine.deprecated.deprecated
    def hide(self):
        pass

    @obengine.deprecated.deprecated
    def show(self):
        pass

    @property
    def size(self):
        return self.view.size

    @size.setter
    def size(self, new_size):

        self.view.size = new_size
        self.brick.set_size(new_size)

        self.phys_obj.update_size()
        
    @property
    def rotation(self):
        return self.view.rotation

    @rotation.setter
    def rotation(self, new_rot):

        self.brick.set_hpr(new_rot)
        self.view.rotation = new_rot
        
        self.phys_rep.rotation = new_rot

    @property
    def position(self):
        return self.view.position

    @position.setter
    def position(self, new_pos):

        self.brick.set_pos(new_pos)
        self.view.position = new_pos

        self.phys_rep.position = new_pos

    @property
    def name(self):
        return self.brick.name

    @name.setter
    def name(self, new_name):
        self.brick.name = new_name

    @property
    def nid(self):
        return self.brick.nid

    @property
    def parent(self):
        return self.brick.parent

    @parent.setter
    def parent(self, new_parent):
        self.brick.parent = new_parent

    @property
    def children(self):
        return self.brick.children

    @obengine.deprecated.deprecated
    def set_size(self, size):

        self.brick.set_size(size)
        self.view.set_size(size)

    @obengine.deprecated.deprecated
    def set_hpr(self, hpr):

        self.brick.set_hpr(hpr)
        self.view.rotation = hpr
        self.phys_rep.rotation = hpr

    @obengine.deprecated.deprecated
    def set_pos(self, vector):

        self.brick.set_pos(vector)
        self.view.position = vector

        self.phys_rep.position = vector

    @obengine.deprecated.deprecated
    def set_rgb(self, color):

        self.brick.set_rgb(color)
        self.view.color = color

    def presenter_on_add(self, world):

        self.world = world
        self.phys_rep.enable()

    def presenter_on_remove(self):

        self.model.showing = False
        self.phys_rep.disable()


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
