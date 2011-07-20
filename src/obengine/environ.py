#
# This module provides a all-in-one class that's used as a shortcut for
# obengine.async.Scheduler, obengine.world.World, obplugin.core.graphics.Window,
# and obplugin.core.physics.World.
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
#
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

        self._eid = Environment._next_avail_id
        Environment._next_avail_id += 1
        
        self.scheduler = obengine.async.Scheduler()
        self.window = obplugin.core.graphics.Window(window_title, self.scheduler)
        self.physics_sandbox = obplugin.core.physics.World()

    @property
    def eid(self):
        return self._eid