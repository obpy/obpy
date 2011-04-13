:: Windows launcher for OpenBlox - it does nothing special,
:: just start oblaunchgui.py.
:: The only thing that relieves the user of any work is the need to call
:: ppython.exe, which is Panda3D's special version of Python on Windows.
:: Other than that, nothing tricky is done.

@ECHO off
ppython.exe oblaunchgui.py
@ECHO on