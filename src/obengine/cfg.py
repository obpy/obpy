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


config_vars = {}

def init():

    global config_vars

    defaults = {'loglevel' : 'debug', 'logfile' : 'oblog.txt', 'viewmode' : 'third-person', 'fps' : 50.0, 'physxfps' : 45.0}

    basedir = __file__[:len(__file__) - len(os.path.join('obengine', 'cfg.py')) - 1]

    cfgparser = ConfigParser.ConfigParser()

    lualibdir = os.path.join(basedir, 'lualibs')
    datadir = os.path.join(basedir, 'data')

    cfgparser.read(os.path.join(basedir, 'obconf.cfg'))

    add_config_var('cfgdir', basedir)
    add_config_var('lualibdir', lualibdir)
    add_config_var('datadir', datadir)
    add_config_var('loglevel', cfgparser.has_section('optional') and cfgparser.get('optional', 'loglevel') or defaults['loglevel'])
    add_config_var('logfile', cfgparser.has_section('optional') and cfgparser.get('optional', 'logfile') or defaults['logfile'])
    add_config_var('viewmode', cfgparser.has_section('optional') and cfgparser.get('optional', 'viewmode') or defaults['viewmode'])

    add_config_var('fps', cfgparser.has_section('required') and cfgparser.getfloat('required', 'fps') or (defaults['fps']))
    add_config_var('physxfps', cfgparser.has_section('required') and cfgparser.getfloat('required', 'physxfps') or defaults['physxfps'])

    if cfgparser.has_section('optional'):

        for key, value in cfgparser.items('optional'):
            add_config_var(key, value)

def add_config_var(key, value):

    global config_vars
    
    config_vars[key] = value

def get_config_var(key):

    global config_vars

    return config_vars[key]