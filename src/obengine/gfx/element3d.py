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
__date__ = "$Aug 9, 2010 11:04:13 PM$"


import functools
import xml.etree.ElementTree as xmlparser

from panda3d.core import CompassEffect

import obengine.math
import obengine.datatypes
import obengine.element
import obengine.plugin
import obengine.deprecated
import obengine.depman
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
    that take obengine.math.Vector, obengine.math.EulerAngle, or obengine.math.Color as arguments.
    """

    def __init__(self, size, rotation, color, window):

        import obplugin.core.graphics
        self.model = obplugin.core.graphics.Model(self.type, window)
        self.on_click = self.model.on_click

        self.on_loaded = self.model.on_loaded
        self.on_loaded += functools.partial(self._init_attrs, size, rotation, color)

    def hide(self):
        self.showing = False

    def show(self):
        self.showing = True

    def load(self, async = True):
        self.model.load(async)

    @obengine.datatypes.nested_property
    def showing():

        def fget(self):
            return self.model.showing


        def fset(self, show):
            self.model.showing = show

        return locals()

    @property
    def bounds(self):
        return self.model.bounds

    @property
    def loaded(self):
        return self.model.load_okay

    def _init_attrs(self, size, rotation, color):

        self.size = size
        self.rotation = rotation
        self.color = color


class BlockBrickView(BrickView):

    type = 'brick-flat'

    def __init__(self, size, rotation, color, window):
        BrickView.__init__(self, size, rotation, color, window)

    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return self.model.position

        def fset(self, new_pos):
            self.model.position = new_pos

        return locals()

    @obengine.datatypes.nested_property
    def size():

        def fget(self):

            size = self.model.scale
            brick_size = obengine.gfx.math.Vector(
            size.x * DEFAULT_X_SIZE,
            size.y * DEFAULT_Y_SIZE,
            size.z * DEFAULT_Z_SIZE
            )

            return brick_size

        def fset(self, new_size):

            self.model.scale = (
            new_size.x / DEFAULT_X_SIZE,
            new_size.y / DEFAULT_Y_SIZE,
            new_size.z / DEFAULT_Z_SIZE
            )

        return locals()

    @obengine.datatypes.nested_property
    def rotation():

        def fget(self):
            return self.model.rotation

        def fset(self, new_rot):
            self.model.rotation = new_rot

        return locals()

    @obengine.datatypes.nested_property
    def color():

        def fget(self):
            return self.model.color

        def fset(self, new_color):
            self.model.color = new_color

        return locals()

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


class XmlElementExtension(object):

    def _vector_str(self, vector):

        vector_str = str(vector)
        vector_str = vector_str[len('Vector') + 1:len(vector_str) - 1]

        return vector_str

    def _color_str(self, color):

        color_str = str(color)
        color_str = color_str[len('Color') + 1:len(color_str) - 1]

        return color_str

    def _euler_str(self, angle):

        euler_str = str(angle)
        euler_str = euler_str[len('EulerAngle') + 1:len(euler_str) - 1]

        # TODO: There has to be a better solution than this!
        return euler_str or '0.0, 0.0, 0.0'

    def _bool_str(self, bool):

        conv_dict = {True : 'yes', False : 'no'}
        return conv_dict[bool]


class BrickPresenter(obengine.element.Element):

    def __init__(self, name, position, color, size, rotation, view, phys_rep):

        obengine.element.Element.__init__(self, name)
        self.set_extension('xml', XmlBrickExtension)

        self.view = view
        self.on_click = self.view.on_click

        self.on_add += self._on_add
        self.on_remove += self._on_remove

        self.phys_rep = phys_rep
        self.phys_rep.owner = self
        self.on_collision = self.phys_rep.on_collision

        self.position = position
        self.color = color
        self.rotation = rotation

    def hide(self):

        self.view.hide()
        self.phys_rep.disable()

    def show(self):

        self.view.show()
        self.phys_rep.enable()

    @obengine.datatypes.nested_property
    def showing():

        def fget(self):
            return self.view.showing

        def fset(self, showing):

            if showing is True:
                self.show()

            else:
                self.hide()

        return locals()

    @obengine.datatypes.nested_property
    def size():

        def fget(self):
            return self.view.size

        def fset(self, new_size):

            self.view.size = new_size
            self.phys_rep.update_size()

        return locals()

    @obengine.datatypes.nested_property
    def rotation():

        def fget(self):
            return self.view.rotation

        def fset(self, new_rot):

            self.view.rotation = new_rot
            self.phys_rep.rotation = new_rot

        return locals()

    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return self.view.position

        def fset(self, new_pos):

            self.view.position = new_pos
            self.phys_rep.position = new_pos

        return locals()

    @obengine.datatypes.nested_property
    def color():

        def fget(self):
            return self.view.color

        def fset(self, new_color):
            self.view.color = new_color

        return locals()

    @obengine.datatypes.nested_property
    def anchored():

        def fget(self):
            return self.phys_rep.anchored

        def fset(self, anchored):
            self.phys_rep.anchored = anchored

        return locals()

    @property
    def bounds(self):
        return self.view.bounds

    @obengine.deprecated.deprecated
    def set_size(self, size):
        self.size = size

    @obengine.deprecated.deprecated
    def set_hpr(self, hpr):
        self.rotation = hpr

    @obengine.deprecated.deprecated
    def set_pos(self, vector):
        self.position = vector

    @obengine.deprecated.deprecated
    def set_rgb(self, color):
        self.color = color

    def _on_add(self, world):

        self.world = world
        self.phys_rep.enable()

    def _on_remove(self):

        self.showing = False
        self.phys_rep.disable()


class XmlBrickExtension(XmlElementExtension):

    def __init__(self, brick):
        self._brick = brick

    @property
    def xml_element(self):

        attributes = {
        'name' : self._brick.name,
        'coords' : self._vector_str(self._brick.position),
        'rgb' : self._color_str(self._brick.color),
        'orientation' : self._euler_str(self._brick.rotation),
        'size' : self._vector_str(self._brick.size),
        'anchored' : self._bool_str(self._brick.anchored)
        }

        element = xmlparser.Element('brick', attributes)

        return element


class SkyboxElement(obengine.element.Element):

    def __init__(self, window, texture = None):

        obengine.element.Element.__init__(self, 'Skybox')
        self.set_extension('xml', XmlSkyboxExtension)

        self._window = window
        self._texture = texture

        # Create the skybox (although the actual model is currently a skysphere!)

        obengine.plugin.require('core.graphics')

        import obplugin.core.graphics

        self.view = obplugin.core.graphics.Model('sky', self._window, clickable = False, cast_shadows = False, compress = False)

        self.on_add += self.sky_on_add
        self.on_remove += self.sky_on_remove

    def sky_on_add(self, _):

        self.view.load()

        while self.view.load_okay is False:
            self._window.scheduler.step()

        self.view.scale = obengine.math.Vector(5000, 5000, 5000)

        # TODO: Replace the below code with something not Panda-specific!

        self.view.panda_node.reparentTo(base.camera)
        self.view.panda_node.setShaderOff()
        self.view.panda_node.setLightOff()
        self.view.panda_node.setFogOff()
        self.view.panda_node.setBin('background', 0)
        self.view.panda_node.setDepthWrite(False)
        self.view.panda_node.setEffect(CompassEffect.make(self._window.panda_window.render))

        # Did the user specify a texture?

        if self._texture:
            self.view.texture = self._texture

    def sky_on_remove(self):
        self.sky.hide()


class XmlSkyboxExtension(XmlElementExtension):

    def __init__(self, skybox):
        self._skybox = skybox

    @property
    def xml_element(self):

        attributes = {}

        if self._skybox._texture is not None:
            attributes['texture'] = self._skybox._texture

        element = xmlparser.Element('skybox', attributes)
        return element


class LightElement(obengine.element.Element):

    def __init__(self, name, window, light_type = None, color = None, position = None, rotation = None, cast_shadows = False):

        obengine.element.Element.__init__(self, name)
        self.set_extension('xml', XmlLightExtension)

        obengine.plugin.require('core.graphics')
        import obplugin.core.graphics

        light_type = light_type or obplugin.core.graphics.Light.DIRECTIONAL
        color = color or obengine.math.Color(255, 255, 255)
        rotation = rotation or obengine.math.EulerAngle()
        position = position or obengine.math.Vector()

        self._window = window
        self._light = obplugin.core.graphics.Light(
        light_type,
        name,
        window,
        color,
        position,
        rotation,
        cast_shadows)

        self._light.load()

    def look_at(self, object):
        self._light.look_at(object.view)

    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return self._light.position

        def fset(self, new_pos):
            self._light.position = new_pos

        return locals()

    @obengine.datatypes.nested_property
    def rotation():

        def fget(self):
            return self._light.rotation

        def fset(self, new_rot):
            self._light.rotation = new_rot

        return locals()

    @obengine.datatypes.nested_property
    def color():

        def fget(self):
            return self._light.color

        def fset(self, new_color):
            self._light.color = new_color

        return locals()

    @property
    def casting_shadows(self):
        return self._light.casting_shadows

    @property
    def light_type(self):
        return self._light.light_type


class XmlLightExtension(XmlElementExtension):

    def __init__(self, light):
        self._light = light

    @property
    def xml_element(self):

        attributes = {
                      'name' : self._light.name,
                      'rgb' : self._color_str(self._light.color),
                      'type' : self._light.light_type,
                      'orientation' : self._euler_str(self._light.rotation),
                      'coords' : self._vector_str(self._light.position),
                      'cast_shadows' : self._bool_str(self._light.casting_shadows)
                      }

        element = xmlparser.Element('light', attributes)
        return element


class ParticleElement(obengine.element.Element):

    def __init__(self, window, name):

        obengine.element.Element.__init__(self, name)

        obengine.plugin.require('core.graphics')
        import obplugin.core.graphics

        self._particle_generator = obplugin.core.graphics.ParticleEmitter(window)

    @obengine.datatypes.nested_property
    def particle_lifespan():

        def fget(self):
            return self._particle_generator.particle_lifespan

        def fset(self, new_lifespan):
            self._particle_generator.particle_lifespan = new_lifespan

        return locals()

    @obengine.datatypes.nested_property
    def particle_birthrate():

        def fget(self):
            return self._particle_generator.particle_birthrate

        def fset(self, new_birthrate):
            self._particle_generator.particle_birthrate = new_birthrate

        return locals()

    @obengine.datatypes.nested_property
    def particle_rise_velocity():

        def fget(self):
            return self._particle_generator.particle_rise_velocity

        def fset(self, new_rise_velocity):
            self._particle_generator.particle_rise_velocity = new_rise_velocity

        return locals()

    @obengine.datatypes.nested_property
    def particle_texture():

        def fget(self):
            return self._particle_generator.particle_texture.texture_path

        def fset(self, new_texture):

            import obplugin.core.graphics

            texture = obplugin.core.graphics.Texture(new_texture)
            texture.load()
            self._particle_generator.particle_texture = texture

        return locals()

    @obengine.datatypes.nested_property
    def disable_alpha():

        def fget(self):
            return self._particle_generator.disable_alpha

        def fset(self, disable_alpha):
            self._particle_generator.disable_alpha = disable_alpha

        return locals()


class CameraElement(obengine.element.Element):

    def __init__(self, window):

        obengine.element.Element.__init__(self, 'camera')

        obengine.plugin.require('core.graphics')
        import obplugin.core.graphics

        self.camera = obplugin.core.graphics.Camera(window)

    def look_at(self, element):
        self.camera.look_at(element.view.model)

    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return self.camera.position

        def fset(self, new_pos):
            self.camera.position = new_pos

        return locals()

    @obengine.datatypes.nested_property
    def rotation():

        def fget(self):
            return self.camera.rotation

        def fset(self, new_angle):
            self.camera.rotation = new_angle

        return locals()
