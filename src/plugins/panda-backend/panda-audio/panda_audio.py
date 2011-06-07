#
# This plugin provides a Panda3D-based audio backend.
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
__date__  = "$May 24, 2011 3:27:05 PM$"


from panda3d.core import Filename, AudioSound

import obengine.vfs
import obengine.event
import obengine.async
import obengine.depman

obengine.depman.gendeps()


class Sound(object):

    LOAD_PRIORITY = 10

    def __init__(self, filename, window, volume = 50.0, looping = False, autoplay = False):

        self.sound_file = filename
        self._window = window
        self._looping = False
        self._autoplay = False
        self._volume = volume

        self.on_loaded = obengine.event.Event()

    def load(self):
        self._window.scheduler.add(obengine.async.Task(self._actual_load, priority = Sound.LOAD_PRIORITY))

    @property
    def playing(self):
        return self._sound.status() == AudioSound.PLAYING

    @playing.setter
    def playing(self, play):

        if play is True:
            if self._sound.status() == AudioSound.READY:
                self._sound.play()

        else:
            if self._sound.status() == AudioSound.PLAYING:
                self._sound.stop()

    @property
    def looping(self):
        return self._looping

    @looping.setter
    def looping(self, loop):

        self._looping = loop
        self._sound.setLoop(loop)

    @property
    def volume(self):
        return self._sound.getVolume() * 100.0

    @volume.setter
    def volume(self, new_volume):
        self._sound.setVolume(new_volume / 100.0)


    def _actual_load(self, _):

        panda_filename = Filename.fromOsSpecific(obengine.vfs.getsyspath(filename))

        self._sound = self._window.panda_window.loader.loadSfx(panda_filename)

        self.looping = self._looping
        self.volume = self._volume

        if self._autoplay is True:
            self.playing = True

        self.on_loaded()
