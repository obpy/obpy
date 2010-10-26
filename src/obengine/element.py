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
__date__ ="$Jul 13, 2010 6:13:05 PM$"

class Element(object):
    """
    The base class for all elements(i.e, scripts, bricks, etc...).
    You shouldn't make an instance of this class.
    """

    def __init__(self, name):

        self.name = name

    # Degenerate methods, for subclasses to override

    def on_add(self, world): pass

    def on_remove(self): pass

class ElementFactory(object):

    elements = [ 'brick', 'skybox', 'script' ]

    def make(self, name, *args):
        
        if name in self.elements:
            
            return getattr(self, 'make_' + name)(*args)

    def make_brick(self, name, coords, rgb, size = [2, 4, 1], hpr = [0, 0, 0], hidden = False, anchored = False):
        
        from obengine.gfx import get_rootwin
        from obengine.gfx.element3d import BrickPresenter
        from obengine.cfg import cfgdir

        model = BrickElement(name, coords, rgb, size, hpr)
        view = get_rootwin().loader.loadModel(cfgdir + '/data/brick.egg')
        presenter = BrickPresenter(model, view, hidden, anchored)
        
        return presenter
    
    def make_skybox(self, texture = None):

        from obengine.gfx.element3d import SkyboxElement
        
        element = SkyboxElement(texture)
        
        return element

    def make_script(self, name, code, filename = None):
        
        element = ScriptElement(name, filename, code)

        return element


class BrickElement(Element):
    
    def __init__(self, name, coords, rgb, size = [2, 4, 1], hpr = [0, 0, 0]):

        Element.__init__(self, name)

        self.coords = coords
        self.size = size
        self.hpr = hpr
        self.rgb = rgb

    def set_size(self, x, y, z):

        self.size[0] = x
        self.size[1] = y
        self.size[2] = z

    def set_pos(self, x, y, z):

        self.coords[0] = x
        self.coords[1] = y
        self.coords[2] = z

    def set_hpr(self, h, p, r):

        self.hpr[0] = h
        self.hpr[1] = p
        self.hpr[2] = r

    def set_rgb(self, r, g, b, a):

        self.rgb[0] = r
        self.rgb[1] = g
        self.rgb[2] = b
        self.rgb[3] = a

class ScriptElement(Element):

    def __init__(self, name, filename = None, code = None):

        Element.__init__(self, name)

        if filename != None:

            self.code = open(filename, 'r').read()

        else:

            self.code = code

    def on_add(self, world):

        from thread import start_new_thread

        self.world = world

        start_new_thread(self.run, ())


    def run(self):

        import obengine.luaengine as luaeng

        self.script_engine = luaeng.ScriptEngine(self.name)

        self.script_engine.expose(self.world)
        self.script_engine.expose(self)
        self.script_engine.execute(self.code)

    def __tolua__(self):

        return 'Script'