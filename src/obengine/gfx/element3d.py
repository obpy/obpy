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
import obengine.depman
obengine.depman.gendeps()


def init():
    obengine.plugin.require('core.graphics')


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
