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

    widget_factory = obengine.gui.WidgetFactory()

    top_toolbar = widget_factory.make('shutter',
    position = obengine.math.Vector2D(0, 90))

    top_toolbar.add(widget_factory.make('button', icon = 'data/icons/new.png'))
    top_toolbar.add(widget_factory.make('button', icon = 'data/icons/open.png'))
    top_toolbar.add(widget_factory.make('button', icon = 'data/icons/save.png'))
    top_toolbar.add(widget_factory.make('button', icon = 'data/icons/pack.png'))

    bottom_toolbar = widget_factory.make('shutter',
    position = obengine.math.Vector2D(0, -90))

    bottom_toolbar.add(widget_factory.make('button', icon = 'data/icons/move.png'))
    bottom_toolbar.add(widget_factory.make('button', icon = 'data/icons/scale.png'))
    bottom_toolbar.add(widget_factory.make('button', icon = 'data/icons/repaint.png'))

    side_toolbar = widget_factory.make('shutter',
    position = obengine.math.Vector2D(-90, 0),
    layout_manager = obengine.gui.VerticalLayoutManager)

    side_toolbar.add(widget_factory.make('button', icon = 'data/icons/Sky.png'))
    side_toolbar.add(widget_factory.make('button', icon = 'data/icons/light.png'))
    side_toolbar.add(widget_factory.make('button', icon = 'data/icons/Lua.png'))
    side_toolbar.add(widget_factory.make('button', icon = 'data/icons/add-brick.png'))
    

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