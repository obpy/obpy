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
__date__ = "Aug 2, 2011 4:54:54 PM"


import os

import obengine.async
import obengine.vfs
import obengine.gui

import bloxworks.project
import bloxworks.gui.propertyeditor
import bloxworks.gui.brick


class LoadProjectDialog(object):

    def __init__(self, window):

        self._window = window

        widget_factory = obengine.gui.WidgetFactory()
        self._dialog = widget_factory.make('container', layout_manager = obengine.gui.VerticalLayoutManager)
        self._cancel_button = widget_factory.make('button', 'Cancel')
        self._cancel_button.on_click += self.hide
        self._dialog.add(self._cancel_button)

        self._name_entry = widget_factory.make('entry', 'Project name', length = 40)
        self._dialog.add(self._name_entry)
        self._name_entry.on_submitted += self._load_project
        self.hide()

    def show(self):
        self._dialog.show()

    def hide(self):
        self._dialog.hide()

    def _load_project(self):

        game_name = self._name_entry.text
        game_path = obengine.vfs.getsyspath('/bloxworks-games/' + game_name)

        if os.path.exists(game_path) is False:

            self._name_entry.text = 'Project not found'
            return

        if game_name == '':
            return

        self._window.scheduler.add(obengine.async.AsyncCall(self._actual_load, 5, game_path))
        self.hide()

    def _actual_load(self, game_path):

        bloxworks.project.load_project(game_path, self._window)
        project = obengine.vfs.open('/bloxworks-registry/project').read()

        property_editor = obengine.vfs.open('/bloxworks-registry/property-editor').read()
        property_editor_visitor = \
        bloxworks.gui.propertyeditor.PropertyEditorProjectVisitor(property_editor)
        project.accept(property_editor_visitor)

        move_tool_visitor = bloxworks.gui.brick.MoveToolProjectVisitor()
        project.accept(move_tool_visitor)

        resize_tool_visitor = bloxworks.gui.brick.ResizeToolProjectVisitor()
        project.accept(resize_tool_visitor)


class NewProjectDialog(object):

    def __init__(self, window):

        self._window = window
        widget_factory = obengine.gui.WidgetFactory()
        self._dialog = widget_factory.make('container', layout_manager = obengine.gui.VerticalLayoutManager)

        self._cancel_button = widget_factory.make('button', 'Cancel')
        self._cancel_button.on_click += self.hide
        self._dialog.add(self._cancel_button)

        self._author_entry = widget_factory.make('entry', 'Author', length = 40)
        self._dialog.add(self._author_entry)

        self._name_entry = widget_factory.make('entry', 'Name', length = 40)
        self._dialog.add(self._name_entry)
        self._name_entry.on_submitted += self._create_project

        self.hide()

    def _create_project(self):

        game_name = self._name_entry.text
        game_path = obengine.vfs.getsyspath('/bloxworks-games/' + game_name)

        if os.path.exists(game_path) is True:

            self._name_entry.text = 'Project already exists'
            return

        game_author = self._author_entry.text

        self._window.scheduler.add(obengine.async.AsyncCall(self._actual_creation, 5, game_name, game_author))
        self.hide()

    def show(self):
        self._dialog.show()

    def hide(self):
        self._dialog.hide()

    def _actual_creation(self, game_name, game_author):
        bloxworks.project.create_new_project(self._window, game_name, game_author)
