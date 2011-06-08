==================
Building OpenBlox
==================

.. note::
   Building OpenBlox from source requires a certain amount
   of technical expertise. Specifically, it requires basic knowledge of:

   * Your operating system's command line
   * Your operating system's method of program installation
   * If things go wrong, some knowledge of Python

Bottom-line prerequisites:

* Python - download from http://python.org
* SCons - download from http://scons.org

Before you run any of the below steps, you must first install the above software. Next, using your operating system's command line/shell, change directories to where you extracted the OpenBlox source code.

Now, to make sure you've installed all the above software, execute these commands (in your command line/shell):

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

Building OpenBlox's documentation
=================================

Building OpenBlox's distributable packages
==========================================
