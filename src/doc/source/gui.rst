========================
The OpenBlox GUI toolkit
========================

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

Here is the general architecture for OpenBlox's GUI toolkit::

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
    ----------------------------
    | core.gui (virtual plugin |
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


Using OpenBlox's GUI
====================

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
    >>> print 'button1.position:', button1.position.x, button1.position.y
    button1.position: 30.0 30.0
    >>> print 'button2.position:', button2.position.x, button2.position.y
    button2.position: 30.0 30.5

As you can see, the container's center is still at ``(30, 30)``,