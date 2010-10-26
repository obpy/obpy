"""
This file is part of The OpenBlox Game Engine.

    The OpenBlox Game Engine is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    The OpenBlox Game Engine is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with The OpenBlox Game Engine.  If not, see <http://www.gnu.org/licenses/>.

"""
__author__="openblocks"
__date__ ="$Jul 12, 2010 7:59:47 PM$"

import cfg
import os
import utils

# This isn't normally set, but it saves a lot of time...

cfgdir = os.getenv("OPENBLOX_DIR")

utils.info('OpenBlox Game Engine(OGE) initalizing...')

# Is the environment variable set?

if cfgdir:

    utils.info('Found OpenBlox environment variable...')

    cfg.cfgdir = cfgdir

# I guess not, so let's look manually...

else:

    utils.warn('Couldn\'t find environment variable, searching for config directory...')

    cfgdir = os.getenv('HOME')

    # Note that Windows also has a HOME environment variable

    if cfgdir:

        # Unfortunately, Python doesn't have an hidden file/directory
        # equivalent to os.sep, so we check the OS type here

        if os.name == 'nt':

            utils.info('On a Windows NT system, searching for config directory inside ' + cfgdir + ' ...')

            if os.path.exists(cfgdir + os.sep + '~openblox'):

                utils.info('Found config directory( ' + cfgdir + os.sep + '~openblox )!')

                cfg.cfgdir = cfgdir
                os.putenv('OPENBLOX_DIR', cfgdir + os.sep + '~openblox')

            else:

                utils.warn('Config directory doesn\'t exist, creating...')

                os.mkdir(cfgdir + os.sep + '~openblox')

                cfg.cfgdir = cfgdir + os.sep + '~openblox'
                os.putenv('OPENBLOX_DIR', cfgdir + os.sep + '~openblox')

        # Thank goodness most other non-Windows OSes are the same, or we would be in
        # for a ton of hard work!

        else:

            utils.info('On a Unix-like system, searching for config directory inside ' + cfgdir + ' ...')

            if os.path.exists(cfgdir + os.sep + '.openblox'):

                utils.info('Found config directory( '+ cfgdir + os.sep + '.openblox )')

                cfg.cfgdir = cfgdir + os.sep + '.openblox'
                os.putenv("OPENBLOX_DIR", cfgdir + os.sep + '.openblox')

            else:

                utils.warn('Config directory doesn\'t exist, creating...')

                os.mkdir(cfgdir + os.sep + '.openblox')
                
                cfg.cfgdir = cfgdir + os.sep + '.openblox'
                os.putenv('OPENBLOX_DIR', cfgdir + os.sep + '.openblox')
                
    else:

        utils.critical('Couldn\'t find configuration directory!')
        raise RuntimeError('Couldn\'t find configuration directory!')
        import sys
        sys.exit(1)

lualibdir = cfg.cfgdir + os.sep + 'lualibs'

if os.path.exists(lualibdir):

    utils.info('Found Lua library directory( ' + lualibdir +' )')

    cfg.lualibdir = lualibdir

else:

    utils.warn('Couldn\'t find the Lua library directory, creating...')
    os.mkdir(lualibdir)

# I didn't want to make my own parser(we humans are quite lazy!) so I used the standard ConfigParser parser

import ConfigParser

cfgparser = ConfigParser.ConfigParser(defaults = {'verbose' : 'yes'})

# Does a configuration file already exist?

if not os.path.exists(cfg.cfgdir + os.sep + 'obconf.cfg'):

    # Guess not, so make one that most users will want
    
    utils.warn('Couldn\'t find config file, creating a default one...')

    cfgfile = open(cfg.cfgdir + os.sep + 'obconf.cfg', 'w')

    cfgparser.add_section('required')

    cfgparser.set('required', 'fps', '30')
    cfgparser.set('required', 'servermode', 'no')

    cfgparser.add_section('optional')

    cfgparser.set('optional', 'viewmode', 'third-person')
    cfgparser.set('optional', 'verbose', 'yes')

    cfgparser.write(cfgfile)
    cfgfile.close()

utils.info('Reading config file...')

cfgparser.read(cfg.cfgdir + os.sep + 'obconf.cfg')

try:

    setattr(cfg, 'servermode', cfgparser.getboolean('required', 'servermode'))
    setattr(cfg, 'fps', cfgparser.getint('required', 'fps'))
    setattr(cfg, 'viewmode', cfgparser.get('optional', 'viewmode'))
    setattr(cfg, 'verbose', cfgparser.getboolean('optional', 'verbose'))


except ConfigParser.ParsingError as error:

    utils.critical('Bad configuration file:\n' + error.message)
    raise RuntimeError('Bad configuration file:\n' + error.message)
    import sys
    sys.exit(1)

utils.info('Read config file sucessfully!')

# Servers don't usally have monitors(doh), so if we're operating as a server, don't load graphics

if not cfg.servermode:

    import obengine.gfx

# Everything loaded fine, so import everything most people need

try:

    # Some people don't want to use Lua, or don't have Lunatic Python installed, so check here

    import luaengine as lua
    import luautils
    
except: pass

from player import *
from world import *
from element import *