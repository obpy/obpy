"""
Copyright (C) 2010 The OpenBlox Project

This file is part of The OpenBlox Game Engine.

    The OpenBlox Game Engine is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    The OpenBlox Game Engine is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with The OpenBlox Game Engine.  If not, see <http://www.gnu.org/licenses/>.

"""

__author__="openblocks"
__date__ ="$Aug 5, 2010 1:37:16 PM$"

import obengine.cfg
import obengine.gfx.window3d
import obengine.utils

from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.stdpy.thread import start_new_thread
from direct.task import Task
from direct.interval.IntervalGlobal import *

from pandac.PandaModules import Vec4, Vec3, CompassEffect, ClockObject
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import loadPrcFileData

rootwin = None

def setup_lights():

    global rootwin

    # Create some lights

    ambient_light = AmbientLight("Ambientlight")
    ambient_light.setColor(Vec4(0.2, 0.2, 0.2, 1))

    # Add a sun

    sunlight = DirectionalLight("Sunlight")
    sunlight.setColor(Vec4(0.8, 0.8, 0.8, 1))

    sunnode = rootwin.render.attachNewNode(sunlight)
    sunnode.setHpr(0, 0, 0)

    # Make 1 "day" last 15 minutes :)

    suninterval = sunnode.hprInterval(60.0 * 15.0, Vec3(0, 360, 0))
    sunseq = Sequence(suninterval)

    # Turn on the lights

    rootwin.render.setLight(rootwin.render.attachNewNode(ambient_light))
    rootwin.render.setLight(sunnode)

    rootwin.render.setShaderAuto()

    sunseq.loop()

    rootwin.setBackgroundColor(1, 1, 1, 1)

def get_rootwin():
    """
    Returns the root Panda3D window.
    Might be removed in the future.
    """

    return rootwin

def run(main_method):
    """
    If this method returns, something bad happened...
    main_method is a method that takes 1 argument, which is the root Panda3D window.

    After the graphics are initalized, a new thread is started, with main_method.
    """

    obengine.utils.info('Initalizing graphics subsystem...')
    
    global rootwin

    loadPrcFileData('', 'show-frame-rate-meter 1')
    loadPrcFileData('', 'want-pstats 1')

    global_clock = ClockObject.getGlobalClock()
    global_clock.setMode(ClockObject.MLimited)
    global_clock.setFrameRate(obengine.cfg.get_config_var('fps'))
    
    rootwin = window3d.Window3D()
    
    setup_lights()

    obengine.utils.info('Graphics subsystem initialized! Loading...')

    main_method(rootwin)

    obengine.utils.info('Loading completed! Entering Panda3D update loop...')

    rootwin.run()