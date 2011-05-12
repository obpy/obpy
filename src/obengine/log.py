# To change this template, choose Tools | Templates
# and open the template in the editor.
"""
Copyright (C) 2011 The OpenBlox Project

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
__date__ ="$May 4, 2011 7:09:12 PM$"

import sys
import os

from sys import _getframe as getframe

import time
import logging

import obengine.cfg
import obengine.depman
obengine.depman.gendeps()

loglevels = { 'debug' : logging.DEBUG,
                'info' : logging.INFO,
                'warning' : logging.WARNING,
                'error' : logging.ERROR,
                'critical' : logging.CRITICAL}

def init():

    level = obengine.cfg.get_config_var('log-level')
    logfile = obengine.cfg.get_config_var('log-file')

    # Writing to C:\Program Files is deprecated
    if sys.platform == 'win32':
        fileloc = os.path.join(os.getenv('APPDATA'), 'OpenBlox', logfile)

    else:
        fileloc = os.path.join(obengine.cfg.get_config_var('cfgdir'), logfile)

    logging.basicConfig(level = loglevels.get(level, logging.NOTSET), filename = fileloc)

def debug(string):
    logging.getLogger(_get_calling_package()).debug(time.ctime() + ': ' + string)

def info(string):
    logging.getLogger(_get_calling_package()).info(time.ctime() + ': ' + string)

def warn(string):
    logging.getLogger(_get_calling_package()).warn(time.ctime() + ': ' + string)

def error(string):
    logging.getLogger(_get_calling_package()).error(time.ctime() + ': ' + string)

def critical(string):
    logging.getLogger(_get_calling_package()).critical(time.ctime() + ': ' + string)

def _get_calling_package():
    return getframe(2).f_globals.get('__name__', 'root')