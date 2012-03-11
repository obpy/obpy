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
__date__ = "Nov 25, 2011 1:36:48 PM"


import copy
import functools
import xml.etree.ElementTree as xmlparser

import obengine.element
import obengine.elementfactory
import obengine.gfx.worldsource

from element_utils import XmlElementExtension


DEFAULT_X_SIZE = 2.0
DEFAULT_Y_SIZE = 4.0
DEFAULT_Z_SIZE = 1.0


class BrickMaker(obengine.element.ElementMaker):

    element_name = 'brick'

    def set_window(self, window):
        self._window = window

    def set_sandbox(self, sandbox):
        self._sandbox = sandbox

    def make(self, name, coords = None, color = None,
             size = None, rotation = None, anchored = False):

        import obplugin.core.physics

        coords = coords or obengine.math.Vector(0, 0, 0)
        color = color or obengine.math.Color(0, 0, 0, 255)
        size = size or  obengine.math.Vector(2, 4, 1)
        rotation = rotation or obengine.math.EulerAngle(0, 0, 0)

        view = BlockBrickView(size, rotation, color, self._window)
        view.load()

        scheduler = self._window.scheduler

        while view.loaded is False:
            scheduler.step()

        phys_size = copy.deepcopy(size)

        phys_rep = obplugin.core.physics.Box(view.model, self._sandbox, None, scheduler, anchored, size = phys_size)
        phys_rep.load()

        while phys_rep.loaded is False:
            scheduler.step()

        controller = BrickPresenter(name, coords, color, size, rotation, view, phys_rep)
        return controller


obengine.elementfactory.ElementFactory.register_element_factory(BrickMaker)


class BrickView(object):
    """
    Base view for all different sorts of bricks.
    To use, simply create a variable called type in your subclass, that corresponds to a model file in data/.
    Then, implement set_size, set_hpr, set_pos, and set_color methods
    that take obengine.math.Vector, obengine.math.EulerAngle, or obengine.math.Color as arguments.
    """

    def __init__(self, size, rotation, color, window):

        import obplugin.core.graphics
        self.model = obplugin.core.graphics.Model(self.type, window)
        self.on_click = self.model.on_click

        self.on_loaded = self.model.on_loaded
        self.on_loaded += functools.partial(self._init_attrs, size, rotation, color)

    def hide(self):
        self.showing = False

    def show(self):
        self.showing = True

    def load(self, async = True):
        self.model.load(async)

    @obengine.datatypes.nested_property
    def showing():

        def fget(self):
            return self.model.showing

        def fset(self, show):
            self.model.showing = show

        return locals()

    @property
    def bounds(self):
        return self.model.bounds

    @property
    def loaded(self):
        return self.model.load_okay

    def _init_attrs(self, size, rotation, color):

        self.size = size
        self.rotation = rotation
        self.color = color


class BlockBrickView(BrickView):

    type = 'brick-flat'

    def __init__(self, size, rotation, color, window):
        BrickView.__init__(self, size, rotation, color, window)

    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return self.model.position

        def fset(self, new_pos):
            self.model.position = new_pos

        return locals()

    @obengine.datatypes.nested_property
    def size():

        def fget(self):

            size = self.model.scale
            brick_size = obengine.math.Vector(
            size.x * DEFAULT_X_SIZE,
            size.y * DEFAULT_Y_SIZE,
            size.z * DEFAULT_Z_SIZE
            )

            return brick_size

        def fset(self, new_size):

            self.model.scale = (
            new_size.x / DEFAULT_X_SIZE,
            new_size.y / DEFAULT_Y_SIZE,
            new_size.z / DEFAULT_Z_SIZE
            )

        return locals()

    @obengine.datatypes.nested_property
    def rotation():

        def fget(self):
            return self.model.rotation

        def fset(self, new_rot):
            self.model.rotation = new_rot

        return locals()

    @obengine.datatypes.nested_property
    def color():

        def fget(self):
            return self.model.color

        def fset(self, new_color):
            self.model.color = new_color

        return locals()


class BrickPresenter(obengine.element.Element):

    def __init__(self, name, position, color, size, rotation, view, phys_rep):

        obengine.element.Element.__init__(self, name)
        self.set_extension('xml', XmlBrickExtension)

        self.view = view
        self.on_click = self.view.on_click

        self.on_add += self._on_add
        self.on_remove += self._on_remove

        self.phys_rep = phys_rep
        self.phys_rep.owner = self
        self.on_collision = self.phys_rep.on_collision

        self.position = position
        self.color = color
        self.rotation = rotation

    def hide(self):

        self.view.hide()
        self.phys_rep.disable()

    def show(self):

        self.view.show()
        self.phys_rep.enable()

    @obengine.datatypes.nested_property
    def showing():

        def fget(self):
            return self.view.showing

        def fset(self, showing):

            if showing is True:
                self.show()

            else:
                self.hide()

        return locals()

    @obengine.datatypes.nested_property
    def size():

        def fget(self):
            return self.view.size

        def fset(self, new_size):

            self.view.size = new_size
            self.phys_rep.size = new_size

        return locals()

    @obengine.datatypes.nested_property
    def rotation():

        def fget(self):
            return self.view.rotation

        def fset(self, new_rot):

            self.view.rotation = new_rot
            self.phys_rep.rotation = new_rot

        return locals()

    @obengine.datatypes.nested_property
    def position():

        def fget(self):
            return self.view.position

        def fset(self, new_pos):

            self.view.position = new_pos
            self.phys_rep.position = new_pos

        return locals()

    @obengine.datatypes.nested_property
    def color():

        def fget(self):
            return self.view.color

        def fset(self, new_color):
            self.view.color = new_color

        return locals()

    @obengine.datatypes.nested_property
    def anchored():

        def fget(self):
            return self.phys_rep.anchored

        def fset(self, anchored):
            self.phys_rep.anchored = anchored

        return locals()

    @obengine.datatypes.nested_property
    def can_collide():

        def fget(self):
            return self.phys_rep.enabled

        def fset(self, can_collide):

            if can_collide is True:
                self.phys_rep.enable()
            else:
                self.phys_rep.disable()

        return locals()

    @property
    def bounds(self):
        return self.view.bounds

    def _on_add(self, world):

        self.world = world
        self.phys_rep.enable()

    def _on_remove(self):

        self.showing = False
        self.phys_rep.disable()


class XmlBrickExtension(XmlElementExtension):

    def __init__(self, brick):
        self._brick = brick

    @property
    def xml_element(self):

        attributes = {
        'name' : self._brick.name,
        'coords' : self._vector_str(self._brick.position),
        'rgb' : self._color_str(self._brick.color),
        'orientation' : self._euler_str(self._brick.rotation),
        'size' : self._vector_str(self._brick.size),
        'anchored' : self._bool_str(self._brick.anchored)
        }

        element = xmlparser.Element('brick', attributes)

        return element


class XmlBrickParser(obengine.element.XmlElementParser):

    tag = 'brick'

    def parse(self, node):

        rgb = obengine.math.Color()
        coords = obengine.math.Vector()
        orientation = obengine.math.EulerAngle()
        size = obengine.math.Vector()
        anchored = False

        # Remove all empty space first, to make string to number conversion easy

        try:

            coordstr = node.attrib['coords'].replace(' ', '')
            rgbstr = node.attrib['rgb'].replace(' ', '')
            orient_str = node.attrib['orientation'].replace(' ', '')
            size_str = node.attrib['size'].replace(' ', '')
            name = node.attrib['name']

        except KeyError, message:
            raise BadWorldError(message)

        if node.attrib.has_key('anchored'):

            if node.attrib['anchored'] == 'yes':
                anchored = True

        try:

            coords.x = float(coordstr.split(',')[0])
            coords.y = float(coordstr.split(',')[1])
            coords.z = float(coordstr.split(',')[2])

            rgb.r = float(rgbstr.split(',')[0])
            rgb.g = float(rgbstr.split(',')[1])
            rgb.b = float(rgbstr.split(',')[2])
            rgb.a = float(rgbstr.split(',')[3])

            orientation.h = float(orient_str.split(',')[0])
            orientation.p = float(orient_str.split(',')[1])
            orientation.r = float(orient_str.split(',')[2])

            size.x = float(size_str.split(',')[0])
            size.y = float(size_str.split(',')[1])
            size.z = float(size_str.split(',')[2])

        except IndexError, message:
            raise obengine.element.XmlParseError(message)

        element = self._element_factory.make('brick', name, coords, rgb, size, orientation, anchored)
        return element


obengine.gfx.worldsource.WorldSource.add_element_parser(XmlBrickParser)
