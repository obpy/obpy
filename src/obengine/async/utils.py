#
# This module provides several misc. asynchronous utilites.
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
__date__ ="$May 4, 2011 11:27:45 AM$"


import sys

import obengine.log
import obengine.async.task
import obengine.depman
obengine.depman.gendeps()


class LoopingCall(object):
    """
    Helper class to easily wrap an existing method for use with obengine.async.Scheduler.
    It is similar to, and inspired by, Twisted's LoopingCall factory.

    NOTE: If the given method throws an unhandled exception, the exception's traceback is logged,
    and the method will not be called further.
    """

    def __init__(self, action, priority = 0, delay = 0.0):

        self.action = action
        self.priority = priority
        self.delay = delay

        if self.delay != 0.0:
            self.task = obengine.async.task.PeriodicTask(self.run_action, delay, priority)

        else:
            self.task = obengine.async.task.Task(self.run_action, priority)
            
        self.execute = self.task.execute

    def run_action(self, task):

        try:
            self.action()
        
        except:

            info = sys.exc_info()
            exc_type = str(info[0])
            exc_value = str(info[1])
            exc_traceback = info[2]

            obengine.log.error(
            'Unhandled exception %s inside looping call:\nMessage: %s\nTraceback: %s' % (
                exc_type, exc_value, exc_traceback
                )
            )

            return task.STOP

        else:
            return task.AGAIN

    @property
    def scheduler(self):
        return self.task.scheduler

    @scheduler.setter
    def scheduler(self, sched):
        self.task.scheduler = sched

    @property
    def name(self):
        return self.task.name


class AsyncCall(object):

    def __init__(self, method, priority, *args, **kwargs):

        self._method = method
        self._finished = False
        
        self.priority = priority

        self.method_args = args
        self.method_kwargs = kwargs

    def execute(self):

        self._result = self._method(*self.method_args, **self.method_kwargs)
        self._finished = True

    def wait(self):
        while self.finished is False:
            self.scheduler.step()

    @property
    def finished(self):
        return self._finished

    @property
    def result(self):
        return self._result
