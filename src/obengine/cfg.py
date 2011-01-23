"""
Copyright (C) 2010 The OpenBlox Project

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
__date__ ="$Aug 3, 2010 2:36:03 PM$"

import os
import sys

import ConfigParser

import tkMessageBox

import obengine.utils

config_vars = {}

def init():

    global config_vars

    obengine.utils.info('Initializing configuration subsystem')

    basedir = os.getenv('OPENBLOX_DIR')

    if basedir == None:

        obengine.utils.info('Couldn\'t find environment variable, looking inside %s' % os.getenv('HOME'))

        if os.name == 'nt':

            obengine.utils.info('On a Windows system, hidden directory character is ~')

            if os.getenv('HOME') != None:
                basedir = os.getenv('HOME') + '\\~openblox\\'

            else:
                basedir = os.getenv('HOMEPATH') + '\\~openblox\\'

            if basedir == None:

                obengine.utils.critical('Couldn\'nt find configuration directory!')

                tkMessageBox.showerror('OGE Configuration', """
                Could not find OpenBlox Game Engine configuration directory!
                """)
                sys.exit(1)

        elif os.name == 'posix':

            obengine.utils.info('On a POSIX system, hidden directory character is .')

            basedir = os.getenv('HOME') + '/.openblox/'

            if basedir == None:

                obengine.utils.critical('Couldn\'nt find configuration directory!')

                tkMessageBox.showerror('OGE Configuration', """
                Could not find OpenBlox Game Engine configuration directory!
                """)

                sys.exit(1)

    if not os.path.exists(basedir):

        obengine.utils.critical('The configuration directory doesn\'t exist!')

        tkMessageBox.showerror('OGE Configuration', """
                Could not find OpenBlox Game Engine configuration directory!
                This could be because of an improper OpenBlox installation.
                Try installing OpenBlox again. If you have further problems, go to:

                http://openblox.sf.net

                and register for an account, and then post in the forums, under "Game Engine Troubleshooting."
                """)

        sys.exit(1)

    cfgparser = ConfigParser.SafeConfigParser(
    {
    'loglevel' : 'debug',
    'logfile' : 'oblog.txt',
    'viewmode' : 'third-person'
    }
    )

    lualibdir = os.path.join(basedir, 'lualibs')
    datadir = os.path.join(basedir, 'data')

    obengine.utils.info('Reading configuration variables...')

    cfgparser.read(os.path.join(basedir, 'obconf.cfg'))

    add_config_var('cfgdir', basedir)
    add_config_var('lualibdir', lualibdir)
    add_config_var('datadir', datadir)
    add_config_var('loglevel', cfgparser.get('required', 'loglevel'))
    add_config_var('logfile', cfgparser.get('required', 'logfile'))
    add_config_var('fps', cfgparser.getint('required', 'fps'))

    add_config_var('viewmode', cfgparser.get('optional', 'viewmode'))

    if cfgparser.has_section('optional'):

        for key, value in cfgparser.items('optional'):
            add_config_var(key, value)

    obengine.utils.info('Configuration subsystem initialization finished!')

def add_config_var(key, value):

    global config_vars
    
    config_vars[key] = value

def get_config_var(key):

    global config_vars

    return config_vars[key]

def __getattr__(key):

    global config_vars

    if key in config_vars:

        raise DeprecationWarning, 'Attribute configuration variables is slated for removal\na later OpenBlox version'
        return key

    elif key in globals():

        return globals()[key]

    raise AttributeError, key