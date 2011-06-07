#
# This module provides SoundElement - a high-level world element that plays audio.
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
__date__  = "$Apr 2, 2011 7:51:54 AM$"


import obengine.element
import obengine.depman
import obengine.plugin
obengine.depman.gendeps()


def init():
    plugin.require('core.audio')


class SoundElement(obengine.element.Element):
    """
    Lets a sound be loaded and played inside an OpenBlox world.
    """
    def __init__(self, name, soundfile, volume = 50.0, looping = False, autoplay = False):
        """
         * name is just the name of this element
         * soundfile is the filename of the sound to load
         * looping specifies whether the sound should repeat, once it is finished
         * autoplay specifies whether the sound should start immediately after it is added to a world
        """

        import obplugin.core.audio

        obengine.element.Element.__init__(self, name)

        self._sound = obplugin.core.audio.Sound(soundfile, volume, looping, autoplay)
        self.on_loaded = self._sound.on_loaded
        self.looping = self._sound.__dict__['looping']
        self.playing = self._sound.__dict__['playing']
        self.volume = self._sound.__dict__['volume']
        
    def load(self):
        self._sound.load()
