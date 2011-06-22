#
# This module provides a simple scheduling class.
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
__date__  = "$May 4, 2011 11:24:00 AM$"


import obengine.datatypes
import obengine.depman
obengine.depman.gendeps()


class Scheduler(object):
    """
    Asynchronous task scheduler.
    NOTE: If you're using a non-dummy renderer, then everything that has a lower priority
    than the rendering task will run at the renderer's frame rate.
    """

    def __init__(self):

        self.queue = obengine.datatypes.heap()
        self.task_buffer = set()

    def add(self, task):
        """Adds a task to the task buffer
        Arguments:
         * task - the task to add
        """

        task.scheduler = self
        self.task_buffer.add(task)

    def empty(self):
        """Checks to see if this scheduler is empty
        Returns True if there are no more tasks to run, False otherwise.
        """
        return not self.queue and not self.task_buffer

    def loop(self):
        """Loops this scheduler
        Runs forever, or at least until there are no more tasks to run :)
        """

        while True:

            try:
                self.step()

            except TaskBufferEmptyException:
                break

    def step(self):

        if len(self.task_buffer) == 0 and len(self.queue) == 0:
            raise TaskBufferEmptyException

        elif len(self.queue) == 0:
            self._copy_from_task_buffer()

        task = self.queue.pop()
        task.execute()

    def _copy_from_task_buffer(self):

        self.queue.extend(self.task_buffer)
        self.task_buffer.clear()

    def _priority_sort(self, task1, task2):
        return cmp(task1.priority, task2.priority)


class TaskBufferEmptyException(Exception):
    pass