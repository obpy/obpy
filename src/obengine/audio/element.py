"""
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
__date__ ="$Apr 2, 2011 7:51:54 AM$"

import os

import obengine.gfx
import obengine.element

from panda3d.core import Filename, AudioSound

class SoundElement(obengine.element.Element):

    def __init__(self, name, soundfile, autoplay=False):
        """
        This is just like all other elements.
        soundfile
        """

        obengine.element.Element.__init__(self, name)

        self.sound = obengine.gfx.get_rootwin().loader.loadSfx(Filename.fromOsSpecific(os.path.join(os.abspath(os.curdir)), soundfile))

        if autoplay == True:
            self.on_add += self.autoplay

        self.on_remove += self.stop

    def autoplay(self, world):
        self.play()

    def play(self):
        """
        Plays the sound, if it is not playing already.
        """

        if self.sound.status() == AudioSound.READY:
            self.sound.play()

    def stop(self):
        """
        Stops the sound, if it is playing.
        """

        if self.sound.status() == AudioSound.PLAYING:
            self.sound.stop()

    def set_volume(self, percentage):
        """
        Sets the volume. percentage (the volume) is anywhere between 0 (silent) and 100 (maximum).
        """

        self.sound.setVolume(percentage / 100.0)

    def get_volume(self):
        """
        Retrieves the volume, as a percentage between 0 and 100.
        """
        return self.sound.getVolume() * 100.0