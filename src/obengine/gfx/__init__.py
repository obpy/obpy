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

import os

from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.stdpy.thread import start_new_thread
from direct.task import Task

from pandac.PandaModules import TransparencyAttrib, Vec4, CompassEffect, ClockObject
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import loadPrcFileData

load_text = None
logo = None
loaded = False

rootwin = None

def progress_update(task):

    # A very clever function, if I do say so myself...
    # Basically, what this does is change the loading text;
    # if we have one period(.), add another one, if we have 3, just show one period.

    text_dict = { 'Loading.' : 'Loading..', 'Loading..' : 'Loading...', 'Loading...' : 'Loading.' }

    global load_text
    global loaded

    load_text.setText(text_dict[load_text.getText()])

    # Are we still loading?

    if not loaded:

         return Task.again

    else:

        # If a Panda3D task does not return Task.again, it is terminated
        load_text.setText('Loaded!')

def stop_load():

    global loaded
    global logo
    global load_text

    loaded = True
    logo.removeNode()
    load_text.removeNode()


def setup_lights():

    global rootwin

    # Create some lights

    ambient_light = AmbientLight("ambientLight")
    ambient_light.setColor(Vec4(.3, .3, .3, 1))

    directional_light = DirectionalLight("directionalLight")
    directional_light.setColor(Vec4(1, 1, 1, 1))
    directional_light.setSpecularColor(Vec4(1, 1, 1, 1))

    dlnode = rootwin.render.attachNewNode(directional_light)
    dlnode.lookAt(0,0,0)

    rootwin.render.setLight(rootwin.render.attachNewNode(ambient_light))
    rootwin.render.setLight(dlnode)

    rootwin.render.setShaderAuto()

def setup_load():

    global logo
    global load_text

    load_text = OnscreenText(text = 'Loading..', pos = (0.7, -0.7))
    
    logo = OnscreenImage(obengine.cfg.get_config_var('cfgdir') + os.sep + 'data' + os.sep +'oblogo.png', pos = (0, 0, 0))
    logo.setTransparency(TransparencyAttrib.MAlpha)

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
    
    setup_load()
    setup_lights()

    # Repeat the progress updating method once every 0.7 seconds

    rootwin.taskMgr.doMethodLater(0.7, progress_update, 'load_update')

    obengine.utils.info('Graphics subsystem initialized! Loading...')

    main_method(rootwin)

    stop_load()

    obengine.utils.info('Loading completed! Entering Panda3D update loop...')

    rootwin.run()