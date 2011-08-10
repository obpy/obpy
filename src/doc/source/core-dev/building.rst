==================
Building OpenBlox
==================

.. warning::

	This document is a work in progress!

.. note::
   Building OpenBlox from source requires a certain amount
   of technical expertise. Specifically, it requires basic knowledge of:

   * Your operating system's command line
   * Your operating system's method of program installation
   * If things go wrong, possibly some knowledge of Python

.. note::
    All the commands given in this page assume use of a
    UNIX-like terminal (i.e, Linux, Mac OSX). Windows commands could be slightly
    different.

**Bottom-line prerequisites**:

* Python 2.6 - download from http://python.org
* SCons (any version should work) - download from http://scons.org

Yes, you read that correctly. OpenBlox's core only depends upon Python itself!
However, to get some of the basic functionality (like 3D rendering, sound, physics,
and Lua scripting), you might need to install one of the below libraries.

**Optional requirements**:

* Panda3D 1.7.1 or higher - 1.7.2 recommended (required for 3D rendering,
  audio, and physics) - download from http://www.panda3d.org/download.php?sdk
* Lupa 0.18 or higher - 0.20 recommended (Mac OSX only,
  required for Lua scripting) - download from http://pypi.python.org/pypi/lupa

.. note::

    Running ``scons configure`` in the directory you extracted the OpenBlox
    source code to will check that you have the Panda3D libraries installed.

Before you run any of the below steps, you must first install the above software.
Next, using your operating system's command line/shell, change directories to
where you extracted the OpenBlox source code.

Now, to make sure you've installed all the above software,
execute these commands (in your command line/shell):

.. code-block:: sh

   python --version
   scons -v

The first command should output something similar to the following:

.. code-block:: sh

   Python 2.6.5

The second, something like this:

.. code-block:: sh

   SCons by Steven Knight et al.:
	script: v1.2.0.d20100117.r4629, 2010/01/17 22:23:21, by scons on scons-dev
	engine: v1.2.0.d20100117.r4629, 2010/01/17 22:23:21, by scons on scons-dev
   Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010 The SCons Foundation

Building OpenBlox itself
========================

To build OpenBlox's runtime (i.e, just the code, no plugins), type:

.. code-block:: sh

    ./build-helpers/remove_pycs.py
    scons runtime

The first command removes any ``.pyc`` files, the second actually builds the
OpenBlox runtime. The runtime should now be located in ``build/obruntime.zip``.
The runtime is not normally used directly (unless your game is/will be written in Python),
instead, use the OBFreeze tool to turn a normal Lua/XML OpenBlox game to an executable.

Building OpenBlox's documentation
=================================

To build OpenBlox's documentation, type:

.. code-block:: sh

    scons docs

This command could take a while to complete, if the documentation is being built
from scratch (i.e, if this is the first time you've ran this command, or you've
just removed all built files with ``scons -c``).

Building OpenBlox's distributable packages
==========================================

TODO