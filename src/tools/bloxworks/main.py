#!/usr/bin/env python
#
# This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


__author__ = "openblocks"
__date__ = "$Jul 26, 2011 1:14:56 PM$"


import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.pardir, os.pardir)))

import obengine.vfs
import obengine.cfg
import obengine.async
import obengine.plugin

import bloxworks.project
import bloxworks.gui.propertyeditor
import bloxworks.gui.toolbars
import bloxworks.gui.project
import bloxworks.gui.brick
import bloxworks.gui.camera


def save_project():

    try:
        project = obengine.vfs.open('/bloxworks-registry/project').read()
    except obengine.vfs.ReadError:
        return

    outfile = os.path.join(
                           obengine.vfs.getsyspath('/bloxworks-games/' + project.world.name),
                           bloxworks.project.WORLD_XML_FILE)

    saver = bloxworks.project.ProjectSaverVisitor(outfile)
    saver.accept(project)


def package_project():

    try:
        project = obengine.vfs.open('/bloxworks-registry/project').read()
    except obengine.vfs.ReadError:
        return

    outfile = os.path.join(
                           obengine.vfs.getsyspath('/bloxworks-games/' + project.world.name),
                           project.world.name + '.zip')

    packager = bloxworks.project.ProjectPackagerVisitor(outfile)
    packager.accept(project)


def create_gui(window):

    property_editor = bloxworks.gui.propertyeditor.PropertyEditor(window)
    side_toolbar = bloxworks.gui.toolbars.SideToolbar()
    bottom_toolbar = bloxworks.gui.toolbars.BottomToolbar()
    top_toolbar = bloxworks.gui.toolbars.TopToolbar()

    lpd = bloxworks.gui.project.LoadProjectDialog(window)
    top_toolbar.on_open_button_clicked += lpd.show

    npd = bloxworks.gui.project.NewProjectDialog(window)
    top_toolbar.on_new_button_clicked += npd.show

    abd = bloxworks.gui.brick.AddBrickDialog(window)
    side_toolbar.on_brick_button_clicked += abd.execute

    top_toolbar.on_save_button_clicked += save_project
    top_toolbar.on_pack_button_clicked += package_project

    move_tool = bloxworks.gui.brick.MoveBrickTool(window)
    bottom_toolbar.on_move_button_clicked += move_tool.toggle_activation

    resize_tool = bloxworks.gui.brick.ResizeBrickTool(window)
    bottom_toolbar.on_scale_button_clicked += resize_tool.toggle_activation

    camera_controller = bloxworks.gui.camera.CameraController(window)


def create_window(scheduler):

    obengine.plugin.require('core.graphics')

    import obplugin.core.graphics

    window = obplugin.core.graphics.Window('BloxWorks', scheduler)
    window.on_loaded += window.start_rendering
    window.load()

    return window


def main():

    obengine.cfg.Config().load(os.path.abspath(os.path.join(os.pardir, os.pardir, 'obconf.cfg')))
    obengine.init()

    sched = obengine.async.Scheduler()
    window = create_window(sched)
    window.on_loaded += lambda: create_gui(window)

    sched.loop()


if __name__ == '__main__':
    main()
