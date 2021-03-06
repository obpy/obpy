#
# This module provides SoundElement - a high-level world element that plays audio.
#
# Copyright (C) 2011-2012 The OpenBlox Project
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
__date__ = "$Apr 2, 2011 7:51:54 AM$"


import xml.etree.ElementTree as xmlparser

import obengine.element
import obengine.elementfactory
import obengine.plugin
import obengine.gfx.worldsource
import obengine.depman
obengine.depman.gendeps()


class SoundElement(obengine.element.Element):
    """
    Lets a sound be loaded and played inside an OpenBlox world.
    """
    def __init__(self, name, soundfile, window, volume = 50.0, looping = False, autoplay = True):
        """
         * name is just the name of this element
         * soundfile is the filename of the sound to load
         * looping specifies whether the sound should repeat, once it is finished
         * autoplay specifies whether the sound should start immediately after it is added to a world
        """

        obengine.plugin.require('core.audio')

        import obplugin.core.audio

        obengine.element.Element.__init__(self, name)

        self.set_extension('xml', XmlSoundExtension)

        self._sound = obplugin.core.audio.Sound(soundfile, window, volume, looping, autoplay)
        self._soundfile = soundfile

        self.on_loaded = self._sound.on_loaded

        if autoplay is True:
            self.on_world_loaded += self._sound.load

    def load(self):
        self._sound.load()

    def play(self):
        self._sound.playing = True

    @property
    def sound(self):
        return self._soundfile


class XmlSoundExtension(object):

    def __init__(self, sound):
        self._sound = sound

    @property
    def xml_element(self):

        attributes = {
        'name' : self._sound.name,
        'src' : self._sound.sound
        }

        element = xmlparser.Element('sound', attributes)
        return element


class XmlSoundParser(obengine.element.XmlElementParser):

    tag = 'sound'

    def parse(self, node):

        yes_no = { 'yes' : True, 'no' : False}

        try:

            name = node.attrib['name']
            src = node.attrib['src']
            autoplay = yes_no[node.attrib.get('autoplay', 'no')]

        except KeyError, message:
            raise obengine.element.XmlParseError(message)

        # Create the element
        element = self._element_factory.make('sound', name, src, autoplay)

        return element


obengine.gfx.worldsource.WorldSource.add_element_parser(XmlSoundParser)


class SoundMaker(obengine.element.ElementMaker):

    element_name = 'sound'

    def set_window(self, window):
        self._window = window

    def make(self, name, soundfile, autoplay = False):

        element = SoundElement(name, soundfile, self._window, autoplay = autoplay)
        return element


obengine.elementfactory.ElementFactory.register_element_factory(SoundMaker)
