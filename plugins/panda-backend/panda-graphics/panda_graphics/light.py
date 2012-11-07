#
# <module description>
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
#
# Copyright (C) 2012 The OpenBlox Project
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
__date__ = "Jul 19, 2012 6:02:13 PM"


from panda3d.core import DirectionalLight, AmbientLight, PointLight

import obengine.math
import obengine.event
import obengine.datatypes
import obengine.log
import obplugin.panda_utils


class Light(obplugin.panda_utils.PandaResource):
    """
    Represents a Panda3D light.
    Currently, only directional, point, and ambient lights are implemented.
    """

    DIRECTIONAL = 'directional'
    AMBIENT = 'ambient'
    POINT = 'point'

    def __init__(self, light_type, name, window, color = obengine.math.Color(255, 255, 255, 255), position = obengine.math.Vector(0, 0, 0), rotation = obengine.math.EulerAngle(0, 0, 0), cast_shadows = False):
        """Creates a new light
        Arguments:
         * light_type - either Light.DIRECTIONAL for a directional light,
                        Light.AMBIENT for an ambient light, or Light.POINT for
                        a point light
         * name - specifies the name of this light on the Panda scene graph.
                  If you're doing any low-level Panda work, remember this!
         * color - the color cast by this light
         * cast_shadows - whether this light can cast shadows. Only directional lights can.
                          Also, this isn't supported on Intel graphics cards
         * rotation - the rotation of this light. For obvious reasons, this only applies to
                      directional lights
        """

        obplugin.panda_utils.PandaResource.__init__(self)

        self._name = name
        self._color = color
        self._light_type = light_type
        self._casting_shadows = cast_shadows
        self._rotation = rotation
        self._position = position
        self._window = window

        if light_type not in (Light.DIRECTIONAL, Light.AMBIENT, Light.POINT):
            raise ValueError('Unknown light type "%s"' % light_type)

    def load(self):
        """Loads this light
        Note that this is actually a synchronous method, but for transparency reasons,
        you should wait for Light's on_loaded event instead.
        """

        if self._light_type == Light.DIRECTIONAL:
            self._init_directional_light()

        elif self._light_type == Light.AMBIENT:
            self._init_ambient_light()

        elif self._light_type == Light.POINT:
            self._init_point_light()

        self.panda_node = self._window.panda_window.render.attachNewNode(self.panda_light)
        base.render.setLight(self.panda_node)

        self.color = self.color
        self.rotation = self.rotation

        if self._light_type == Light.POINT:
            self.position = self.position

        if self._light_type == Light.DIRECTIONAL:

            shadow_override = obengine.cfg.Config().get_bool('use-shadows', 'core.gfx', False)
            if self._casting_shadows is True and shadow_override is True:
                self._enable_shadows()

        self.on_loaded()

    def look_at(self, obj):
        """Points the light at obj
        Currently, obj can only be a directional or point light,
        or a model.
        """

        if hasattr(obj, 'panda_node'):
            self.panda_node.lookAt(obj.panda_node)

        else:
            raise ValueError('class %s does not contain a valid Panda3D scene graph node' % obj.__class__.__name__)

    @property
    def light_type(self):
        return self._light_type

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):

        if isinstance(color, tuple):
            color = obengine.math.Color(*color)

        self._color = color
        self.panda_light.setColor(self.convert_color(color))

    @property
    def name(self):
        return self._name

    @property
    def casting_shadows(self):
        return self._casting_shadows

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rot):

        if isinstance(rot, tuple):
            self._rotation = obengine.math.EulerAngle(*rot)

        else:
            self._rotation = rot

        self.panda_node.setHpr(*self.convert_euler_angle(self._rotation))

    @obengine.datatypes.nested_property
    def position():

        def fget(self):

            if self._light_type != Light.POINT:
                obengine.log.warn('Tried to retrieve position of non-point light')

            return obplugin.panda_utils.PandaConverter.convert_vec3(self.panda_node.getPos())

        def fset(self, new_pos):

            if self._light_type != Light.POINT:
                obengine.log.warn('Tried to set position of non-point light')

            if isinstance(new_pos, tuple):
                self._position = obengine.math.Vector(*new_pos)

            else:
                self._position = new_pos

            self.panda_node.setPos(obplugin.panda_utils.PandaConverter.convert_vector(self._position))

        return locals()

    def _init_directional_light(self):
        self.panda_light = DirectionalLight(self._name)

    def _init_ambient_light(self):

        self.panda_light = AmbientLight(self._name)

        if self._casting_shadows is True:
            obengine.utils.warn('Tried to turn on shadows for an ambient light')

    def _init_point_light(self):
        self.panda_light = PointLight(self._name)

    def _enable_shadows(self):
        print 'FIXME: add shadows'
