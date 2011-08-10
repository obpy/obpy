================
Testing OpenBlox
================

.. warning::

	This document is a work in progress!

Prerequisites:

* Scons 1.2 or higher - download from http://scons.org, or from your Linux distribution's respective package manager
* Py.Test 2.0.3 or higher - download from http://pytest.org, or from your Linux distribution's respective package manager

.. note::

   All the terminal commands in this document assume a UNIX-like terminal; the equivalent Windows command could be different.

Merely open up a terminal/command-line, change directories to where you extracted the OpenBlox source, and type:

   .. code-block:: sh
      
      scons test

This tests out the entire engine, including the documentation.
A report, similar to the following, will be printed:

   .. code-block:: sh

      scons: Reading SConscript files ...
      scons: done reading SConscript files.
      scons: Building targets ...
      py.test -q
      collected 53 items 
      .....................................................
      53 passed in 0.92 seconds
      scons: done building targets

If there's an error, it will look something like this:

   .. code-block:: sh

      scons: Reading SConscript files ...
      scons: done reading SConscript files.
      scons: Building targets ...
      py.test -q
      collected 53 items 
      ........................F............................
      =================================================================================== FAILURES ====================================================================================
      ___________________________________________________________________________________ [doctest] ___________________________________________________________________________________
      522                   or `AmbiguousNameException` if multiple children of this node are named *name*
      523 
      524         Example:
      525 
      526             >>> sg = SceneGraph()
      527             >>> n1 = SceneNode('Node 1')
      528             >>> n2 = SceneNode('Node 2')
      529             >>> sg.add_node(n1)
      530             >>> n2.parent = n1
      531             >>> print n1.get_child_by_name('Node 2').name
      Expected:
         Node 3
      Got:
         Node 2

      <some path>/obengine/scenegraph.py:531: DocTestFailure
      1 failed, 52 passed in 0.89 seconds
      scons: *** [py.test] Error 1
      scons: building terminated because of errors.

That means a unit test (specifically, in `obengine.scenegraph`) didn't pass. If this occurs when you try to build OpenBlox, won't you please attempt to fix it? :)
