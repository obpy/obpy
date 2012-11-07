==============================
OpenBlox's asynchronous system
==============================

.. warning::

	This document is a work in progress!

.. versionadded:: 0.7

OpenBlox utilizes an asynchronous, event-driven approach in almost everything
it does, from loading games to creating bricks; and this package, ``obengine.async``,
handles all the low-level asynchronous tasks.

Why would you/OpenBlox utilize an asynchronous approach instead of a true,
multi-threaded appproach? Simple:

* Since the asynchronous method doesn't *truly* run several blocks of code at the 
  same time, you don't have to worry about thread-safety
* Python code doesn't really execute at the same time (at least in the CPython
  implementation), so there's no real advantage to using a threaded approach

Tutorial
========

Enter the following into an interactive Python session:

    >>> from obengine.async import *
    >>> def task1(task):
    ...     print 'In task1!'
    ...     return task.STOP
    ...
    >>> def task2(task):
    ...     print 'In task2!'
    ...     return task.STOP
    ...
    >>> def task3(task):
    ...     print 'In task3!'
    ...     return task.STOP
    ...
    >>> sched = Scheduler()
    >>> sched.add(Task(task1, priority = 5))
    >>> sched.add(Task(task2, priority = 4))
    >>> sched.add(Task(task3, priority = 3))
    >>> sched.loop()
    In task1!
    In task2!
    In task3!

Reference
=========


.. inheritance-diagram:: obengine.async.task

.. inheritance-diagram:: obengine.async.scheduler

.. inheritance-diagram:: obengine.async.utils


.. automodule:: obengine.async.task
	:members:

.. automodule:: obengine.async.scheduler
	:members:

.. automodule:: obengine.async.utils
	:members: