===============================================
OpenBlox's event system (:mod:`obengine.event`)
===============================================

.. module:: obengine.event
.. versionadded:: 0.7

OpenBlox's event system forms OpenBlox's backbone, along with OpenBlox's
`plugin system </core-dev/pluginsystem>` and `asynchronous system </core-dev/asyncsystem>`.

Some examples of OpenBlox modules that use the event system are:

    * `obengine.gui` (the OpenBlox GUI)
    * `obengine.plugin` (the OpenBlox plugin system)

Here's a quick example on how to make your own event:

    >>> import obengine.event
    >>> e = obengine.event.Event()
    >>> def test_handler():
    ...     print 'Test handler fired!'
    ...
    >>> e += test_handler
    >>> e()
    Test handler fired!

You can also remove bound event handlers:

    >>> e -= test_handler
    >>> e()

Let's define a handler that takes some arguments:

    >>> def second_test_handler(arg1, arg2):
    ...     print arg1, arg2
    ...
    >>> e += second_test_handler
    >>> e('Hello,', 'World!')
    Hello, World!



Reference
=========

.. class:: Event()

    .. method:: fire([*args, **kwargs])

        Fires this event, and calls all bound event handlers in the order
        they were added (i.e, in a FIFO fashion), passing any given arguments
        to each event handler.

        .. warning::

            If any of the event handlers throw an exception, subsequent event handlers
            (i.e, those that haven't been fired yet) won't get called.

    .. method:: add_handler(handler)

        Adds *handler* to the list of event handlers bound to this event.
        Nothing is done if *handler* is already bound to this event.

        :param handler: The handler to add
        :type handler: any callable object

    .. method:: remove_handler(handler)

        Removes *handler* from the list of event handlers bound to this event.

        :param handler: The handler to remove
        :raises: `ValueError` if the handler isn't already handling this event.

    .. method:: enable()

        Enables this event, if it wasn't already enabled.

    .. method:: disable()

        Disables this event (so calls to :meth:`fire` or :meth:`__call__` do
        nothing).

    .. attribute:: enabled

        A `bool`, which enables (if set to `True`) or disables (if set to `False`)
        this event.

        The reason this attribute exists (when :meth:`enable` and :meth:`disable` exist)
        is to enable users to easily select the enabling/disabling system that
        works best for them (:meth:`enable`/:meth:`disable` for
        event handlers, this attribute otherwise).

    .. method:: handler_count()

        Returns the number of handlers currently bound to this event.

    .. method:: __iadd__(handler)

        See :meth:`add_handler`.

    .. method:: __isub__(handler)

        See :meth:`remove_handler`.

    .. method:: __call__([*args, **kwargs])

        See :meth:`fire`.

    .. method:: __len__()

        See :meth:`handler_count`.