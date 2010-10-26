__author__="openblocks"
__date__ ="$Jul 12, 2010 7:59:47 PM$"

import cfg
import os

# This isn't normally set, but it saves a lot of time...

cfgdir = os.getenv("OPENBLOX_DIR")

print 'OpenBlox Game Engine(OGE) initalizing...'

# Is the environment variable set?

if cfgdir:

    print '[STARTUP] Found OpenBlox environment variable...'

    cfg.cfgdir = cfgdir

# I guess not, so let's look manually...

else:

    print '[STARTUP] Couldn\'t find environment variable, searching for config directory...'

    cfgdir = os.getenv('HOME')

    # Note that Windows also has a HOME environment variable

    if cfgdir:

        # Unfortunately, Python doesn't have an hidden file/directory
        # equivalent to os.sep, so we check the OS type here

        if os.name == 'nt':

            print '[STARTUP] On a Windows NT system, searching for config directory inside', cfgdir, '...'

            if os.path.exists(cfgdir + os.sep + '~openblox'):

                print '[STARTUP] Found config directory(', cfgdir + os.sep + '~openblox )!'

                cfg.cfgdir = cfgdir
                os.putenv('OPENBLOX_DIR', cfgdir + os.sep + '~openblox')

            else:

                print '[STARTUP] Config directory doesn\'t exist, creating...'

                os.mkdir(cfgdir + os.sep + '~openblox')

                cfg.cfgdir = cfgdir + os.sep + '~openblox'
                os.putenv('OPENBLOX_DIR', cfgdir + os.sep + '~openblox')

        # Thank goodness most other non-Windows OSes are the same, or we would be in
        # for a ton of hard work!

        else:

            print '[STARTUP] On a Unix-like system, searching for config directory inside', cfgdir, '...'

            if os.path.exists(cfgdir + os.sep + '.openblox'):

                print '[STARTUP] Found config directory(', cfgdir + os.sep + '.openblox )'

                cfg.cfgdir = cfgdir + os.sep + '.openblox'
                os.putenv("OPENBLOX_DIR", cfgdir + os.sep + '.openblox')

            else:

                print '[STARTUP] Config directory doesn\'t exist, creating...'

                os.mkdir(cfgdir + os.sep + '.openblox')
                
                cfg.cfgdir = cfgdir + os.sep + '.openblox'
                os.putenv('OPENBLOX_DIR', cfgdir + os.sep + '.openblox')
                
    else:
        
        raise RuntimeError('Couldn\'t find configuration directory!')
        import sys
        sys.exit(1)

lualibdir = cfg.cfgdir + os.sep + 'lualibs'

if os.path.exists(lualibdir):

    print '[STARTUP] Found Lua library directory(', lualibdir, ')'

    cfg.lualibdir = lualibdir

else:

    print '[STARTUP][WARNING] Couldn\'t find the Lua library directory, creating...'
    os.mkdir(lualibdir)

# I didn't want to make my own parser(we humans are quite lazy!) so I used the standard ConfigParser parser

import ConfigParser

cfgparser = ConfigParser.ConfigParser()

# Does a configuration file already exist?

if not os.path.exists(cfg.cfgdir + os.sep + 'obconf.cfg'):

    # Guess not, so make one that most users will want
    
    print '[STARTUP] Couldn\'t find config file, creating a default one...'

    cfgfile = open(cfg.cfgdir + os.sep + 'obconf.cfg', 'w')

    cfgparser.add_section('required')

    cfgparser.set('required', 'fps', '30')
    cfgparser.set('required', 'servermode', 'no')

    cfgparser.add_section('optional')

    cfgparser.set('optional', 'viewmode', 'third-person')

    cfgparser.write(cfgfile)
    cfgfile.close()

print '[STARTUP] Reading config file...'

cfgparser.read(cfg.cfgdir + os.sep + 'obconf.cfg')

try:

    setattr(cfg, 'servermode', cfgparser.getboolean('required', 'servermode'))
    setattr(cfg, 'fps', cfgparser.getint('required', 'fps'))
    setattr(cfg, 'viewmode', cfgparser.get('optional', 'viewmode'))

except ConfigParser.ParsingError as error:
    
    raise RuntimeError('Bad configuration file:\n' + error.message)
    import sys
    sys.exit(1)

print '[STARTUP] Read config file sucessfully!'

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