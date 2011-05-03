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

import obengine.cfg
import obengine.event
import obengine.async
import obengine.vfs

import obengine.gfx.math

COLOR_SCALER = 255.0

def init():

    global show_base

    _setup_config_values()

    show_base = ShowBase()

    _setup_lights()
    _setup_window()

    scheduler.add(obengine.async.PeriodicTask(taskMgr.step, 1 / obengine.cfg.get_config_var('frame-rate')))

class PandaResource(object):

    def __init__(self):
        self.on_loaded = obengine.event.Event()

    def panda_path(self, path):
        return Filename(Filename.fromOsSpecific(obengine.vfs.getsyspath(path)))

class Model(PandaResource):

    def __init__(self, model_path, position = None, rotation = None, scale = None, color = None):

        PandaResource.__init__(self)

        self.model_path = model_path
        self.panda_model_path = self.panda_path(model_path)

        self.model = None
        
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

    def hide(self):
        self.model.detachNode()

    def load(self):
        self.model = loader.loadModel(self.model_path, callback = self.on_loaded)

    @property
    def showing(self):
        return self._showing

    @showing.setter
    def showing(self, val):

        if val == True:
            self.model.reparentTo(base.render)

        elif val == False:
            self.model.detachNode()

        else:
            raise ValueError('val must be either True or False (was %s)' % val)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, *args):
        
        if len(args) == 1:
            self._position = args[0]

        else:

            self._position.x = args[0]
            self._position.y = args[1]
            self._position.z = args[2]

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, *args):

        if len(args) == 1:
            self._position = args[0]

        else:

            self._position.x = args[0]
            self._position.y = args[1]
            self._position.z = args[2]

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, *args):

        if len(args) == 1:
            self._scale = args[0]

        else:

            self._scale.x = args[0]
            self._scale.y = args[1]
            self._scale.z = args[2]

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, *args):

        if len(args) == 1:
            self._rotation = args[0]

        else:

            self._rotation.h = args[0]
            self._rotation.p = args[1]
            self._rotation.r = args[2]

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, *args):

        if len(args) == 1:
            self._color = args[0]

        else:

            self._color.r = args[0]
            self._color.g = args[1]
            self._color.b = args[2]
            self._color.a = args[3]

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, tex):

        self._texture = tex
        self.model.setTexture(tex.texture)

    def _setup_position(self):

        self._position.on_x_changed += lambda x: self.model.setX(x)
        self._position.on_y_changed += lambda y: self.model.setY(y)
        self._position.on_z_changed += lambda z: self.model.setX(z)

    def _setup_scale(self):

        self._scale.on_x_changed += lambda x: self.model.setScale(self._scale.x, self._scale.y, self._scale.z)
        self._scale.on_y_changed += lambda y: self.model.setScale(self._scale.x, self._scale.y, self._scale.z)
        self._scale.on_z_changed += lambda z: self.model.setScale(self._scale.x, self._scale.y, self._scale.z)

    def _setup_rotation(self):

        self._rotation.on_h_changed += lambda h: self.model.setH(h)
        self._rotation.on_p_changed += lambda p: self.model.setP(p)
        self._rotation.on_r_changed += lambda r: self.model.setR(r)

    def _setup_color(self):

        self._color.on_r_changed += lambda r: self.model.setR(r / COLOR_SCALER)
        self._color.on_g_changed += lambda g: self.model.setG(g / COLOR_SCALER)
        self._color.on_b_changed += lambda b: self.model.setB(r / COLOR_SCALER)

class Texture(PandaResource):

    def __init__(self, texture_path):

        self.texture_path
        self.panda_texture_path = self.panda_path(texture_path)

        self.texture = None

    def load(self):
        self.texture = loader.loadTexture(self.panda_texture_path, callback = self.on_loaded)

def _setup_window():
    base.setBackgroundColor(1, 1, 1, 1)

def _setup_config_values():

    frame_rate = obengine.cfg.get_config_var('frame-rate')
    show_frame_rate = {True : '#t', False : '#f'}[obengine.cfg.get_config_var('show-frame-rate')]
    resolution = ' '.join(obengine.cfg.get_config_var('resolution').split('x'))

    datadir = obengine.cfg.get_config_var('datadir')
    obengine.vfs.mount('/data', obengine.vfs.RealFS(datadir))

    try:
        user_paths = obengine.cfg.get_config_var('data-paths').split()

    except KeyError:
        user_paths = []

    data_paths = [datadir] + user_paths

    loadPrcFileData('show-frame-rate-meter %s' % show_frame_rate)
    loadPrcFileData('win-size %s' % resolution)

    for path in data_paths:
        loadPrcFileData('model-path %s' % path)

    global_clock = ClockObject.getGlobalClock()
    global_clock.setMode(ClockObject.MLimited)
    global_clock.setFrameRate(frame_rate)

def _setup_lights():

    ambient_light = AmbientLight('AmbientLight')
    ambient_light.setColor(Vec4(0.2, 0.2, 0.2, 1))

    sun_light = DirectionalLight("Sunlight")
    sun_light.setColor(Vec4(0.8, 0.8, 0.8, 1))

    if obengine.cfg.get_config_var('use-shadows') is True:
        sun_light.setShadowCaster(True, 512, 512)

    sun_node = rootwin.render.attachNewNode(sunlight)
    sun_node.lookAt(0, 0, 0)

    base.render.setLight(sun_node)
    base.render.setLight(base.render.attachNewNode(ambient_light))