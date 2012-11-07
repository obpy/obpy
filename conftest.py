
# conftest.py - Simple Py.Test plugin to allow running of 
# Sphinx-embedded doctests (and doctests inside OpenBlox plugins)
# from Py.Test


import os
import fnmatch


collect_ignore = fnmatch.filter(os.listdir(os.curdir), 'pyinstaller-1.[56].[012]')


def pytest_configure(config):

    import sys
    import os

    # Since Py.Test is run from the root OpenBlox directory,
    # and since the obengine Python package (that contains
    # all the OpenBlox code) is also there, we just add
    # the "current directory", i.e, the directory Py.Test
    # was started from.

    sys.path.append(os.path.abspath(os.curdir))

