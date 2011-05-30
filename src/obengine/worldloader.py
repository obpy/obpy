# obengine.worldloader
# ===================
#
# Provides an asynchronous world-loading algorithim.
#
# Copyright (C) 2011 The OpenBlox Project
# License: GNU GPL v3
#
# See <TODO: No Sphinx docs yet - add some!> for the primary source of documentation
# for this module.

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