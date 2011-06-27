=====================================================
OpenBlox's asynchronous system (``obengine.async``)
=====================================================

.. module:: obengine.async
.. versionadded:: 0.7

OpenBlox utilizes an asynchronous, event-driven approach in almost everything
it does, from loading games to creating bricks; and this package, ``obengine.async``,
handles all the low-level asynchronous tasks.

Tutorial
========

Enter the following into your interactive Python session:

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