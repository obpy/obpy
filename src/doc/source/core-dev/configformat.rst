=================================
The OpenBlox configuration format
=================================

.. versionadded:: 0.6

.. versionchanged:: 0.7
    Removed ``required`` and ``optional`` sections; added the following sections:
    
    * ``core``
    * ``core.gfx``
    * ``core.hardware``

History
=========

This format came into existence due to the fact that OpenBlox needed a way to let non-programmers
easily modify the performance and (to a lesser extent) the behavior of OpenBlox.

So, the OpenBlox configuration format was created, with syntax borrowed
from the familiar Windows ``.ini`` configuration format.

How the average config file looks
=================================

To give you a taste of the simplicity of the OpenBlox
configuration format (hereon referred to as "the obconf.cfg format", 
as that is the customary name for the configuration file), here is the default
configuration file that ships with OpenBlox:

   .. code-block:: ini

      [core]

      log-level = debug
      log-file = oblog.txt

      [core.gfx]

      frame-rate = 45
      show-frame-rate = yes
      use-shadows = no
      resolution = 1024x768

      [core.hardware]

      a_key = a
      b_key = s
      x_key = x
      y_key = c

You can probably understand most (if not all) of this already, without any explanation whatsoever.

Main options
=============

Logging related
---------------

``log-level``
~~~~~~~~~~~~~

This is the minimum severity (inclusive) that candidate log messages must have to actually *be* put into the log file.
Valid values are:

 * ``debug`` - Logs anything and everything. Very useful if you need to debug some tough problem,
             or are trying to find out why OpenBlox mysteriously crashes
 * ``info`` - Logs general messages. This is probably the next best option for normal users, after ``warn``.
 * ``warn`` - The default log level. This is probably the best if you're not working directly on OpenBlox's code, i.e, you just make OpenBlox games.
 * ``error`` - Logs only errors to the log file. If you want a tidy log file, this is probably best.
 * ``critical`` - Logs only critical errors (i.e, crashes) to the log file. If you observe a crash, switch the log level to ``debug``.

``log-file``
~~~~~~~~~~~~

This is the log file to write to. By default, it's ``oblog.txt``.

.. note::
   This is a filename, so make sure it's a valid filename for your OS!

If this is an absolute path (i.e, on Windows, it starts with a drive letter, like ``C:``, or on Unix [like Linux and Mac OSX], it starts with `/`), 
then the file will be written there. Otherwise, the log file will be inserted in one of 2 directories:

* ``%APPDATA%\OpenBlox\``, if you're running Windows
* ``$HOME/OpenBlox/``, if you're running Unix (Linux or Mac OSX)

Graphics-related
-----------------

``frame-rate``
~~~~~~~~~~~~~~

This is an integer that specifies the rate at which the graphics (and the physics) will be updated.
For example, if ``frame-rate`` is given a value of ``45``, than OpenBlox will refresh/update its graphics and physics 45 times a second.

.. note::

   For most computers, specifying a value over ``60`` will actually just set the frame rate to ``60``.

``use-shadows``
~~~~~~~~~~~~~~~

.. warning::

   This will seriously slow down OpenBlox if you're using an Intel graphics card,
   without actually displaying any shadows.

This option specifies whether bricks (and other 3D objects) should cast shadows.
Be warned, this can seriously slow down your frame rate if the game you're playing
has a lot of 3D models/bricks.

Valid values are:

* ``yes`` - Use shadows
* ``no`` - Don't use shadows (the default)

``show-frame-rate``
~~~~~~~~~~~~~~~~~~~

This option specifies whether the frame rate should be displayed on-screen.
If this is enabled, you'll see the frame rate in the top-right corner of your screen.

Valid values are:

* ``yes`` - Display the frame rate
* ``no`` - Don't display the frame rate

``resolution``
~~~~~~~~~~~~~~

You've probably already guessed this one. It specifies the window size and resolution.
The format for the resolution is most likely similar to what you've seen before.

The resolution on the **X** axis is the first value (on the left side
of the lowercase ``x``), and the resolution for the **Y** axis is on
the right (on the right side of the lowercase ``x``).

By default, this is ``1024x768``.

.. note::
    Be sure to pick a resolution that your graphics card can handle!

Key-related
-----------

``a_key``, ``b_key``, ``x_key``, and ``y_key``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These four options tell OpenBlox which *virtual key* [1]_ is bound to which
physical key on your keyboard.

Valid values for these options are any letter key on your keyboard.

Basic syntax
============

The ``obconf.cfg`` file format basically looks like this:

   .. code-block:: ini

      # This is a comment, to help others understand what you're doing

      [a section]

      # You can have a comment basically anywhere, because
      # anything after the pound symbol is ignored.
      # Though, this means you can't have a line that starts
      # with a comment and ends with a variable assignment, for example.
      
      # Set "variable" in "a section" to have a value of "value"
      variable = value

      [another section]

      # This doesn't change the value of "variable" in "a section"; this
      # is a completely different variable!
      # This is because it is defined in a different section ("another section")

      variable = value2

Common gotchas
==============

* Variable names *cannot* have spaces
* Section names *must not* include either ``[`` or ``]``


.. rubric:: Footnotes

.. [1] A *virtual key* is a facility OpenBlox provides
       so games can receive keyboard-like input on many different operating systems
       (including iOS and Android), without having to know which keys each gamer
       prefers to use (or if the device they're playing on has any real keys at all!)