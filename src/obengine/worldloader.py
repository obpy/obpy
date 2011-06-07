#
# This module provides an asynchronous world-loading algorithim.
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
#
#
# Copyright (C) 2010-2011 The OpenBlox Project
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

__author__="openblocks"
__date__ ="$May 28, 2011 11:26:46 AM$"

import obengine.event
import obengine.async
import obengine.utils
import obengine.depman

obengine.depman.gendeps()

class WorldLoader(object):

    _PRIORITY_RANGE = (35, 20)

    def __init__(self, world, source, scheduler):

        self._world = world
        self._source = source
        self._scheduler = scheduler

        self.on_world_loaded = obengine.event.Event()

    def load(self):

        num_elements = len(self._source)

        for index, element in enumerate(self._source):

            loader = obengine.async.AsyncCall(
            self._load_single_element,
            self._get_priority(index, num_elements),
            element,
            index,
            num_elements
            )

            self._scheduler.add(loader)

    def _load_single_element(self, element, element_index, num_elements):

        self._world.element.add_node(element)

        if element_index + 1 == num_elements:
            self.on_world_loaded()

    def _get_priority(self, element_index, num_elements):
        
        orig_range = (0, num_elements)

        priority = obengine.utils.interp_range(
        orig_range,
        self._PRIORITY_RANGE,
        element_index 
        )

        return priority