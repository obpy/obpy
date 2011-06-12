import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.pardir, os.pardir)))

from obengine.interface import *

class TestClass(object):

    def __init__(self, a, b, c):
        pass

    def do_x(self, x):
        pass

    def do_y(self, y):
        pass

    def do_z(self, z):
        pass

class TestInterface1(object):

    def do_z(self, z):
        pass

class TestInterface2(object):

    def __init__(self, a, b, c):
        pass

    def do_x(self, x):
        pass

class TestInterface3(object):

    def __init__(self, a, b, c, d):
        pass

if __name__ == '__main__':

    print 'implements(TestClass, TestInterface1):', implements(TestClass, TestInterface1)
    print 'implements(TestClass, TestInterface2):', implements(TestClass, TestInterface2)
    print 'implements(TestClass, TestInterface3):', implements(TestClass, TestInterface3)
