OpenBlox Game Engine Readme
---------------------------

Version 0.5 stable

Installing on Windows
---------------------

System Requirements
-------------------

Panda3D(Available from http://panda3d.org/download.php)
Python 2.6(http://python.org)

First download and install Python 2.6.
You must then download and install Panda3D from the given link.

Now, proceed to the 'Inital Setup' section...

Installing on Linux
-------------------

System Requirements
-------------------

Panda3D(available from http://panda3d.org/download.php)
Python 2.6

Python 2.6 should be installable from your package manager; consult its manual on how to install it.
You must install your distribution's respective package from http://panda3d.org/download.php .

Continue to the 'Inital Setup' section...

Compiling Requirements
----------------------

OpenBlox is written in Python, and therefore does not need to be compiled.

Installing on Mac OSX
---------------------

System Requirements
-------------------

Python 2.6
Panda3D(available from http://panda3d.org)

A DMG image is for Panda3D is available from http://www.panda3d.org/download.php?platform=macosx&version=1.7.0&sdk .
Note that the OSX version of Panda3D requires the NVIDIA Cg Toolkit, which you can download at:

http://developer.download.nvidia.com/cg/Cg_3.0/Cg-3.0_July2010.dmg

Python may already be installed on your system, if not, go to http://python.org .

Now you can proceed to the 'Inital Setup' section...

Inital Setup
-----------------

Merely run installer.py as root(or Administrator). The installer will guide you step by step through the installation process.

If the installer says the installation finished sucessfully, you can proceed to 'Testing'...

Testing
-----------------

Start the world launcher by running launchworldgui.py. A window should appear.
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

FAQ
-----------------

The installer finished with an error!

    The most likely reason is you didn't have an internet connection.
    OpenBlox depends upon a few third-party libraries to run.

The world launcher opens, and I can select a game, but the actual game never shows up!

    You do not have Panda3D installed. See one of the above sections on how to install it.

Nothing runs!

    Python isn't installed. Again, see one if the above sections on how to install it.