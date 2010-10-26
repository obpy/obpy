OpenBlox Game Engine Readme
---------------------------

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

Python 2.6
Panda3D(available from http://panda3d.org)
(If you want to use the Lua utilities, download Lunatic Python from http://labix.org/download/lunatic-python/lunatic-python-1.0.tar.bz2)

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

(If you want to use the Lua utilities, download Lunatic Python from http://labix.org/download/lunatic-python/lunatic-python-1.0.tar.bz2)

A DMG installer is for Panda3D is available from http://www.panda3d.org/download.php?platform=macosx&version=1.7.0&sdk .
Note that the OSX version of Panda3D requires the NVIDIA Cg Toolkit, which you can download at:

http://developer.download.nvidia.com/cg/Cg_3.0/Cg-3.0_July2010.dmg

Python may already be installed on your system, if not, go to http://python.org .

Now you can proceed to the 'Inital Setup' section...

Inital Setup
-----------------

Create your OpenBlox configuration directory, by doing one of the following:

*   On Windows, run 'mkdir C:\Users\<your username>\~openblox'
*   On Linux and OSX, run 'mkdir /home/<your username>/.openblox'

Copy the 'data' directory (which is located where you extracted OpenBlox) to inside the OpenBlox configuration directory.

The OpenBlox configuration directory should now have a folder called 'data' inside it.

Now, proceed to the 'Testing' section...

Testing
-----------------

In the directory where you extracted OpenBlox, there should be a file called test.py; start it by either:

*   Double-clicking it
*   Starting it from the terminal/command-line by typing 'python test.py'

A window should appear, showing a demo of OpenBlox's character avatar. You can control the camera with the following controls:

*   Middle mouse button - rotating the camera
*   Right mouse button  - moves the camera backwards and forwards; in conjunction with moving the mouse itself
*   Left mouse button   - Pans the camera, in conjunction with moving the mouse

FAQ
-----------------

Help! I cannot find the OpenBlox configuration directory, although I created it!

    You must be able to view hidden files and folders; to turn this on, press Cntrl+H on Linux.

    On Windows, perform the following:

       * Select 'Tools' -> 'Folder Options'
       * Press the 'View' tab
       * Under 'Hidden Files and Folders', press 'Show hidden files and folders'
