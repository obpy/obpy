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
__date__  = "$Jul 26, 2011 1:14:56 PM$"


import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.pardir, os.pardir)))

import obengine.math
import obengine.cfg
import obengine.async
import obengine.plugin
import obengine.gui


def create_gui():

    property_editor_form = widget_factory.make(
    'container',
    layout_manager = obengine.gui.VerticalLayoutManager,
    position = obengine.math.Vector2D(75, -60))

    property_editor_form.add(widget_factory.make('checkbox', 'Collide'))

    property_editor_form.add(widget_factory.make('checkbox', 'Anchored'))
    
    property_editor_form.add(widget_factory.make('entry'))

    property_editor_form.add(widget_factory.make(
    'label',
    'Rotation'))

    property_editor_form.add(widget_factory.make('entry'))

    property_editor_form.add(widget_factory.make(
    'label',
    'Size'))

    property_editor_form.add(widget_factory.make('entry'))

    property_editor_form.add(widget_factory.make(
    'label',
    'Color'))

    property_editor_form.add(widget_factory.make('entry'))

    property_editor_form.add(widget_factory.make(
    'label',
    'Name'
    ))

    
    

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
    window.on_loaded += create_gui

    sched.loop()


if __name__ == '__main__':
    main()