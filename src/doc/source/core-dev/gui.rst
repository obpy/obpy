========================
The OpenBlox GUI toolkit
========================

.. module:: obengine.gui
.. versionadded:: 0.7

Design overview
===============

Keeping in line with OpenBlox's OS/API-independence spirit, OpenBlox's GUI toolkit
doesn't depend upon any one GUI library. So, it is a little more complex
than most GUI toolkits (at least at the architecture level), but it pays off
in the long run, as OpenBlox's GUI system works independent of any rendering
code, plus, it can even be used on a system that has no screen (like a server),
*yet all your GUI code still works*.

This is easily accomplished by splitting the GUI toolkit code into 3 distinct layers:

 * Logic layer
 * Rendering layer
 * Logic + rendering glue layer

The OS/API-independence is promoted even further by sticking the rendering code
into an OpenBlox plugin, so the rendering code isn't even contained within OpenBlox itself.

Here's the general architecture for OpenBlox's GUI toolkit::

    -----------------
    | OpenBlox core |
    ---------------------------------
    |                               |
    |   -------------------------   |
    |   |                       |   |
    |   |  Widget logic layer   |   |
    |   |_______________________|   |
    |            /|\                |
    |             |                 |          End User
    |             |                 |          ________
    |             |                 |         /        \
    |   -------------------------   |         |        |
    |   |                       |   |     \   |        |  /
    |   | Widget logic/graphic  |   |      \  \________/ /
    |   | bindings              |<--|------ \     |     /
    |   |_______________________|   |        \-===|===-/
    |             |                 |             |
    |_____________|_________________|             |
                  |                              / \
                  |                             /   \
                 \|/                           /     \
    -----------------------------
    | core.gui (virtual plugin) |
    --------------------------------
    |                              |
    |______________________________|
                 /|\
                  |
    --------------|------------------
    | OpenBlox GUI|rendering plugin |
    --------------|----------------------
    |             |                     |
    |   -------------------------       |
    |   |                       |       |
    |   | Widget rendering code |       |
    |   |_______________________|       |
    |                                   |
    |___________________________________|


An example
==========

Here's a quick example to vertically align 3 buttons (using a container) automatically::

    >>> from obengine.gui import *
    >>> from obengine.math import Vector2D

    >>> factory = WidgetFactory()
    >>> container = factory.make('container', position = Vector2D(30, 30), margin = 0.5)
    >>> button1 = factory.make('button', 'Button 1')
    >>> button2 = factory.make('button', 'Button 2')
    >>> button3 = factory.make('button', 'Button 3')

    >>> container.add(button1)
    >>> container.add(button2)
    >>> container.add(button3)

    >>> print 'button1.position:', button1.position
    button1.position: Vector2D(30.0, 29.0)
    >>> print 'button2.position:', button2.position
    button2.position: Vector2D(30.0, 30.0)
    >>> print 'button3.position:', button3.position
    button3.position: Vector2D(30.0, 31.25)

As you can see, the average **Y**-position of each of the three buttons
is still at the container's center ``(30, 30)``.

.. note::

    The average **Y**-position of the widgets in
    the container is *actually*  about ``(30, 30.1)``. This is due to
    floating-point errors in the partitioning algorithm.

The coordinate system
=====================

OpenBlox's GUI toolkit's coordinate system is straight forward: The center of
the screen is at ``(0, 0)``, and the drawable area on the screen ranges
from ``(-100, 100)`` to ``(100, -100)``. Most (if not all) GUI toolkits
have their origin in the upper-left corner of the screen, whereas with OpenBlox,
the screen operates like a normal Cartiesian graph, with the origin in the center.

