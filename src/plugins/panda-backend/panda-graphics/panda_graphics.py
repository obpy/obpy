#
# This plugin provides a Panda3D-based 3D graphics implementation.
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
__date__ = "$May 2, 2011 5:37:04 PM$"


import uuid

from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

import obengine.cfg
import obengine.log
import obengine.event
import obengine.async
import obengine.vfs
import obengine.plugin
import obengine.gfx.math
from obplugin.panda_utils import PandaResource, PandaConverter, COLOR_SCALER
from obplugin.panda_hardware import MouseEvent


CLICKABLE_BITMASK = BitMask32(0x101)

# TODO: Get rid of the need for this variable - it's very ugly!
loaded_models = {}


class Model(PandaResource):
    """
    Represents a Panda3D model.
    NOTE: Textures loaded at runtime are currently NOT supported!
    
    """

    def __init__(self, model_path, window, position = None, rotation = None, scale = None, color = None, clickable = True):

        PandaResource.__init__(self)

        self.model_path = model_path
        self.panda_model_path = self.panda_path(model_path)
        self.panda_node = None
        self.load_okay = False
        self.window = window
        self._showing = False
        self.on_click = obengine.event.Event()

        self._texture = None
        self._parent = None
        self._position = position or obengine.gfx.math.Vector()
        self._setup_position()
        self._color = color or obengine.gfx.math.Color()
        self._setup_color()
        self._rotation = rotation or obengine.gfx.math.EulerAngle()
        self._setup_rotation()
        self._scale = scale or obengine.gfx.math.Vector()
        self._setup_scale()

        self._clickable = clickable

    def load(self, async = True):
        """
        Loads this model.
        Note that instead of waiting for this method to return,
        listen for this Model's on_loaded event. When that event is fired,
        the model is ready to be used.
        """

        self.window.panda_window.loader.loadModel(self.panda_model_path, callback = self._set_load_okay)

    @property
    def bounds(self):

        point1, point2 = self.panda_node.calcTightBounds()
        point1 = PandaConverter.convert_vec3(point1)
        point2 = PandaConverter.convert_vec3(point2)
#
#        point3 = obengine.gfx.math.Vector(point1.x, point2.y, point1.z)
#        point4 = obengine.gfx.math.Vector(point2.x, point1.y, point2.z)

        return point1, point2

    @property
    def showing(self):
        return self._showing

    @showing.setter
    def showing(self, val):

        if val is True:
            self.panda_node.reparentTo(self.window.panda_window.render)

        elif val is False:
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

        else:

            self._color.r = color.r
            self._color.g = color.g
            self._color.b = color.b
            self._color.a = color.a

        self.panda_node.setColor(self.convert_color(self._color))

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, tex):

        self._texture = tex
        self.panda_node.setTexture(tex.texture)

    @obengine.datatypes.nested_property
    def parent():

        def fget(self):
            return self._parent

        def fset(self, parent):

            self._parent = parent
            self.panda_node.reparentTo(parent.panda_node)

        return locals()

    def _setup_position(self):

        self._position.on_x_changed += lambda x: self.panda_node.setX(x)
        self._position.on_y_changed += lambda y: self.panda_node.setY(y)
        self._position.on_z_changed += lambda z: self.panda_node.setZ(z)

    def _setup_scale(self):

        self._scale.on_x_changed += lambda x: self.panda_node.setScale(self._scale.x, self._scale.y, self._scale.z)
        self._scale.on_y_changed += lambda y: self.panda_node.setScale(self._scale.x, self._scale.y, self._scale.z)
        self._scale.on_z_changed += lambda z: self.panda_node.setScale(self._scale.x, self._scale.y, self._scale.z)

    def _setup_rotation(self):

        self._rotation.on_h_changed += lambda h: self.panda_node.setH(h)
        self._rotation.on_p_changed += lambda p: self.panda_node.setP(p)
        self._rotation.on_r_changed += lambda r: self.panda_node.setR(r)

    def _setup_color(self):

        self._color.on_r_changed += lambda r: self.panda_node.setColor(r / COLOR_SCALER, self._color.g, self._color.b)
        self._color.on_g_changed += lambda g: self.panda_node.setColor(self._color.r, self._color.b, g / COLOR_SCALER)
        self._color.on_b_changed += lambda b: self.panda_node.setColor(b / COLOR_SCALER, self._color.g, self._color.b)

    def _check_mouse(self):

        if self.window.panda_window.mouseWatcherNode.hasMouse() is False:
            return

        mouse_pos = self.window.panda_window.mouseWatcherNode.getMouse()
        self.window.picker_ray.setFromLens(
        self.window.panda_window.camNode,
        mouse_pos.getX(),
        mouse_pos.getY())

        self.window.mouse_traverser.traverse(self.window.panda_window.render)

        if self.window.collision_queue.getNumEntries() > 0:

            self.window.collision_queue.sortEntries()
            picked_node = self.window.collision_queue.getEntry(0).getIntoNodePath().findNetTag('clickable-flag')

            picked_node_uuid = picked_node.getTag('clickable-flag')

            if picked_node_uuid == self._uuid:
                self.on_click()

    def _set_load_okay(self, model):

        self.load_okay = True
        self._uuid = str(uuid.uuid1())
        loaded_models[self._uuid] = self

        self.panda_node = model
        self.panda_node.setTransparency(TransparencyAttrib.MAlpha)
        self.panda_node.setTag('clickable-flag', self._uuid)
        self.showing = True

        if self._clickable is True:
            self.panda_node.setCollideMask(CLICKABLE_BITMASK)

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

        loader.loadTexture(self.panda_texture_path, callback = self._set_load_okay)

    def _set_load_okay(self, tex):

        self.texture = tex
        self.on_loaded()


class Light(PandaResource):
    """
    Represents a Panda3D light.
    Currently, only directional and ambient lights are implemented.
    """

    DIRECTIONAL = 'directional'
    AMBIENT = 'ambient'

    def __init__(self, light_type, name, window, color = obengine.gfx.math.Color(255, 255, 255, 255), rotation = obengine.gfx.math.EulerAngle(0, 0, 0), cast_shadows = False):
        """Creates a new light
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
        self._window = window

        if light_type not in [Light.DIRECTIONAL, Light.AMBIENT]:
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

        self.panda_node = self._window.panda_window.render.attachNewNode(self.panda_light)
        base.render.setLight(self.panda_node)

        self.on_loaded()

    def look_at(self, obj):
        """Points the light at obj
        Currently, obj can only be a directional light
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


class Window(object):

    RENDER_PRIORITY = 10
    LOAD_PRIORITY = 25

    def __init__(self, window_title, scheduler):

        self.on_loaded = obengine.event.Event()
        self._config_src = obengine.cfg.Config()
        self._title = window_title
        self.scheduler = scheduler

        self._on_mouse_clicked = obengine.event.Event()

    def start_rendering(self):
        self.scheduler.add(obengine.async.LoopingCall(self.panda_window.taskMgr.step, priority = Window.RENDER_PRIORITY))

    def load(self):
        self.scheduler.add(obengine.async.Task(self._actual_load, priority = Window.LOAD_PRIORITY))

    @obengine.datatypes.nested_property
    def title():

        def fget(self):
            return self._title

        def fset(self, new_title):

            self._title = new_title
            self.window_properties.setTitle(self._title)

        return locals()

    def _actual_load(self, task):

        self.frame_rate = self._config_src.get_int('frame-rate', 'core.gfx')
        self.show_frame_rate = self._config_src.get_bool('show-frame-rate', 'core.gfx')
        self.resolution = map(int, self._config_src.get_str('resolution', 'core.gfx').split('x'))
        self.search_path = self._config_src.get_str('cfgdir') + '/data'

        self.clock = ClockObject.getGlobalClock()
        self.clock.setMode(ClockObject.MLimited)
        self.clock.setFrameRate(self.frame_rate)

        self.window_properties = WindowProperties()
        self.window_properties.setSize(*self.resolution)
        self.window_properties.setTitle(self._title)

        self.panda_window = ShowBase()
        self.panda_window.setFrameRateMeter(self.show_frame_rate)
        self.panda_window.setBackgroundColor(1, 1, 1, 1)
        self.panda_window.win.requestProperties(self.window_properties)
        self.panda_window.render.setShaderAuto()

        picker_node = CollisionNode('mouse_ray')
        picker_nodepath = self.panda_window.camera.attachNewNode(picker_node)
        picker_node.setFromCollideMask(CLICKABLE_BITMASK)
        self.picker_ray = CollisionRay()
        picker_node.addSolid(self.picker_ray)
        self.mouse_traverser = CollisionTraverser()
        self.collision_queue = CollisionHandlerQueue()
        self.mouse_traverser.addCollider(picker_nodepath, self.collision_queue)
        mouse_button = MouseEvent.LEFT_MOUSE
        mouse_event_type = MouseEvent.TYPE_DOWN
        self._click_event = MouseEvent(
                                       self,
                                       mouse_button,
                                       mouse_event_type)
        self._click_event += self._pick_mouse

        getModelPath().appendPath(self.search_path)
        self.on_loaded()

        return task.STOP

    def _pick_mouse(self):

        if self.panda_window.mouseWatcherNode.hasMouse() is False:
            return

        mouse = self.panda_window.mouseWatcherNode.getMouse()
        self.picker_ray.setFromLens(self.panda_window.camNode, mouse.getX(), mouse.getY())

        self.mouse_traverser.traverse(self.panda_window.render)

        if self.collision_queue.getNumEntries() > 0:

            self.collision_queue.sortEntries()
            picked_node = self.collision_queue.getEntry(0).getIntoNodePath().findNetTag('clickable-flag')

            loaded_models[picked_node.getTag('clickable-flag')].on_click()



class Camera(object):

    def __init__(self, window):

        self.on_loaded = obengine.event.Event()

        self.window = window
        self.camera = self.window.panda_window.camera
        self.panda_node = self.camera

    def load(self):
        self.on_loaded()

    def look_at(self, model):
        self.camera.lookAt(model.panda_node)

    @property
    def position(self):

        cam_vec = self.camera.getPos()
        return obengine.gfx.math.Vector(cam_vec.getX(), cam_vec.getY(), cam_vec.getZ())

    @position.setter
    def position(self, pos):

        if isinstance(pos, tuple):
            pos = obengine.gfx.math.Vector(*pos)

        self.camera.setPos(pos.x, pos.y, pos.z)

    @obengine.datatypes.nested_property
    def rotation():

        def fget(self):
            return PandaConverter.convert_quat(self.camera.getQuat())

        def fset(self, new_angle):

            quat = PandaConvert.convert_angle(new_angle)
            self.camera.setQuat(quat)

        return locals()
