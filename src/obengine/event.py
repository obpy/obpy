#
# This module provides some basic, generic, event-handling facilites.
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


__author__="openblocks"
__date__ ="$Feb 22, 2011 5:11:32 PM$"


import obengine.depman
obengine.depman.gendeps()


class Event(object):
    """
    Basic event manager.

    Use __iadd__ or add_handler to add a handler for an Event instance.
    Next, use __call__ or fire to trigger all bound handlers.
    You can also use __isub__ or remove_handler to remove a bound handler.

    Sample usage:

        >>> def callback():
        ...     print 'Callback called!'
        ...
        >>> event = Event()
        >>> event += callback
        >>> event()
        Callback called!
        
    Event callbacks can also be removed:
    
        >>> event -= callback
        >>> event()
        >>>

    Arguments given to the Event instance are passed to each callback, as well:

        >>> def callback_with_args(arg1, arg2):
        ...     print 'arg1:', arg1, 'arg2:', arg2
        ...
        >>> event += callback_with_args
        >>> event('Hello,', 'World!')
        arg1: Hello, arg2: World!

    You can temporarily disable an event, too:

        >>> event.disable()
        >>> event('Hello,', 'World!')
        >>> event.enable()
        >>> event('Hello,', 'World!')
        arg1: Hello, arg2: World!
        >>> event.enabled = False
        >>> event('Hello,', 'World!')
        >>> event.enabled = True
        >>> event('Hello,', 'World!')
        arg1: Hello, arg2: World!

    You can also clear all the handlers:

        >>> event.clear()
        >>> event('Hello,', 'World!')
        >>>
    """

    def __init__(self):

        self.enabled = True
        self.handlers = set()

    def add_handler(self, handler):

        self.handlers.add(handler)

        # Return self, for __iadd__ compatibility
        return self

    def remove_handler(self, handler):
        """
        Removes handler handler from this Event's set of bound handlers.
        Raises ValueError if the handler isn't in the set in the first place.
        """

        try:
            
            self.handlers.remove(handler)
            return self

        except:
            raise ValueError('Given handler is not handling this event, and thus cannot be removed')

    def fire(self, *args, **kwargs):
        """
        Triggers this Event.
        All handlers are fired, one after another, with all given arguments to this
        method passed on to them.
        """

        if self.enabled is False:
            return

        for handler in reversed(list(self.handlers)):
            handler(*args, **kwargs)

    def handler_count(self):
        """
        Returns the current number of handlers.
        """
        return len(self.handlers)

    def clear(self):
        self.handlers = set()

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    __iadd__ = add_handler
    __isub__ = remove_handler
    __call__ = fire
    __len__ = handler_count
    