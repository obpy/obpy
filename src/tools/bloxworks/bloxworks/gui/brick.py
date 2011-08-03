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


import obengine.async
import obengine.vfs
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

        self._name_entry = widget_factory.make('entry', length = 30)
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
