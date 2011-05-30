# <obengine.environ>
# ===================
#
# High-level interface to various low-level modules, for easier usage of OpenBlox.
#
# Copyright (C) 2011 The OpenBlox Project
# License: GNU GPL v3
#
# See <TODO: No Sphinx docs yet - add some!> for the primary source of documentation
# for this module.

__author__ = "openblocks"
__date__  = "$May 28, 2011 11:24:13 PM$"

import obengine.async
import obengine.vfs
import obengine.plugin
import obengine.depman

obengine.depman.gendeps()

def init():
    
    obengine.plugin.require('core.graphics')
    obengine.plugin.require('core.physics')

class Environment(object):

    _next_avail_id = 0

    def __init__(self, window_title = 'OpenBlox'):

        import obplugin.core.graphics
        import obplugin.core.physics

        self._eid = Envrionment._next_avail_id
        Envrionment._next_avail_id += 1
        
        self.scheduler = obengine.async.Scheduler()
        self.window = obplugin.core.graphics.Window(window_title, self.scheduler)
        self.physics_sandbox = obplugin.core.physics.World()

    @property
    def eid(self):
        return self._eid

