#
# This module provides a simple way (using factories) to create various elements, instead of
# directly instantiating them.
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
#
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
__date__ = "$Jan 23, 2011 7:57:35 AM$"


import obengine.depman

obengine.depman.gendeps()


def init():

    obengine.plugin.require('core.physics')
    obengine.plugin.require('core.graphics')


class ElementFactory(object):

    _element_factories = {}
    window = None
    sandbox = None

    def set_window(self, window):

        ElementFactory.window = window

        for element_factory in ElementFactory._element_factories.itervalues():
            if hasattr(element_factory, 'set_window'):
                element_factory.set_window(ElementFactory.window)

    def set_sandbox(self, sandbox):

        ElementFactory.sandbox = sandbox

        for element_factory in ElementFactory._element_factories.itervalues():
            if hasattr(element_factory, 'set_sandbox'):
                element_factory.set_sandbox(ElementFactory.sandbox)

    @staticmethod
    def register_element_factory(factory_cls):

        assert ElementFactory._element_factories.get(factory_cls.element_name) is None

        factory_instance = factory_cls()
        ElementFactory._element_factories[factory_cls.element_name] = factory_instance

        if hasattr(factory_instance, 'set_window') and ElementFactory.window is not None:
            factory_instance.set_window(ElementFactory.window)

        if hasattr(factory_instance, 'set_sandbox') and ElementFactory.sandbox is not None:
            factory_instance.set_sandbox(ElementFactory.sandbox)

    def make(self, name, *args, **kwargs):

        try:
            element_factory = self._element_factories[name]

        except KeyError:
            raise UnknownElementError(name)

        return element_factory.make(*args, **kwargs)


class UnknownElementError(Exception):
    """
    Raised when an unknown element type is passed to ElementFactory.make.
    """
    pass
