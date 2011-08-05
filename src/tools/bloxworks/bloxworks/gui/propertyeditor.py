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
__date__ = "Aug 1, 2011 8:03:51 PM"


import functools

import obengine.math
import obengine.async
import obengine.vfs
import obengine.gui
import obengine.elementfactory

import bloxworks.project
import bloxworks.commands.element
import bloxworks.commands.brick


class PropertyEditor(object):

    def __init__(self, window):

        widget_factory = obengine.gui.WidgetFactory()
        self._form = widget_factory.make(
                                        'container',
                                         layout_manager = obengine.gui.VerticalLayoutManager,
                                         position = obengine.math.Vector2D(60, -30))

        ENTRY_LENGTH = 35

#        self._collide_checkbox = widget_factory.make('checkbox', 'Collide')
#        self._form.add(self._collide_checkbox)

        self._window = window

        self._hide_button = widget_factory.make('button', 'Hide')
        self._hide_button.on_click += self._form.hide
        self._form.add(self._hide_button)

        self._clone_button = widget_factory.make('button', 'Clone brick')
        self._clone_button.on_click += self._clone_brick
        self._form.add(self._clone_button)

        self._remove_button = widget_factory.make('button', 'Remove brick')
        self._remove_button.on_click += self._remove_brick
        self._form.add(self._remove_button)

        self._anchored_checkbox = widget_factory.make('checkbox', 'Anchored')
        self._form.add(self._anchored_checkbox)

        self._rotation_entry = widget_factory.make('entry', length = ENTRY_LENGTH)
        self._form.add(self._rotation_entry)

        self._rotation_label = widget_factory.make('label', 'Rotation')
        self._form.add(self._rotation_label)

        self._size_entry = widget_factory.make('entry', length = ENTRY_LENGTH)
        self._form.add(self._size_entry)

        self._size_label = widget_factory.make('label', 'Size')
        self._form.add(self._size_label)

        self._color_entry = widget_factory.make('entry', length = ENTRY_LENGTH)
        self._form.add(self._color_entry)

        self._color_label = widget_factory.make('label', 'Color')
        self._form.add(self._color_label)

        self._position_entry = widget_factory.make('entry', length = ENTRY_LENGTH)
        self._form.add(self._position_entry)

        self._position_label = widget_factory.make('label', 'Position')
        self._form.add(self._position_label)

        self._name_entry = widget_factory.make('entry', length = ENTRY_LENGTH)
        self._form.add(self._name_entry)

        self._name_label = widget_factory.make('label', 'Name')
        self._form.add(self._name_label)

        self._brick = None
        self.reset()

        obengine.vfs.open('/bloxworks-registry/property-editor', 'w').write(self)

    def populate(self, brick):

        self.reset()

        self._form.showing = True

        self._brick = brick

        self._name_entry.text = self._brick.name
        self._anchored_checkbox.state = int(self._brick.anchored)
        self._rotation_entry.text = self._euler_angle_to_str(self._brick.rotation)
        self._color_entry.text = self._color_to_str(self._brick.color)
        self._size_entry.text = self._vector_to_str(self._brick.size)
        self._position_entry.text = self._vector_to_str(self._brick.position)

        self._name_entry.on_submitted += self._set_brick_name
        self._anchored_checkbox.on_state_changed += self._set_brick_anchored
        self._rotation_entry.on_submitted += self._set_brick_rotation
        self._color_entry.on_submitted += self._set_brick_color
        self._size_entry.on_submitted += self._set_brick_size
        self._position_entry.on_submitted += self._set_brick_position

    def reset(self):

        if self._brick is not None:

            self._name_entry.on_submitted -= self._set_brick_name
            self._anchored_checkbox.on_state_changed -= self._set_brick_anchored
            self._rotation_entry.on_submitted -= self._set_brick_rotation
            self._color_entry.on_submitted -= self._set_brick_color
            self._size_entry.on_submitted -= self._set_brick_size

        self._name_entry.text = ''
        self._position_entry.text = ''
        self._rotation_entry.text = ''
        self._color_entry.text = ''
        self._size_entry.text = ''

        self._brick = None

        self._form.showing = False

    def _set_brick_name(self):
        if self._brick is not None:
            self._brick.name = self._name_entry.text

    def _set_brick_anchored(self, checkbox_state):
        if self._brick is not None:
            self._brick.anchored = bool(checkbox_state)

    def _set_brick_position(self):

        position_str = self._position_entry.text

        if self._brick is None:
            return

        position_components = position_str.strip().split(',')

        if len(position_components) != 3:
            return

        try:
            position_components = map(float, position_components)
        except ValueError:
            return

        position = obengine.math.Vector(*position_components)
        self._brick.position = position

    def _set_brick_color(self):

        color_str = self._color_entry.text

        if self._brick is None:
            return

        color_components = color_str.strip().split(',')

        if 4 <= len(color_components) >= 3 is False:
            return

        try:
            color_components = map(float, color_components)
        except ValueError:
            return

        color = obengine.math.Color(*color_components)
        self._brick.color = color

    def _set_brick_size(self):

        size_str = self._size_entry.text

        if self._brick is None:
            return

        size_components = size_str.strip().split(',')

        if len(size_components) != 3:
            return

        try:
            size_components = map(float, size_components)
        except ValueError:
            return

        size = obengine.math.Vector(*size_components)
        self._brick.size = size

    def _set_brick_rotation(self):

        rotation_str = self._rotation_entry.text

        if self._brick is None:
            return

        rotation_components = rotation_str.strip().split(',')

        if len(rotation_components) != 3:
            return

        try:
            rotation_components = map(float, rotation_components)
        except ValueError:
            return

        rotation = obengine.math.EulerAngle(*rotation_components)
        self._brick.rotation = rotation

    def _remove_brick(self):

        project = obengine.vfs.open('/bloxworks-registry/project').read()
        nid = self._brick.nid
        bloxworks.commands.element.RemoveElementCommand(project, nid = nid).execute()

        self.reset()

    def _clone_brick(self):

        size = self._brick.size
        anchored = self._brick.anchored
        color = self._brick.color
        rotation = self._brick.rotation

        factory = obengine.elementfactory.ElementFactory()
        factory.set_window(self._window)
        sandbox = obengine.vfs.open('/bloxworks-registry/sandbox').read()
        factory.set_sandbox(sandbox)

        project = obengine.vfs.open('/bloxworks-registry/project').read()

        command = bloxworks.commands.brick.AddBrickCommand(project,
                                                           factory,
                                                           'Cloned Brick',
                                                           size = size,
                                                           anchored = anchored,
                                                           color = color,
                                                           rotation = rotation)
        self._window.scheduler.add(obengine.async.AsyncCall(command.execute, 5))

    def _vector_to_str(self, vector):
        return str('%s, %s, %s' % (vector.x, vector.y, vector.z))

    def _euler_angle_to_str(self, angle):
        return str('%s, %s, %s' % (angle.h, angle.p, angle.r))

    def _color_to_str(self, color):
        return str('%s, %s, %s, %s' % (color.r, color.g, color.b, color.a))


class PropertyEditorProjectVisitor(bloxworks.project.ProjectVisitor):

    def __init__(self, property_editor):
        self._property_editor = property_editor

    def visit(self, project):

        for element in project.world.element.nodes.itervalues():

            # TODO: Replace the below condition with something more general!
            if element.__class__.__name__ == 'BrickPresenter':
                element.on_click += functools.partial(self._property_editor.populate, element)
