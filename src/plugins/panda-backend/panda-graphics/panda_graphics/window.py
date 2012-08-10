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
__date__ = "Jul 19, 2012 6:02:27 PM"


from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

import obengine.datatypes
import obengine.event
import obengine.cfg
import obplugin.panda_hardware

from model import ModelCollector, CLICKABLE_BITMASK


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
        self.scheduler.add(obengine.async.Task(self._run_panda_task, priority = Window.RENDER_PRIORITY))

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

        loadPrcFileData('', 'want-pstats #t')
        loadPrcFileData("", "prefer-parasite-buffer #f")

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
        #self.panda_window.disableMouse()
        self.panda_window.bufferViewer.toggleEnable()
        self.panda_window.enableParticles()
        getModelPath().appendPath(self.search_path)

        scene_fog = Fog('scene-wide fog')
        scene_fog.setColor(0.5, 0.8, 0.8)
        scene_fog.setExpDensity(0.0009)
        self.panda_window.render.setFog(scene_fog)

        picker_node = CollisionNode('mouse_ray')
        picker_nodepath = self.panda_window.camera.attachNewNode(picker_node)
        picker_node.setFromCollideMask(CLICKABLE_BITMASK)
        self.picker_ray = CollisionRay()
        picker_node.addSolid(self.picker_ray)
        self.mouse_traverser = CollisionTraverser()
        self.collision_queue = CollisionHandlerQueue()
        self.mouse_traverser.addCollider(picker_nodepath, self.collision_queue)
        mouse_button = obplugin.panda_hardware.MouseEvent.LEFT_MOUSE
        mouse_event_type = obplugin.panda_hardware.MouseEvent.TYPE_DOWN
        self._click_event = obplugin.panda_hardware.MouseEvent(
                                       self,
                                       mouse_button,
                                       mouse_event_type)
        self._click_event += self._pick_mouse

        ModelCollector()

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

    def _run_panda_task(self, task):

        try:
            self.panda_window.taskMgr.step()

        except SystemExit:
            return task.STOP

        return task.AGAIN
