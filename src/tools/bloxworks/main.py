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

import obengine.math
import obengine.cfg
import obengine.async
import obengine.plugin
import obengine.world
import obengine.gui
import obengine.elementfactory

import bloxworks.project
import bloxworks.commands.brick
import bloxworks.gui.propertyeditor
import bloxworks.gui.toolbars



def make_brick(window):

    world = obengine.world.World(1, 'World')
    project = bloxworks.project.Project(world, 'openblocks', '0.7.0')

    element_factory = obengine.elementfactory.ElementFactory()
    element_factory.set_window(window)

    obengine.plugin.require('core.physics')
    import obplugin.core.physics
    physics_sandbox = obplugin.core.physics.World()
    physics_sandbox.load()
    element_factory.set_sandbox(physics_sandbox)

    add_brick_command = bloxworks.commands.brick.AddBrickCommand(project, element_factory, 'Brick')
    add_brick_command.execute()

def create_gui(window):

    property_editor = bloxworks.gui.propertyeditor.PropertyEditor()
    side_toolbar = bloxworks.gui.toolbars.SideToolbar()
    bottom_toolbar = bloxworks.gui.toolbars.BottomToolbar()
    top_toolbar = bloxworks.gui.toolbars.TopToolbar()

    make_brick(window)



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
