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
__date__ = "Dec 19, 2011 3:58:46 PM"


import obengine.interface
import obengine.event
import obengine.element
import obengine.gfx.player


class ToolElement(obengine.element.Element):

    def __init__(self, name, script, model = None):

        obengine.element.Element.__init__(self, name)

        self._script = script
        self._model = model
        if self._model is not None:
            self._model.hide()
        self._player = None

        self.on_equipped = obengine.event.Event()
        self.on_unequipped = obengine.event.Event()

        self.on_parent_changed += self._check_for_equip

        self._script.parent = self
        self._script.execute()

    def equip(self):

        assert self._player is not None

        self._model.show()
        self.on_equipped()

    def unequip(self):

        assert self._player is not None

        self._model.hide()
        self.on_unequipped()

    def _check_for_equip(self, new_parent):

        if obengine.interface.implements(new_parent, obengine.gfx.player.PlayerController):

            self._player = new_parent
            if self._model is not None:
                # TODO: Replace use of private attributes here with something better!
                self._model.parent = self._player._view._model
