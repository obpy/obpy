__author__="alexander"
__date__ ="$Aug 4, 2010 2:56:12 PM$"

import os
import glob

from setuptools import setup, find_packages

hdp = {'nt' : '~', 'posix' : '.'}
home = os.environ['HOME']

ob_dir = os.path.join(home, hdp[os.name] + 'openblox')
data_dir = os.path.join(ob_dir, 'data')
lua_dir = os.path.join(ob_dir, 'lualibs')

data_files = glob.glob(os.path.join('data', '*'))

setup (
  name = 'OpenBlox Game Engine',
  version = '0.1',

  packages = find_packages(),

  install_requires = ['pyttk', 'lupa'],

  data_files = [(data_dir, data_files), (lua_dir, '')],

  author = 'The OpenBlox Team',
  author_email = 'openblocks@users.sourceforge.net',

  summary = 'Powerful yet simple 3D development framework',
  url = 'http://openblox.sourceforge.net',
  license = 'GNU GPL v3',
  long_description = """
  OpenBlox is an extremely powerful 3D game development framework, sporting such features as:

  * Scripting, via Lua
  * Plugin development, with Python
  * A simple game distribution system
  """,
)