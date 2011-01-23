"""
Copyright (C) 2010 The OpenBlox Project

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
__date__ ="$Jul 12, 2010 8:02:01 PM$"

class AttrDict(dict):
    """
    A decorated dict that links attributes to keys, so we can do this:
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

    a = AttrDict(a = 1, b = 2, c = 3)
    print a.a, a.b, a.c

    This should output:

    1 2 3
    """

    def __init__(self, **kwargs):
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