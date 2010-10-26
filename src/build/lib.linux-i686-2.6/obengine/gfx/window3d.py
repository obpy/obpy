__author__="openblocks"
__date__ ="$Aug 5, 2010 3:26:05 PM$"

from direct.showbase.ShowBase import ShowBase

class Window3D(object, ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

    def connect_on_update(self, func):

        self.taskMgr.add(func, func.__name__)

