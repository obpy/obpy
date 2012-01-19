#
# <module description>
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
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
__date__ = "Jan 18, 2012 7:40:43 PM"


import xml.etree.ElementTree as xmlparser

import obengine.math
import obengine.plugin
import obengine.element
import obengine.elementfactory

from element_utils import XmlElementExtension


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


class LightMaker(obengine.element.ElementMaker):

    element_name = 'light'

    def set_window(self, window):
        self._window = window

    def make(self, name, type = None, color = None, position = None, rotation = None, cast_shadows = False):

        element = LightElement(name, self._window, type, color, position, rotation, cast_shadows)
        return element


obengine.elementfactory.ElementFactory.register_element_factory(LightMaker)


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
