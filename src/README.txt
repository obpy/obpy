===========================
OpenBlox Game Engine Readme
===========================

-----------------------------
For OpenBlox version 0.7 beta
-----------------------------

Installing on Windows
----------------------

NOTE: If you're using a non-final (i.e, alpha, beta, or bleeding-edge) release,
      you can safely skip ahead to the "Testing" section, if
      you've already installed OpenBlox 0.6.2. Otherwise, you
      need to install OpenBlox 0.6.2 before you can play OpenBlox 0.7

(You'll need an Internet connection to run the Windows installer.
Note that it may take around 2-5 minutes to for the installer to download the required libraries.)

Be sure to keep the default installation location (``C:\\Program Files\\OpenBlox``); otherwise, OpenBlox won't work.
Also, if a message comes up concerning "EGG caching", you can safely press "No."
If there is a dialog box comes up about "default Python installation", press "Yes."

Merely run the given Windows installer; you may be using it to view this README!
If that's the case, proceed to the "Testing" section.

Installing on Linux
-------------------

System Requirements
~~~~~~~~~~~~~~~~~~~

* Panda3D 1.7.1 or greater (1.7.2 recommended) (available from http://panda3d.org/download.php,
  currently, you must download the SDK ("Panda3D SDK for Developers"),
  not "Panda3D Runtime for End-Users").
* Python 2.6 (2.5 or 2.7 probably won't work)

Python 2.6 should be installable from your package manager; consult its manual
on how to install it.
If you're viewing this from the installer, install the above software; otherwise,
install the above software and then run the installer.

Installing on Mac OSX
---------------------

System Requirements
~~~~~~~~~~~~~~~~~~~

* Python 2.6
* Panda3D 1.7.1 or greater (1.7.2 recommended)
* wxPython (optional; install only if you want the GUI)
* LuaJIT 2 beta 4
* Lupa 0.18 or greater (0.20 recommended)

A DMG image for Panda3D is available from http://www.panda3d.org/download.php?platform=macosx&version=1.7.0&sdk .
Note that the OSX version of Panda3D requires the NVIDIA Cg Toolkit, which you can download at:

    http://developer.download.nvidia.com/cg/Cg_3.0/Cg-3.0_July2010.dmg

A wxPython DMG is downloadable at:

    http://downloads.sourceforge.net/wxpython/wxPython2.8-osx-unicode-2.8.11.0-universal-py2.6.dmg

Just run the wxPython installer inside the DMG image.

Lupa is downloadable from:

    http://pypi.python.org/packages/source/l/lupa/lupa-0.20.tar.gz#md5=a1bd4f3eef4cbcca56c3c22343acf143

..note::

    Lupa/Lua is a C application, and thus needs to be compiled. No pre-compiled
    binaries are yet availiable, otherwise this step would be unnecessary.
    If you like, email the OpenBlox administrator at openblocks@users.sourceforge.net
    with the attached OSX binaries of Lupa, so others won't have to go through this step.)

To compile Lupa:

* Download LuaJIT (at http://luajit.org/download/LuaJIT-2.0.0-beta4.tar.gz)
* Untar the LuaJIT folder inside the Lupa directory
* Open a Terminal, and change directories to the LuaJIT folder
* Type::

    make
    cd ..
    make

* Copy the ``build/lib.xxxxx-xxxx-2.6/lupa`` directory to
  the ``plugins/lupa-scripting/`` directory inside your OpenBlox download archive.


Now you can proceed to the 'Testing' section...

Testing
--------

Windows
-------

Open OpenBlox from your Start Menu (All Programs > OpenBlox > OpenBlox).
Select the test world (World).
Press "Play game."

See the "Playing" section for more information.

Linux
-------

GUI
~~~~~~

Open OpenBlox from your desktop, or applications menu (the location varies across distributions).
Select the test world (World).
Press "Play game."

See the "Playing" section for more information.

Command-line UI (if you didn't install wxPython)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Open up a terminal, and type::
    
    cd ~/OpenBlox

Next, type::

    python oblaunch.py World

See the "Playing" section for more information.

Mac OSX
-------

GUI
~~~~

Open the directory where you extracted OpenBlox.
Double-click oblaunchgui.py (If this step doesn't work, open up a terminal, change directories, and type "python oblaunchgui.py", without quotes ).
Select the test world (World).
Press "Play game."

See the "Playing" section for more information.

Command-line UI (if you didn't install wxPython)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Open up a terminal, and change directories to where you extracted OpenBlox
Next, type::

    python oblaunch.py World

See the "Playing" section for more information.

Playing
--------

You can move with the following keys:

 * Up arrow key: Move forward
 * Down arrow key: Move forward
 * Left arrow key: Rotate left
 * Right arrow key: Rotate right
 * Space: Jump

More information
----------------

OpenBlox 0.7 comes with HTML documentation, that you can browse at
build\docs\html\index.html.

Creating your own games
------------------------

Look at the built-in documentation (see the "More information" section)
for a quick example on how to use BloxWorks - OpenBlox's game editor.

The OpenBlox wiki has all the info you need to make your very own OpenBlox games.
Go to:

    http://openblox.tuxfamily.org

for more information, and a tutorial.

FAQ
----

See http://openblox.tuxfamily.org/FAQ.

Further support
---------------

The OpenBlox Wiki:

    http://openblox.tuxfamily.org

The OpenBlox Forums (always search for a solution before asking for help):

    http://openblox.sourceforge.net/forum