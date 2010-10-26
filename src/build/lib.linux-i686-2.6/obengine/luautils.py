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
         
        if hasattr(self.obj, name) and type(getattr(self.obj, name)) == MethodType:
            
            func = getattr(self.obj, name)

            def wrapper(*args, **kwargs):

                args = args[:len(args) - 1]

                result = func(*args, **kwargs)

                return result

        elif hasattr(self.obj, name):

            return getattr(self.obj, name)

        raise AttributeError(name)