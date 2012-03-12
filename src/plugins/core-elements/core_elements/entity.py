#
# <module description>
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
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
__date__ = "Dec 27, 2011 9:34:19 PM"


import obengine.event
import obengine.datatypes
import obengine.element
import obengine.math

import obplugin.core.physics


class EntityElement(obengine.element.Element):

    def __init__(self, name, max_health, respawn = True, respawn_filter = None, parent = None):

        obengine.element.Element.__init__(self, name, parent)

        self._max_health = max_health
        self._health = health
        self.on_health_changed = obengine.event.Event()
        self.on_max_health_changed = obengine.event.Event()
        self.on_died = obengine.event.Event()

        self._velocity = obengine.math.Vector()
        self.on_falling = obengine.event.Event()

        self._respawn = respawn
        self._respawn_filter = respawn_filter

    def take_damage(self, damage):

        self._health = max(0, self.health - damage)

        if self._health == 0:
            self.on_died()

    @obengine.datatypes.nested_property
    def max_health():

        def fget(self):
            return self._max_health

        def fset(self, new_max_health):

            old_max_health = self.max_health
            self._max_health = new_max_health

            if self.max_health != old_max_health:
                self.on_max_health_changed(self.max_health)

        return locals()

    @obengine.datatypes.nested_property
    def health():

        def fget(self):
            return self._health

        def fset(self, new_health):

            self._health = max(0, new_health)

            if self._health == 0:
                self.on_died()

        return locals()

    def take_damage(self, damage):
        self.health -= damage
