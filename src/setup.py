__author__="alexander"
__date__ ="$Aug 4, 2010 2:56:12 PM$"

from setuptools import setup, find_packages

setup (
  name = 'OpenBlox Game Engine',
  version = '0.1',

  packages = find_packages(),

  install_requires=[],

  author = 'The OpenBlox Team',
  author_email = 'openblocks@users.sourceforge.net',

  summary = 'Powerful yet simple 3D development framework',
  url = 'http://openblox.sourceforge.net',
  license = 'GNU GPL v3',
  long_description = """
  OpenBlox is an extremely powerful 3D game development framework, sporting such features as:

  * Scripting, via Lua
  * Plugin development, with Python
  * A complete RAD environment
  * A simple game distribution system
  * Networking, so multiple people can play your game at a time
  """,
)