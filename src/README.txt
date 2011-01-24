OpenBlox Game Engine Readme
---------------------------

Version 0.5 stable, revision 2

ALWAYS refer to this readme, instead of the your OpenBlox download archive's readme, as this is more up to date!

Installing on Windows
---------------------

System Requirements
-------------------

* Panda3D(Available from http://panda3d.org/download.php)
* Python 2.6(http://python.org)
* Lua 5.0 or 5.1 (http://code.google.com/p/luaforwindows/downloads/detail?name=LuaForWindows_v5.1.4-40.exe&can=2&q=)

First download and install Python 2.6.
You must then download and install Panda3D from the given link.

Now, proceed to the 'Inital Setup' section...

Installing on Linux
-------------------

System Requirements
-------------------

* Panda3D(available from http://panda3d.org/download.php)
* Python 2.6
* Lua 5.0 or 5.1
* GCC (this may already be installed on your system)

Python 2.6 should be installable from your package manager; consult its manual on how to install it.
Lua should also be installable from your package manager.
You must install your distribution's respective Panda3D package from http://panda3d.org/download.php .

Continue to the 'Inital Setup' section...

Compiling Requirements
----------------------

OpenBlox is written in Python, and therefore does not need to be compiled.
Just in case you didn't know...

Installing on Mac OSX
---------------------

System Requirements
-------------------

Python 2.6
Panda3D(available from http://panda3d.org)
Lua 5.0 or 5.1

A DMG image is for Panda3D is available from http://www.panda3d.org/download.php?platform=macosx&version=1.7.0&sdk .
Note that the OSX version of Panda3D requires the NVIDIA Cg Toolkit, which you can download at:

http://developer.download.nvidia.com/cg/Cg_3.0/Cg-3.0_July2010.dmg

Python may already be installed on your system, if not, go to http://python.org.
Get the Lua DMG from http://www.frykholm.se/files/luaframework_502.dmg and put it in your Library folder to install Lua.

Now you can proceed to the 'Inital Setup' section...

Inital Setup
-----------------

Merely run installer.py as root(or Administrator), or with administrator permissions. The installer will guide you step by step through the installation process.

If the installer says the installation finished sucessfully, you can proceed to 'Testing'... Otherwise, make an account at:

http://openblox.sourceforge.net

and post on the forums, under "Troubleshooting".

Testing
-----------------

Windows
-------

Double-click the file startlauncher.bat.

Other
-------

Double-click the file startlauncher.sh

A window should appear.
Click 'Browse...'
Select 'World.zip' from the file dialog.

Press 'Open'.
Press 'Load world'.

The OpenBlox Game Engine should start up, and the camera should be pointing at your avatar.
You can move with the following keys:

Up arrow key: Move forward
Down arrow key: Move forward
Left arrow key: Rotate left
Right arrow key: Rotate right
Space: Jump

(Note that the character can fall down at times, so either restart OpenBlox, or set your avatar upright by carefully pressing Jump)

FAQ
-----------------

The installer finished with an error!

    The most likely reason is you didn't have an internet connection.
    OpenBlox depends upon a few third-party libraries to run, besides Panda3D.

The world launcher opens, and I can select a game, but the actual game never shows up!

    You do not have Panda3D installed. See one of the above sections on how to install it.
    Note that Panda3D will be integrated into OpenBlox in a future release.

Nothing runs!

    Python isn't installed. Again, see one if the above sections on how to install it.
    In a future release, Python will(hopefully) no longer be a dependency, so you don't have to worry about this for long.
