==================
Building OpenBlox
==================

.. warning::

	This document is a work in progress!

Prerequisites
=============

**Required Knowledge**

* A basic understanding of your operating system's terminal/command prompt
* A basic understanding of your operating system's preferred method of
  software installation
* A basic understanding of how to compile C/C++ code

**Tools**

* Python 2.6 - download at http://www.python.org/download/releases/2.6.7/
* PyInstaller 1.5.1 or higher - download it at http://www.pyinstaller.org/
* Scons 1.2 or higher - download from http://scons.org/download.php
* A C compiler - either GCC (on Linux and OSX) or MinGW (on Windows) will work - get MinGW
  at http://www.mingw.org/wiki/Getting_Started
* Cython (required to build Lupa) - get it at http://cython.org or
  http://www.lfd.uci.edu/~gohlke/pythonlibs/#cython.

**Libraries**

 * Panda3D 1.8 or higher - download from http://www.panda3d.org/download.php?sdk
 * Lupa 0.18 or higher (which must be compiled with Lua 5.1 on Windows) - download Lupa
   from http://pypi.python.org/pypi/lupa, and get Lua at http://www.lua.org/download.html
 * wxPython 2.8 or higher - download at http://wxpython.org/download.php#stable

See each respective tool/library's site for installation instructions (PyInstaller and Lupa
are exceptions). Also, note each tool and library may also has its own list of
dependencies - the two lists presented here are not exhaustive; they only list
direct dependencies for OpenBlox.

Installing PyInstaller
~~~~~~~~~~~~~~~~~~~~~~

To install PyInstaller, all you have to do is extract it to the root directory of
the OpenBlox source code tree. When you finish, the root OpenBlox directory
should contain a "pyinstaller-1.x.x" directory.

.. note::

	The root OpenBlox source code directory is merely the directory that
	contains INSTALL.txt, which this document is a copy of.
	
Installing Lupa
~~~~~~~~~~~~~~~

To install Lupa on Windows, you have to perform the following steps:

* Download and extract Lupa from the link given near the top of this document
* Apply the patch ``patches\lupasetup-windows.patch`` (located inside the root
  OpenBlox source code directory) to the file ``setup.py`` located in the directory
  you extracted Lupa to.
    
.. note::

  You can use a program like Patch (http://gnuwin32.sourceforge.net/packages/patch.htm)
  to apply patches on Windows.
	
* Download Lua 5.1 using the link given near the top of this document
* Extract the Lua 5.1 archive to the same directory that you extracted Lupa to.
  Be sure the two projects remain in *separate but adjacent* directories, otherwise
  the patch won't work!
* Apply the patch ``patches\luaconf-windows.patch`` to the file ``src\luaconf.h``
  inside the directory that you extracted Lua 5.1 to
* Use the mingw32-make tool to build Lua 5.1 like so::
  
    mingw32-make
      
  Make sure that you're in the base Lua 5.1 directory before running this command!
* If the above command completed successfully, there should be a lua51.dll file in
  the ``src`` directory inside the base Lua 5.1 directory. Copy that file out into
  the base Lupa directory
* Open a command prompt inside the base Lupa directory, and run the
  command ``python setup.py build`` to build Lupa. If that command finishes successfully,
  then type ``python setup.py install`` to install Lupa
  
.. note::

  Linux users: If you have a pre-existing local installation of Lua, and you wish to use it
  instead of compiling LuaJIT2 or Lua again, apply the patch ``lupasetup-linux.patch``
  to the ``setup.py`` file in the base Lupa directory, and then pass the ``--no-luajit``
  option to ``setup.py``.

Building OpenBlox
=================

Once you've installed all the prerequisites, open up a terminal (or
command prompt on Windows), and type the following command::

	scons configure
	
You should see something similar to the following::

	scons: Reading SConscript files ...
	Checking for Python module panda3d...(cached) yes
	Checking for Python module lupa...(cached) yes
	Checking for PyInstaller...(cached) yes
	Configuration finished successfully!
	
This means OpenBlox/SCons detected all the prerequisites, and you're ready to build OpenBlox.
To build OpenBlox itself (the actual OpenBlox executable), type the following command::

	scons build
	
This step will create a ``build`` folder, with a ``bin`` folder inside.
Inside that sub-folder lie a few executables - ``obplay.exe`` and ``bloxworks.exe``
if you're on Windows, ``obplay`` and ``bloxworks`` otherwise.

.. note::

	The process of building the OpenBlox binaries can take up several hundred
	megabytes of disk space, so this is something to keep in mind if you're tight
	on hard drive space.
	
Optionally, you can also generate OpenBlox's HTML documentation with the following command::

	scons build-doc
	
You can view the generated HTML documentation by opening up the file ``index.html``
inside the ``doc`` directory (that itself lies in the ``build`` directory).
If you're viewing this file, this probably means you've built the HTML documentation already
or are viewing an already-built copy.

Starting OpenBlox
=================

Now that you've built OpenBlox, you can start it by running the executable
``obplay.exe`` (named ``obplay`` on Linux and Mac OSX) located inside the ``build/bin``
directory. OpenBlox will start up, and you can play around with the bundled games, or 
make your own with BloxWorks. Have fun!

Where to go from here
=====================

**Play a game**

You can play any of the bundled games, or find more to download at
OpenBlox's website - http://openblox.sourceforge.net.

**Make a game**

OpenBlox's game creation tool is called BloxWorks. You can start it by running the
executable ``bloxworks.exe`` (or simply ``bloxworks`` if you're on Linux or OSX)
inside the ``bin`` directory you created earlier. Refer to the generated
HTML documentation discussed earlier for more info on how to use Bloxworks.

**Read the documentation**

If you generated the HTML documentation discussed in `Building OpenBlox`, you can
view it by pointing your favorite web browser at ``build/doc/index.html`` (or
``build\doc\index.html`` on Windows).