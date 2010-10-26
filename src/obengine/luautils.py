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
__date__ ="$Aug 2, 2010 2:25:56 PM$"

from types import MethodType

class TestObj:
    
    def test(self):
        
        print 'Ran!'
        return 'Ran'

    def __tolua__(self):

        return 'testc'

class LuaObjectWrapper(object):

    def __init__(self, obj):

        self.obj = obj

    def __getattr__(self, name):

        print 'getting', name

        if hasattr(self.obj, name) and type(getattr(self.obj, name)) == MethodType:
            
            func = getattr(self.obj, name)

            def wrapper(*args, **kwargs):

                args = args[:len(args) - 1]

                result = func(*args, **kwargs)

                return result

        elif hasattr(self.obj, name):

            return getattr(self.obj, name)

        raise AttributeError(name)