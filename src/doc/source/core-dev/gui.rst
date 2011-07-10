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

See *examples/api/gfxgui.py* for a complete example.

The coordinate system
=====================

OpenBlox's GUI toolkit's coordinate system is straight forward: The center of
the screen is at ``(0, 0)``, and the drawable area on the screen ranges
from ``(-100, 100)`` to ``(100, -100)``. Most (if not all) GUI toolkits
have their origin in the upper-left corner of the screen, whereas with OpenBlox,
the screen operates like a normal Cartiesian graph, with the origin in the center.

