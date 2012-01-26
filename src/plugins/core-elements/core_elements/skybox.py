#
# <module description>
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
#
# Copyright (C) 2012 The OpenBlox Project
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
__date__ = "Jan 18, 2012 7:46:31 PM"


import xml.etree.ElementTree as xmlparser

from panda3d.core import CompassEffect

import obengine.math
import obengine.element
import obengine.plugin
import obengine.gfx.worldsource

from element_utils import XmlElementExtension


class SkyboxElement(obengine.element.Element):

    def __init__(self, window, texture = None):

        obengine.element.Element.__init__(self, 'Skybox')
        self.set_extension('xml', XmlSkyboxExtension)

        self._window = window
        self._texture = texture

        # Create the skybox (although the actual model is currently a skysphere!)

        obengine.plugin.require('core.graphics')

        import obplugin.core.graphics

        self.view = obplugin.core.graphics.Model('sky', self._window, clickable = False, cast_shadows = False, compress = False)

        self.on_add += self.sky_on_add
        self.on_remove += self.sky_on_remove

    def sky_on_add(self, _):

        self.view.load()

        while self.view.load_okay is False:
            self._window.scheduler.step()

        self.view.scale = obengine.math.Vector(5000, 5000, 5000)

        # TODO: Replace the below code with something not Panda-specific!

        self.view.panda_node.reparentTo(base.camera)
        self.view.panda_node.setShaderOff()
        self.view.panda_node.setLightOff()
        self.view.panda_node.setFogOff()
        self.view.panda_node.setBin('background', 0)
        self.view.panda_node.setDepthWrite(False)
        self.view.panda_node.setEffect(CompassEffect.make(self._window.panda_window.render))

        # Did the user specify a texture?

        if self._texture:
            self.view.texture = self._texture

    def sky_on_remove(self):
        self.sky.hide()


class SkyboxMaker(obengine.element.ElementMaker):

    element_name = 'skybox'

    def set_window(self, window):
        self._window = window

    def make(self, texture = None):

        element = SkyboxElement(self._window, texture)
        return element


obengine.elementfactory.ElementFactory.register_element_factory(SkyboxMaker)


class XmlSkyboxExtension(XmlElementExtension):

    def __init__(self, skybox):
        self._skybox = skybox

    @property
    def xml_element(self):

        attributes = {}

        if self._skybox._texture is not None:
            attributes['texture'] = self._skybox._texture

        element = xmlparser.Element('skybox', attributes)
        return element


class XmlSkyboxParser(obengine.element.XmlElementParser):

    tag = 'skybox'

    def parse(self, node):

        element = self._element_factory.make('skybox', node.attrib.get('src'))
        return element


obengine.gfx.worldsource.WorldSource.add_element_parser(XmlSkyboxParser)
