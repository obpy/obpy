"""
Copyright (C) 2011 The OpenBlox Project

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

__author__ = "openblocks"
__date__  = "$May 4, 2011 8:08:03 PM$"

import event
import depman

depman.gendeps()

class AttrDict(dict):
    """
    A decorated dict that links attributes to keys, so we can do this:

    from obengine.attrdict import AttrDict

    a = AttrDict()
    a.Key1 = "Test1"
    a.Key2 = "Test2"

    print a.Key1
    print a['Key1']
    print a.Key2
    print a['Key2']

    This should output:

    Test1
    Test1
    Test2
    Test2

    NEW IN 0.5:

    You can also initalize AttrDict like a regular dict:

    from obengine.attrdict import AttrDict

    a = AttrDict(a = 1, b = 2, c = 3)
    print a.a, a.b, a.c

    This should output:

    1 2 3
    """

    def __init__(self, **kwargs):
        """Just like initalizing a normal dict. See dict.__init__ for more info.
        """
        dict.__init__(self, **kwargs)

    def __getattr__(self, item):
        try:
            return self.__getitem__(item)
        except:
            raise AttributeError(item)

    def __setattr__(self, item, value):
        if self.__dict__.has_key(item):
            dict.__setattr__(self, item, value)
        else:
            self.__setitem__(item, value)

class Borg(object):
    
    __shared_state = {}

    def __new__(cls, *p, **k):

        self = object.__new__(cls)
        self.__dict__ = cls.__shared_state

        return self

class EventDict(dict):

    def __init__(self, *args, **kwargs):

        dict.__init__(self, *args, **kwargs)

        self.on_item_added = event.Event()
        self.on_item_retrieved = event.Event()
        self.on_item_changed = event.Event()
        self.on_item_removed = event.Event()

    def __getitem__(self, key):

        item = dict.__getitem__(self, key)
        self.on_item_retrieved(key)

        return item

    def __setitem__(self, key, value):

        item_changed = False
        item_added = False

        if self.has_key(key):
            item_changed = True

        else:
            item_added = True

        dict.__setitem__(self, key, value)

        item_value = dict.__getitem__(self, key)

        if item_changed is True:
            self.on_item_changed(key, item_value)

        else:
            self.on_item_added(key, item_value)

    def __delitem__(self, key):

        dict.__delitem__(self, key)
        self.on_item_removed

def wrap_callable(func, before, after):
    
    def wrapper(*args, **kwargs):

        try:

            before(*args, **kwargs)
            return func(*args, **kwargs)
        
        finally:
            after(*args, **kwargs)