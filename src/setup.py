__author__="alexander"
__date__ ="$Aug 4, 2010 2:56:12 PM$"

import os
import sys
import glob
import sys

try:
    from setuptools import find_packages, setup
except:

    import tkMessageBox

    tkMessageBox.showinfo('setuptools Installer', '''
    The setuptools module was not found.
    It will be installed now.

    Note that you must have administrator permissions to continue!
    ''')

    retval = None

    if os.name != 'nt':
        retval = os.system('sh tpapps/setuptools-0.6c11-py2.6.egg')

    else:
        retval = os.system('tpapps\setuptools-0.6c11.win32-py2.6.exe')

    if retval == 0:

        tkMessageBox.showinfo('setuptools Installer', '''
        The installation completed sucessfully!
        ''')

        if os.name != 'nt':
            sys.exit(os.system('python setup.py install'))

        else:
            sys.exit(os.system('C:\Python26\python.exe setup.py install'))

    else:
        tkMessageBox.showinfo('setuptools Installer', '''
        There was a problem with the installation.
        You probably did not have administrator permissions.

        Otherwise, contact the OpenBlox developers at:
        http://openblox.sourceforge.net/?q=forum for support.
        ''')

        sys.exit(1)

hdp = {'nt' : '~', 'posix' : '.'}
home = os.environ['HOME']

ob_dir = os.path.join(home, hdp[os.name] + 'openblox')
data_dir = os.path.join(ob_dir, 'data')
lua_dir = os.path.join(ob_dir, 'lualibs')

data_files = glob.glob(os.path.join('data', '*'))

def postinstall():
    
    print 'Running postinstall...'

    if os.name == 'posix':

        print 'Changing permissions for config directory(%s)' % ob_dir
        os.system('chmod -R 777 %s' % ob_dir)

setup(
  name = 'OpenBlox Game Engine',
  version = '0.1',

  packages = find_packages(),

  install_requires = ['pyttk'],
  scripts = glob.glob('tools/*.py'),

  data_files = [(data_dir, data_files), (lua_dir, '')],

  author = 'The OpenBlox Team',
  author_email = 'openblocks@users.sourceforge.net',

  description = 'Powerful yet simple 3D development framework',
  url = 'http://openblox.sourceforge.net',
  license = 'GNU GPL v3',
  long_description = """
  OpenBlox is an extremely powerful 3D game development framework, sporting such features as:

  * Scripting, via Lua
  * Plugin development, with Python
  * A simple game distribution system
  """,
)

if 'install' in sys.argv:
    postinstall()