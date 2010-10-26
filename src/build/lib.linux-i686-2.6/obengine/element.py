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

    def on_add(self): pass

    def on_remove(self): pass

class ElementFactory(object):

    elements = [ 'brick', 'skybox' ]

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

    def set_rgb(self, r, g, b):

        self.rgb[0] = r
        self.rgb[1] = g
        self.rgb[2] = b