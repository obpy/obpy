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
__date__ ="$Feb 22, 2011 5:11:32 PM$"

class Event(object):

    def __init__(self):
        self.handlers = set()

    def add_handler(self, handler):

        self.handlers.add(handler)
        return self

    def remove_handler(self, handler):

        try:
            self.handlers.remove(handler)

        except:
            raise ValueError('Given handler is not handling this event, and thus cannot be removed')

    def fire(self, *args, **kwargs):

        for handler in self.handlers:
            handler(*args, **kwargs)

    def handler_count(self):
        return len(self.handlers)

    __iadd__ = add_handler
    __isub__ = remove_handler
    __call__ = fire