"""
Copyright (C) 2011 The OpenBlox Project

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
__date__ ="$May 2, 2011 5:37:04 PM$"

from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

import obengine.depman
import obengine.cfg
import obengine.log
import obengine.event
import obengine.async
import obengine.vfs

import obengine.gfx.math

obengine.depman.gendeps()


COLOR_SCALER = 255.0
RENDER_PRIORITY = 10

def init():

    # We have to retrieve graphics-specific configuration things first. Why?
    # Panda3D requires you to set all data concerning frame rate and the like *before*
    # you create a window
    _setup_config_values()

    # In case you're wondering why this variable isn't used, it's because
    # ShowBase's constructor assigns a lot of stuff to the __builtin__ namespace
    show_base = ShowBase()

    # Initalize the window, now that we've set it up
    _setup_window()

    obengine.async.scheduler.add(obengine.async.LoopingCall(taskMgr.step, priority = RENDER_PRIORITY))

class PandaResource(object):
    """
    Base resource class containing various OpenBlox-to-Panda3D conversion utilities.
    It also provides a common, garunteed interface for all Panda3D resources
    """

    def __init__(self):
        self.on_loaded = obengine.event.Event()

    def panda_path(self, path):
        
        if obengine.vfs.SEPERATOR in path:
            return Filename.fromOsSpecific(obengine.vfs.getsyspath(path))

        else:
            return path

    def convert_color(self, color):
        return Vec4(*map(lambda i : i / COLOR_SCALER, [color.r, color.g, color.b, color.a]))

    def convert_vector(self, vector):
        return Vec3(vector.x, vector.y, vector.z)

    def convert_euler_angle(self, angle):
        return [angle.h, angle.p, angle.r]

class Model(PandaResource):
    """
    Represents a Panda3D model.
    NOTE: UV textures loaded at runtime are currently NOT supported!
    
    """

    def __init__(self, model_path, position = None, rotation = None, scale = None, color = None):

        PandaResource.__init__(self)

        self.model_path = model_path
        self.panda_model_path = self.panda_path(model_path)

        self.panda_node = None

        self.load_okay = False
        
        self._showing = False
        self._texture = None

        self._position = position or obengine.gfx.math.Vector()
        self._setup_position()

        self._color = color or obengine.gfx.math.Color()
        self._setup_color()

        self._rotation = rotation or obengine.gfx.math.EulerAngle()
        self._setup_rotation()

        self._scale = scale or obengine.gfx.math.Vector()
        self._setup_scale()

    def load(self):
        """
        Loads this model.
        Note that instead of waiting for this method to return,
        listen for this Model's on_loaded event. When that event is fired,
        the model is ready to be used.
        """
        
        loader.loadModel(self.panda_model_path, callback = self._set_load_okay)

    @property
    def showing(self):
        return self._showing

    @showing.setter
    def showing(self, val):

        if val == True:
            self.panda_node.reparentTo(base.render)

        elif val == False:
            self.panda_node.detachNode()

        else:
            raise ValueError('val must be either True or False (was %s)' % val)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, pos):

        if isinstance(pos, tuple):

            self._position = obengine.gfx.math.Vector(*pos)
            self.panda_node.setPos(self.convert_vector(self._position))

        else:

            self._position.x = pos.x
            self._position.y = pos.y
            self._position.z = pos.z

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):

        if isinstance(scale, tuple):

            self._scale = obengine.gfx.math.Vector(*scale)
            self.panda_node.setScale(self.convert_vector(self._scale))

        else:

            self._scale.x = scale.x
            self._scale.y = scale.y
            self._scale.z = scale.z

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rot):

        if isinstance(rot, tuple):

            self._rotation = rot
            self.panda_node.setHpr(*self.convert_euler_angle(self._rotation))

        else:

            self._rotation.h = rot.h
            self._rotation.p = rot.p
            self._rotation.r = rot.r

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):

        if isinstance(color, tuple):

            self._color = obengine.gfx.math.Color(*color)
            self.panda_node.setColor(self.convert_color(self._color))

        else:

            self._color.r = color.r
            self._color.g = color.g
            self._color.b = color.b
            self._color.a = color.a

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, tex):

        self._texture = tex
        self.panda_node.setTexture(tex.texture)

    def _setup_position(self):

        self._position.on_x_changed += lambda x: self.panda_node.setX(x)
        self._position.on_y_changed += lambda y: self.panda_node.setY(y)
        self._position.on_z_changed += lambda z: self.panda_node.setX(z)

    def _setup_scale(self):

        self._scale.on_x_changed += lambda x: self.panda_node.setScale(self._scale.x, self._scale.y, self._scale.z)
        self._scale.on_y_changed += lambda y: self.panda_node.setScale(self._scale.x, self._scale.y, self._scale.z)
        self._scale.on_z_changed += lambda z: self.panda_node.setScale(self._scale.x, self._scale.y, self._scale.z)

    def _setup_rotation(self):

        self._rotation.on_h_changed += lambda h: self.panda_node.setH(h)
        self._rotation.on_p_changed += lambda p: self.panda_node.setP(p)
        self._rotation.on_r_changed += lambda r: self.panda_node.setR(r)

    def _setup_color(self):

        self._color.on_r_changed += lambda r: self.panda_node.setR(r / COLOR_SCALER)
        self._color.on_g_changed += lambda g: self.panda_node.setG(g / COLOR_SCALER)
        self._color.on_b_changed += lambda b: self.panda_node.setB(r / COLOR_SCALER)

    def _set_load_okay(self, model):

        self.load_okay = True
        
        self.panda_node = model
        self.panda_node.setTransparency(TransparencyAttrib.MAlpha)
        
        self.on_loaded()

class Texture(PandaResource):
    """
    Represents a Panda3D texture.
    Supported image formats:
     * .png
     * .jpeg/.jpg
     * .gif (no animations)
     * .tif
     * .bmp
    """

    def __init__(self, texture_path):

        self.texture_path
        self.panda_texture_path = self.panda_path(texture_path)

        self.texture = None

    def load(self):
        """
        Loads this texture.
        Instead of waiting for this method to return, wait for Texture's
        on_loaded event. When that event is fired, the texture is ready to be used.
        """


        loader.loadTexture(self.panda_texture_path, callback = self.on_loaded)

    def _set_load_okay(self, tex):
        self.texture = tex

class Light(PandaResource):
    """
    Represents a Panda3D light.
    Currently, only directional and ambient lights are implemented.
    """

    DIRECTIONAL = 'directional'
    AMBIENT = 'ambient'

    def __init__(self, light_type, name, color = obengine.gfx.math.Color(255, 255, 255, 255), cast_shadows = False, rotation = obengine.gfx.math.EulerAngle(0, 0, 0)):
        """
        Arguments:
         * light_type - either Light.DIRECTIONAL for a directional light, or
                        Light.AMBIENT for an ambient light
         * name - specifies the name of this light on the Panda scene graph.
                  If you're doing any low-level Panda work, remember this!
         * color - the color cast by this light
         * cast_shadows - whether this light can cast shadows. Only directional lights can.
                          Also, this isn't supported on Intel graphics cards
         * rotation - the rotation of this light. For obvious reasons, this only applies to
                      directional lights
        """

        PandaResource.__init__(self)

        self._name = name
        self._color = color
        self._casting_shadows = cast_shadows
        self._light_type = light_type
        self._rotation = rotation

        if light_type not in [Light.DIRECTIONAL, Light.AMBIENT]:
            raise ValueError('Unknown light type "%s"' % light_type)

    def load(self):
        """
        Loads this light.
        Note that this is actually a synchronous method, but for transparency reasons,
        you should wait for Light's on_loaded event instead.
        """

        if self._light_type == Light.DIRECTIONAL:
            self._init_directional_light()

        elif self._light_type == Light.AMBIENT:
            self._init_ambient_light()

        self.panda_node = base.render.attachNewNode(self.panda_light)
        base.render.setLight(self.panda_node)

        self.on_loaded()

    def look_at(self, obj):
        """
        Points the light at obj. Currently, obj can only be a directional light
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
            color = obengine.gfx.math.Color(*color)

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
            self._rotation = obengine.gfx.math.EulerAngle(*rot)

        else:
            self._rotation = rot

        self.panda_light.setHpr(self.convert_euler_angle(self._rotation))

    def _init_directional_light(self):

        self.panda_light = DirectionalLight(self._name)
        self.panda_light.setColor(self.convert_color(self._color))

        if self._casting_shadows == True:
            self.panda_light.setShadowCaster(True, 512, 512)

    def _init_ambient_light(self):

        self.panda_light = AmbientLight(self._name)
        self.panda_light.setColor(self.convert_color(self._color))

        if self._casting_shadows == True:
            obengine.utils.warn('Tried to turn on shadows for an ambient light')

def _setup_window():

    base.setBackgroundColor(1, 1, 1, 1)
    base.render.setShaderAuto()

def _setup_config_values():

    obengine.log.debug('Initalizing Panda3D render window')

    # Get the frame rate
    frame_rate = obengine.cfg.get_config_var('frame-rate')

    # Should we show the frame rate?
    show_frame_rate = int(obengine.cfg.get_config_var('show-frame-rate'))

    # Get the requested resolution
    resolution = ' '.join(obengine.cfg.get_config_var('resolution').split('x'))

    datadir = obengine.cfg.get_config_var('datadir')

    obengine.log.debug('Frame rate = %s FPS' % frame_rate)
    obengine.log.debug('%s' % bool(show_frame_rate) and 'Showing frame rate' or 'Not showing frame rate')

    # Mount the data directory
    obengine.vfs.mount('/data', obengine.vfs.RealFS(datadir))

    # Has the user specified any extra paths?
    # If so, add them, too
    try:
        user_paths = obengine.cfg.get_config_var('data-paths').split()

    except KeyError:
        user_paths = []

    data_paths = [datadir] + user_paths
    obengine.log.debug('Model path: %s' % ','.join(data_paths))

    # Now, we can actually give the configuration values to Panda!

    loadPrcFileData('', 'show-frame-rate-meter %s' % show_frame_rate)
    loadPrcFileData('', 'win-size %s' % resolution)

    for path in data_paths:
        loadPrcFileData('','model-path %s' % path)

    # Set the frame rate

    global_clock = ClockObject.getGlobalClock()
    global_clock.setMode(ClockObject.MLimited)
    global_clock.setFrameRate(frame_rate)