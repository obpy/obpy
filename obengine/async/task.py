#
# This module provides several differently behaving asynchronous tasks.
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
__date__ = "$May 4, 2011 11:24:29 AM$"


import time

import obengine.depman
obengine.depman.gendeps()


class Task(object):
    """
    Base task class, for other task classes to inherit from.
    This is still a useful class, if you want your task to run at
    the maximum possible speed.
    
    :param action: the function to run. It is called like this;
                   ``action(task, *args, **kwargs)``
    :param priority: the priority of this task. Task with a higher priority,
                     i.e, a higher value for this parameter, are run sooner
                     than tasks with a lower priority (a lower given value).
    :param name: the name of this task. If not given,
                 ``action.__name__`` will be used instead.
    :param args: an iterable containing arguments to pass
                 to *action* whenever it's called.
    :param kwargs: a dict or dict-like object that will be passed
                   to *action* when it's called.
    """

    AGAIN, STOP = range(2)

    def __init__(self, action, priority = 0, name = None, args = [], kwargs = {}):

        self.action = action
        self.name = name or action.__name__

        self.args = args
        self.kwargs = kwargs

        self.priority = priority

        self.time = 0.0

        self.scheduler = None

    def execute(self):

        tm = self._run_action()
        self.time += tm

    def _run_action(self):

        # Record how much time our action takes

        t1 = time.time()
        ret = self.action(self, *self.args, **self.kwargs)
        t2 = time.time()

        # Does our action want to be run again?
        if ret == self.AGAIN:
            self._reschedule()

        # Does it want to stop?
        elif ret == self.STOP:

            if self in self.scheduler.task_buffer:
                self.scheduler.task_buffer.remove(self)

        return t2 - t1

    def _reschedule(self):
        self.scheduler.add(self)

    def __cmp__(self, other):

        if hasattr(other, 'priority'):
            return - cmp(self.priority, other.priority)

        return 0


class PeriodicTask(Task):
    """
    See `Task` for documentation on the majority of these arguments.
    
    :param period: the time that should elapse between runs of this task.
                   Other tasks will run while this task is waiting, even
                   if their priority is lower.
    """

    def __init__(self, action, period, priority = 0, name = None, args = [], kwargs = {}):

        Task.__init__(self, action, priority, name, args, kwargs)

        self.period = period
        self.start_time = None

    def execute(self):

        # Is this the first time we've run?

        if self.start_time == None:

            self.start_time = time.time()
            self._reschedule()

        else:

            # We've run at least once before, so check to
            # see if our period has expired

            now = time.time()

            if now - self.start_time > self.period:

                self.time += now - self.start_time

                tm = self._run_action()

                self.time += tm
                self.start_time = time.time()

            else:
                self._reschedule()


class DelayedTask(Task):
    """
    See `Task` for documentation on the majority of these arguments.
    
    :param delay: how long to wait before running this task.
                  This doesn't block - other tasks still run.
        """

    def __init__(self, action, delay, priority = 0, name = None, args = [], kwargs = {}):

        Task.__init__(self, action, priority, name, args, kwargs)

        self.delay = delay
        self.start_time = None

    def execute(self):

        if self.start_time == None:

            # This is the first time we've been executed, so
            # put ourselves back into our scheduler

            self.start_time = time.time()
            self._reschedule()

        else:

            # We've run at least one time before, so check
            # to see if our delay is up

            now = time.time()

            if now - self.start_time > self.delay:
                self.scheduler.add(Task(self.action, self.name, self.args, self.kwargs))

            else:
                self._reschedule()
