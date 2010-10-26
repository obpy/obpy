__author__="alexander"
__date__ ="$Aug 5, 2010 1:37:16 PM$"

import obengine.cfg
import window3d

import os

from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.stdpy.thread import start_new_thread
from direct.task import Task

from pandac.PandaModules import TransparencyAttrib, Vec4, CompassEffect, OdeWorld, OdeSimpleSpace, OdeJointGroup
from panda3d.core import AmbientLight, DirectionalLight

load_text = None
logo = None
loaded = False

rootwin = None

phys_world = None
phys_space = None
phys_cg = None
phys_objs = []

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

    loaded = True
    logo.removeNode()

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
    
    logo = OnscreenImage(obengine.cfg.cfgdir + os.sep + 'data' + os.sep +'OpenBlox Logo.png', pos = (0, 0, 0))
    logo.setTransparency(TransparencyAttrib.MAlpha)

def setup_physics():

    global phys_world
    global phys_space
    global phys_cg

    # Create the physical representation of our world

    phys_world = OdeWorld()
    phys_world.setGravity(0, 0, -9.81)

    phys_space = OdeSimpleSpace()
    phys_space.setAutoCollideWorld(phys_world)

    phys_cg = OdeJointGroup()

    phys_space.setAutoCollideJointGroup(phys_cg)

    # We use autoCollide for automatic collisions, so we initalize the surface table here
    # See http://www.panda3d.org/manual/index.php/Collision_Detection_with_ODE for more info

    phys_world.initSurfaceTable(1)
    phys_world.setSurfaceEntry(0, 0, 150, 0.0, 9.1, 0.9, 0.00001, 0.0, 0.002)

    rootwin.taskMgr.add(update_physics, 'update_physics')

def get_rootwin():
    """
    Returns the root Panda3D window.
    Might be removed in the future.
    """
    
    return rootwin

def get_phys_world():
    """
    Returns the physical representation of our sandbox.
    Might be removed in the future.
    """

    return phys_world

def get_phys_space():

    return phys_space

def get_phys_cg():

    return phys_cg

def update_physics(task):

    global phys_objs

    get_phys_space().autoCollide()

    phys_world.quickStep(1.0 / float(obengine.cfg.fps))

    for obj in phys_objs:

        obj.update()

    get_phys_cg().empty()

    return Task.cont

def register_phys_obj(obj):

    global phys_objs

    phys_objs.append(obj)

def init(main_method):
    """
    If this method returns, something bad happened...
    main_method is a method that takes 1 argument, which is the root Panda3D window.

    After the graphics are initalized, a new thread is started, with main_method.
    """

    print '[STARTUP] Initalizing graphics subsystem...'
    
    global rootwin
    rootwin = window3d.Window3D()
    
    setup_load()
    setup_lights()
    setup_physics()

    # Repeat the progress updating method once every 0.7 seconds

    rootwin.taskMgr.doMethodLater(0.7, progress_update, 'load_update')

    
    start_new_thread(main_method,(rootwin, ))
    stop_load()

    rootwin.run()