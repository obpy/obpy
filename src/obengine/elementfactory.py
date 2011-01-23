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
__date__ ="$Jan 23, 2011 7:57:35 AM$"

class ElementFactory(object):

    elements = [ 'brick', 'skybox', 'script' ]

    def make(self, name, *args):

        if name in self.elements:
            return getattr(self, 'make_' + name)(*args)

    def make_brick(self, name, coords, rgb, size = [2, 4, 1], hpr = [0, 0, 0], hidden = False, anchored = False):

        import obengine.gfx
        import obengine.gfx.element3d
        from obengine.cfg import get_config_var
        from obengine.element import BrickElement
        
        from pandac.PandaModules import Filename

        model = BrickElement(name, coords, rgb, size, hpr)
        view = obengine.gfx.get_rootwin().loader.loadModel(Filename.fromOsSpecific(get_config_var('cfgdir') + '/data/brick.egg'))
        presenter = obengine.gfx.element3d.BrickPresenter(model, view, hidden, anchored)

        return presenter

    def make_skybox(self, texture = None):

        from obengine.gfx.element3d import SkyboxElement

        element = SkyboxElement(texture)

        return element

    def make_script(self, name, code, filename = None):
        
        from obengine.scripting.element import ScriptElement

        element = ScriptElement(name, filename, code)

        return element