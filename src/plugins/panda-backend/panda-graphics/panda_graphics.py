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
import math

import panda3d.core
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.filter.CommonFilters import *

import shadow

import obengine.datatypes
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

    on_model_loaded = obengine.event.Event()

    def __init__(self, model_path, window, position = None, rotation = None, scale = None, color = None, clickable = True, cast_shadows = True):

        PandaResource.__init__(self)

        self.model_path = model_path
        self.panda_model_path = self.panda_path(model_path)
        self.panda_node = None
        self.load_okay = False
        self.window = window
        self._showing = False
        self.on_click = obengine.event.Event()
        self.cast_shadows = cast_shadows

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

    @obengine.datatypes.nested_property
    def position():

    	def fget(self):
    	    return self._position

    	def fset(self, pos):

    	    if isinstance(pos, tuple):
    		      self._position = obengine.gfx.math.Vector(*pos)
    		      self.panda_node.setPos(self.convert_vector(self._position))

    	    else:
    		      self._position.x = pos.x
    		      self._position.y = pos.y
    		      self._position.z = pos.z

        return locals()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, new_scale):

        if isinstance(new_scale, tuple):

            self._scale = obengine.gfx.math.Vector(*new_scale)
            self.panda_node.setScale(*self.convert_vector(self._scale))

        else:

            self._scale.x = new_scale.x
            self._scale.y = new_scale.y
            self._scale.z = new_scale.z

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

        Model.on_model_loaded(self)
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
    Currently, only directional, point, and ambient lights are implemented.
    """

    DIRECTIONAL = 'directional'
    AMBIENT = 'ambient'
    POINT = 'point'

    def __init__(self, light_type, name, window, color = obengine.gfx.math.Color(255, 255, 255, 255), position = obengine.gfx.math.Vector(0, 0, 0), rotation = obengine.gfx.math.EulerAngle(0, 0, 0), cast_shadows = False):
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

        PandaResource.__init__(self)

        self._name = name
        self._color = color
        self._casting_shadows = cast_shadows
        self._light_type = light_type
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

        if self._light_type != Light.AMBIENT:

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

        self.panda_node.setHpr(*self.convert_euler_angle(self._rotation))

    @obengine.datatypes.nested_property
    def position():

        def fget(self):

            if self._light_type != Light.POINT:
                obengine.log.warn('Tried to retrieve position of non-point light')

            return PandaConverter.convert_vec3(self.panda_node.getPos())

        def fset(self, new_pos):

            if self._light_type != Light.POINT:
                obengine.log.warn('Tried to set position of non-point light')

            if isinstance(new_pos, tuple):
                self._position = obengine.gfx.math.Vector(*new_pos)

            else:
                self._position = new_pos

            self.panda_node.setPos(PandaConverter.convert_vector(self._position))

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

        window_properties = WindowProperties.size(512, 512)
        frame_buffer_properties = FrameBufferProperties()
        frame_buffer_properties.setRgbColor(1)
        frame_buffer_properties.setAlphaBits(1)
        frame_buffer_properties.setDepthBits(1)

        shadow_buffer = self._window.panda_window.graphicsEngine.makeOutput(
                                                                            base.pipe,
                                                                            'offscreen buffer',
                                                                            - 2,
                                                                            frame_buffer_properties,
                                                                            window_properties,
                                                                            GraphicsPipe.BFRefuseWindow,
                                                                            self._window.panda_window.win.getGsg(),
                                                                            self._window.panda_window.win
                                                                            )
        if shadow_buffer is None:
            return

        shadow_map = panda3d.core.Texture()
        shadow_buffer.addRenderTexture(shadow_map,
                                       GraphicsOutput.RTMBindOrCopy,
                                       GraphicsOutput.RTPColor)

        self._shadow_camera = base.makeCamera(shadow_buffer)
        self._shadow_camera.reparentTo(render)
        self._shadow_camera.node().setScene(render)
        shadow_cam_lens = OrthographicLens()
#        shadow_cam_lens.setFov(70)
        shadow_cam_lens.setNearFar(0, 500)
        shadow_cam_lens.setFilmSize(100, 100)
        self._shadow_camera.node().setLens(shadow_cam_lens)
        self._shadow_camera.setPos(self._get_position())
        self._shadow_camera.lookAt(0, 0, 0)

        render.setShaderInput('light', self._shadow_camera)
        render.setShaderInput('Ldepthmap', shadow_map)
        AMBIENT = 0.0
        render.setShaderInput('ambient',
                                           AMBIENT,
                                           1.0, 1.0, 0.0)
        #render.setShaderInput('texDisable', 0, 0, 0, 1)
        render.setShaderInput('scale', 1, 1, 1, 1)
        SHADOW_PUSH_BIAS = 0.70
        render.setShaderInput('push',
                               SHADOW_PUSH_BIAS,
                               SHADOW_PUSH_BIAS,
                               SHADOW_PUSH_BIAS,
                               0)

        lci = NodePath(PandaNode("Light Camera Initializer"))
        shadow_caster_shader = self._window.panda_window.loader.loadShader('shadow-caster.sha')
        lci.setShader(shadow_caster_shader)
        self._shadow_camera.node().setInitialState(lci.getState())

#        self._shadows = []
#        self._shadowed_models = []
#        self._shadowed_model_positions = []
#        self._shadowed_model_rotations = []
#
#        Model.on_model_loaded += self._add_shadow
#        self._window.scheduler.add(obengine.async.LoopingCall(self._update_shadows))

    def _add_shadow(self, model):

        if model.cast_shadows is False:
            return

        infinite_dist = self.light_type == Light.DIRECTIONAL
        shadow_geom = shadow.Shadow(model.panda_node, self.panda_node, infinite_dist)

        self._shadows.append(shadow_geom)
        self._shadowed_models.append(model)

        shadow_geom.generate()

    def _update_shadows(self):

        for index, shadow in enumerate(self._shadows):

            current_model_pos = str(self._shadowed_models[index].position)
            current_model_rotation = str(self._shadowed_models[index].rotation)

            try:
                prev_model_pos = self._shadowed_model_positions[index]
                prev_model_rotation = self._shadowed_model_rotations[index]

            except IndexError:

                self._shadowed_model_positions.append(str(self._shadowed_models[index].position))
                self._shadowed_model_rotations.append(str(self._shadowed_models[index].rotation))

                prev_model_pos = ''
                prev_model_rotation = ''

            if current_model_pos != prev_model_pos or current_model_rotation != prev_model_rotation:

                self._shadowed_model_positions[index] = current_model_pos
                self._shadowed_model_rotations[index] = current_model_rotation

                shadow.generate()

    def _get_position(self):

        hpr = self.panda_node.getHpr()

        hpr.setX(hpr.getX() * math.pi / 180)
        hpr.setY(hpr.getY() * math.pi / 180)
        hpr.setZ(hpr.getZ() * math.pi / 180)

        l = Vec3(math.cos(hpr.getX()) * math.cos(hpr.getY()),
                 math.sin(hpr.getX()) * math.cos(hpr.getY()),
                 math.sin(hpr.getY()))

        VECTOR_SCALE = 10
        l *= VECTOR_SCALE

        print 'hpr:', l

        return l


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

        loadPrcFileData('', 'want-pstats 1')
        loadPrcFileData("", "prefer-parasite-buffer #f")

        print 'use vsync:', self._config_src.get_bool('use-vsync', 'core.gfx', True)
        if self._config_src.get_bool('use-vsync', 'core.gfx', True) is False:
            loadPrcFileData('', 'sync-video #f')

        if self.frame_rate != 0:

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
        #self.panda_window.render.setShaderAuto()
        self.panda_window.disableMouse()
        getModelPath().appendPath(self.search_path)

        if self._config_src.get_str('shading', 'core.gfx', 'normal') == 'toon-full':

           self._enable_toon_outline()
           self._enable_toon_shading()

        elif self._config_src.get_str('shading', 'core.gfx', 'normal') == 'toon':
            self._enable_toon_shading()

        else:
            pass
#            self.panda_window.render.setAttrib(LightRampAttrib.makeHdr0())

        use_shadows = self._config_src.get_bool('use-shadows', 'core.gfx')
        if use_shadows is True:
            self._enable_shadows()

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

    def _enable_toon_shading(self):
        return self.panda_window.render.setAttrib(LightRampAttrib.makeDoubleThreshold(0.4, 0.3, 0.5, 0.4))

    def _enable_toon_outline(self):

        normals_buffer = self.panda_window.win.makeTextureBuffer('Normals Buffer', 0, 0)
        normals_buffer.setClearColor(Vec4(0.5, 0.5, 0.5, 1))
        normals_camera = self.panda_window.makeCamera(normals_buffer,
            lens = self.panda_window.cam.node().getLens())
        normals_camera.node().setScene(self.panda_window.render)
        normals_node = NodePath(PandaNode('temp. normals node'))
        normals_node.setShader(self.panda_window.loader.loadShader('normal-shader.cg'))
        normals_camera.node().setInitialState(normals_node.getState())
        edge_detect_scene = normals_buffer.getTextureCard()
        edge_detect_scene.setTransparency(1)
        edge_detect_scene.setColor(1, 1, 1, 0)
        edge_detect_scene.reparentTo(self.panda_window.render2d)
        ink_shader = self.panda_window.loader.loadShader('ink-shader.cg')
        edge_detect_scene.setShader(ink_shader)
        SEPARATION = 0.001
        edge_detect_scene.setShaderInput('separation', Vec4(SEPARATION, 0, SEPARATION, 0))
        CUTOFF = 0.3
        edge_detect_scene.setShaderInput('cutoff', Vec4(CUTOFF, CUTOFF, CUTOFF, CUTOFF))

    def _enable_shadows(self):

         sci = NodePath(PandaNode("Shadow Camera Initializer"))
         shadow_renderer_shader = self.panda_window.loader.loadShader('shadow-renderer.sha')
         sci.setShader(shadow_renderer_shader)
         base.cam.node().setInitialState(sci.getState())
         base.bufferViewer.toggleEnable()


class Camera(object):

    def __init__(self, window):

        self.on_loaded = obengine.event.Event()

        self.window = window
        self.camera = self.window.panda_window.camera
        self.panda_node = self.camera
        self._parent = None

    def load(self):
        self.on_loaded()

    def look_at(self, model):
        self.camera.lookAt(model.panda_node)

    def look_at_point(self, point):
        self.camera.lookAt(PandaConverter.convert_vector_to_point3(point))

    def move(self, vector):
        self.camera.setPos(self.camera, vector.x, vector.y, vector.z)

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

            quat = PandaConverter.convert_angle(new_angle)
            self.camera.setQuat(quat)

        return locals()

    @obengine.datatypes.nested_property
    def parent():

        def fget(self):
            return self._parent

        def fset(self, new_parent):

            self._parent = new_parent
            self.camera.reparentTo(self.parent.panda_node)

        return locals()
