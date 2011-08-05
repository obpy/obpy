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
__date__ = "Aug 2, 2011 7:11:56 PM"


import functools
import copy

import obengine.async
import obengine.vfs
import obengine.plugin
import obengine.gui
import obengine.elementfactory

import bloxworks.commands.brick


class AddBrickDialog(object):

    def __init__(self, window):

        self._window = window
        self._factory = obengine.elementfactory.ElementFactory()
        self._factory.set_window(self._window)

        widget_factory = obengine.gui.WidgetFactory()
        self._dialog = widget_factory.make('container', layout_manager = obengine.gui.VerticalLayoutManager)

        self._cancel_button = widget_factory.make('button', 'Cancel')
        self._cancel_button.on_click += self.hide
        self._dialog.add(self._cancel_button)

        self._name_entry = widget_factory.make('entry', 'Name', length = 30)
        self._name_entry.on_submitted += self._create_brick
        self._dialog.add(self._name_entry)

        self.hide()

    def show(self):
        self._dialog.show()

    def hide(self):
        self._dialog.hide()

    def _create_brick(self):

        self._factory.set_sandbox(obengine.vfs.open('/bloxworks-registry/sandbox').read())
        brick_name = self._name_entry.text
        self._window.scheduler.add(obengine.async.AsyncCall(self._actual_create, 5, brick_name))

    def _actual_create(self, brick_name):

        project = obengine.vfs.open('/bloxworks-registry/project').read()
        bloxworks.commands.brick.AddBrickCommand(project, self._factory, brick_name).execute()

        self.hide()


class MoveBrickTool(object):

    def __init__(self, window):

        self._moving = False
        self._activated = False
        self._brick = None

        obengine.plugin.require('core.hardware')
        import obplugin.core.hardware

        coord_space = obplugin.core.hardware.MouseMotionEvent.COORD_3D
        self._mouse_motion_event = obplugin.core.hardware.MouseMotionEvent(
                                                                           window,
                                                                           coord_space)

        mouse_wheel = obplugin.core.hardware.MouseEvent.MOUSE_WHEEL
        wheel_up = obplugin.core.hardware.MouseEvent.TYPE_WHEEL_UP
        self._move_z_up_event = obplugin.core.hardware.MouseEvent(
                                                                  window,
                                                                  mouse_wheel,
                                                                  wheel_up)

        wheel_down = obplugin.core.hardware.MouseEvent.TYPE_WHEEL_DOWN
        self._move_z_down_event = obplugin.core.hardware.MouseEvent(
                                                                    window,
                                                                    mouse_wheel,
                                                                    wheel_down)

        mouse_button = obplugin.core.hardware.MouseEvent.LEFT_MOUSE
        mouse_event_type = obplugin.core.hardware.MouseEvent.TYPE_DOWN
        self._stop_event = obplugin.core.hardware.MouseEvent(
                                                             window,
                                                             mouse_button,
                                                             mouse_event_type)

        obengine.vfs.open('/bloxworks-registry/move-tool', 'w').write(self)

    def set_state(self, state):
        self._activated = state

    def toggle_activation(self):
        self._activated = not self._activated

    def deactivate(self):
        self._activated = False

    def activate(self):
        self._activated = True

    def move(self, brick):

        if self._activated is False:
            return

        if self._moving is True:

            self.reset()
            return

        self._moving = True

        self._brick = brick
        self._mouse_motion_event += self._move_brick
        self._mouse_motion_event.z_value = self._brick.position.z

        self._move_z_up_event += self._move_brick_up
        self._move_z_down_event += self._move_brick_down

    def reset(self):

        self._brick = None
        self._moving = False

        if self._move_brick in self._mouse_motion_event.handlers:

            self._mouse_motion_event -= self._move_brick
            self._move_z_up_event -= self._move_brick_up
            self._move_z_down_event -= self._move_brick_down

        if self.reset in self._stop_event.handlers:
            self._stop_event -= self.reset

    def _move_brick(self, mouse_pos):

        copied_vector = copy.copy(mouse_pos)
        copied_vector.x = round(copied_vector.x)
        copied_vector.y = round(copied_vector.y)
        copied_vector.z = self._brick.position.z

        self._brick.position = copied_vector

        if self.reset not in self._stop_event.handlers:
            self._stop_event += self.reset

    def _move_brick_up(self):

        new_pos = self._brick.position
        new_pos.z += 1
        self._brick.position = new_pos

    def _move_brick_down(self):

        new_pos = self._brick.position
        new_pos.z -= 1
        self._brick.position = new_pos


class MoveToolProjectVisitor(object):

    def visit(self, project):

        move_tool = obengine.vfs.open('/bloxworks-registry/move-tool').read()
        world = obengine.vfs.open('/bloxworks-registry/project').read().world

        for element in world.element.nodes.itervalues():
            if element.__class__.__name__ == 'BrickPresenter':
                element.on_click += functools.partial(move_tool.move, element)


class ResizeBrickTool(object):

    def __init__(self, window):

        self._resizing = False
        self._activated = False
        self._brick = None

        obengine.plugin.require('core.hardware')
        import obplugin.core.hardware

        mouse_wheel = obplugin.core.hardware.MouseEvent.MOUSE_WHEEL
        wheel_up = obplugin.core.hardware.MouseEvent.TYPE_WHEEL_UP
        self._move_z_up_event = obplugin.core.hardware.MouseEvent(
                                                                  window,
                                                                  mouse_wheel,
                                                                  wheel_up)

        wheel_down = obplugin.core.hardware.MouseEvent.TYPE_WHEEL_DOWN
        self._move_z_down_event = obplugin.core.hardware.MouseEvent(
                                                                    window,
                                                                    mouse_wheel,
                                                                    wheel_down)

        coord_space = obplugin.core.hardware.MouseMotionEvent.COORD_3D
        self._mouse_motion_event = obplugin.core.hardware.MouseMotionEvent(
                                                                           window,
                                                                           coord_space)

        mouse_button = obplugin.core.hardware.MouseEvent.LEFT_MOUSE
        mouse_event_type = obplugin.core.hardware.MouseEvent.TYPE_DOWN
        self._stop_event = obplugin.core.hardware.MouseEvent(
                                                             window,
                                                             mouse_button,
                                                             mouse_event_type)

        obengine.vfs.open('/bloxworks-registry/resize-tool', 'w').write(self)

    def set_state(self, state):
        self._activated = state

    def toggle_activation(self):
        self._activated = not self._activated

    def deactivate(self):
        self._activated = False

    def activate(self):
        self._activated = True

    def resize(self, brick):

        if self._activated is False:
            return

        if self._resizing is True:

            self.reset()
            return

        self._resizing = True

        self._brick = brick

        self._mouse_motion_event.z_value = self._brick.position.z
        self._mouse_motion_event += self._resize_brick

        self._move_z_up_event += self._resize_brick_z_up
        self._move_z_down_event += self._resize_brick_z_down

    def reset(self):

        self._brick = None
        self._resizing = False

        if self._resize_brick in self._mouse_motion_event.handlers:

            self._mouse_motion_event -= self._resize_brick
            self._move_z_up_event -= self._resize_brick_z_up
            self._move_z_down_event -= self._resize_brick_z_down

    def _resize_brick(self, mouse_pos):

        mouse_x_delta = mouse_pos.x - self._mouse_motion_event._old_mouse_x
        mouse_y_delta = mouse_pos.y - self._mouse_motion_event._old_mouse_y

        copied_size = copy.copy(self._brick.size)
        copied_size.x += round(mouse_x_delta)
        copied_size.x = abs(copied_size.x)
        copied_size.y += round(mouse_y_delta)
        copied_size.y = abs(copied_size.y)

        copied_size.x = max(1, copied_size.x)
        copied_size.y = max(1, copied_size.y)

        self._brick.size = copied_size

    def _resize_brick_z_up(self):

        copied_size = copy.copy(self._brick.size)
        copied_size.z += 1
        copied_size.z = max(1, copied_size.z)
        self._brick.size = copied_size

    def _resize_brick_z_down(self):

        copied_size = copy.copy(self._brick.size)
        copied_size.z -= 1
        copied_size.z = max(1, copied_size.z)
        self._brick.size = copied_size


class ResizeToolProjectVisitor(object):

    def visit(self, project):

        resize_tool = obengine.vfs.open('/bloxworks-registry/resize-tool').read()
        world = obengine.vfs.open('/bloxworks-registry/project').read().world

        for element in world.element.nodes.itervalues():
            if element.__class__.__name__ == 'BrickPresenter':
                element.on_click += functools.partial(resize_tool.resize, element)
