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

__author__="openblocks"
__date__ ="$Apr 14, 2011 5:34:04 AM$"

from obengine.gfx import get_rootwin

class KeyEvent(object):
    
    A_KEY = 0
    B_KEY = 1
    X_KEY = 2
    Y_KEY = 3
    
    key_conv = {
    
    A_KEY : 'q',
    B_KEY : 'w',
    
    X_KEY : 's',
    Y_KEY : 'd'
    
    }
    
    TYPE_REPEAT = 0
    TYPE_DOWN = 1
    TYPE_UP = 2
    
    type_conv = {
    
    TYPE_REPEAT : 'repeat',
    TYPE_DOWN : 'down',
    TYPE_UP : 'up'
    
    }

    @property
    def key(self):
        return self._raw_key_val

    @key.setter
    def key(self, value):

        self._key = self.key_conv[value]
        self._raw_key_val = value

    @property
    def type(self):
        return self._raw_type_val

    @type.setter
    def type(self, value):

        self._type = self.type_conv[value]
        self._raw_type_val = value

    def start(self):
        get_rootwin().accept('%s-%s' % (self._key, self._type), self.fire)

    def fire(self, __):
        self.handler(self)

class TimerEvent(object):

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        self._interval = value

    def start(self):
        get_rootwin().taskMgr.add(self.fire, self.handler.__name__ + str(self.interval))

    def stop(self):
        get_rootwin().taskMgr.remove(self.handler.__name__ + str(self.interval))

    def fire(self, task):

        if task.time % self.interval == 0:
            self.handler(self)
            
        return task.cont