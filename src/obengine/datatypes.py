#
# This module provides a generic place to put custom datatypes.
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
__date__  = "$May 4, 2011 8:08:03 PM$"


import collections

import event
import depman

depman.gendeps()

class AttrDict(dict):
    """
    A decorated dict that links attributes to keys, so we can do this:

    >>> a = AttrDict()
    >>> a.Key1 = "Test1"
    >>> a.Key2 = "Test2"

    >>> print a.Key1
    Test1
    >>> print a['Key1']
    Test1
    >>> print a.Key2
    Test2
    >>> print a['Key2']
    Test2

    NEW IN OpenBlox 0.5:

    You can also initalize AttrDict like a regular dict:

    >>> a = AttrDict(a = 1, b = 2, c = 3)
    >>> print a.a, a.b, a.c
    1 2 3
    """

    def __init__(self, **kwargs):
        """Just like initalizing a normal dict. See dict.__init__ for more info."""
        dict.__init__(self, **kwargs)

    def __getattr__(self, item):

        try:
            return object.__getattr__(self, item)

        except AttributeError:
            pass

        try:
            return dict.__getitem__(self, item)
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, item, value):
        self[item] = value


class Borg(object):
    
    __shared_state = {}

    def __new__(cls):

        self = object.__new__(cls)
        self.__dict__ = cls.__shared_state

        return self


class EventDict(dict):

    def __init__(self, **kwargs):

        dict.__init__(self, **kwargs)

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
        self.on_item_removed()


class EventAttrDict(EventDict, AttrDict):

    def __init__(self, **kwargs):

        EventDict.__init__(self, **kwargs)
        AttrDict.__init__(self, **kwargs)


class orderedset(collections.MutableSet):
    """Ordered set - like a set, but remembers insertion order
    Based on Raymond Hettinger's MIT-licensed ASPN recipe(
    http://code.activestate.com/recipes/576694/).
    This class' source code is GPLed, but the original code, as stated above,
    is under the MIT license (http://www.opensource.org/licenses/mit-license.php).

    Example:

        >>> o = orderedset('The quick brown fox...')
        >>> o
        orderedset(['T', 'h', 'e', ' ', 'q', 'u', 'i', 'c', 'k', 'b', 'r', 'o', 'w', 'n', 'f', 'x', '.'])
        >>> o.add(5)
        >>> o.add(2)
        >>> o
        orderedset(['T', 'h', 'e', ' ', 'q', 'u', 'i', 'c', 'k', 'b', 'r', 'o', 'w', 'n', 'f', 'x', '.', 5, 2])
        >>> for item in o:
        ...     print item,
        ...
        T h e   q u i c k b r o w n f x . 5 2
    """
    
    KEY, PREV, NEXT = range(3)
    
    def __init__(self, iterable = None):
        
        self._end = end = []
        end += [None, end, end]
        self._map = {}
        
        if iterable is not None:
            self |= iterable
            
    def add(self, key):
        
        if key not in self:
            
            end = self._end
            curr_key = end[orderedset.PREV]
            curr_key[orderedset.NEXT] = end[orderedset.PREV] = self._map[key] = [key, curr_key, end]
            
    def discard(self, key):
        
        if key in self:
            
            key, prev_key, next_key = self._map.pop(key)
            prev_key[orderedset.NEXT] = next_key
            next_key[orderedset.PREV] = prev_key
            
    def pop(self, last = True):
        
        if not self:
            raise KeyError('orderedset is empty')
        
        key = next(reversed(self)) if last else next(iter(self))
        self.discard(key)
        return key
        
    def __len__(self):
        return len(self._map)
    
    def __contains__(self, key):
        return key in self._map
    
    def __reversed__(self):
        
        end = self._end
        curr_key = end[orderedset.PREV]
        
        while curr_key is not end:
            
            yield curr_key[orderedset.KEY]
            curr_key = curr_key[orderedset.PREV]

    def __iter__(self):

        end = self._end
        curr_key = end[orderedset.NEXT]

        while curr_key is not end:

            yield curr_key[orderedset.KEY]
            curr_key = curr_key[orderedset.NEXT]
            
    def __repr__(self):
        
        if not self:
            return '%s()' % (self.__class__.__name__,)
        
        return '%s(%r)' % (self.__class__.__name__, list(self))
    
    def __eq__(self, other):
        
        if isinstance(other, self.__class__):
            return len(self) == len(other) and list(self) == list(other)
        
        return set(self) == set(other)
    
    def __del__(self):
        self.clear()

def nested_property(func):
    
    func_locals = func()
    func_locals['doc'] = func.__doc__
    
    return property(**func_locals)


def wrap_callable(func, before, after):
    
    def wrapper(*args, **kwargs):

        try:

            before(*args, **kwargs)
            return func(*args, **kwargs)
        
        finally:
            after(*args, **kwargs)