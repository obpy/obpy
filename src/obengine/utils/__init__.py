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
__date__ ="$Sep 28, 2010 1:35:13 PM$"

import logging
import os
import sys
import time
import types

import obengine.cfg
import obengine.event

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

def info(string):
    logging.info(time.ctime() + ': ' + string)

def warn(string):
    logging.warn(time.ctime() + ': ' + string)

def error(string):
    logging.error(time.ctime() + ': ' + string)

def critical(string):
    logging.critical(time.ctime() + ': ' + string)

def wrap_callable(method, before, after):

    def wrapper(*args, **kwargs):

        before(*args, **kwargs)

        try:
            return method(*args, **kwargs)

        finally:
            after(*args, **kwargs)

    wrapper.__name__ = method.__name__

    return wrapper

class Borg:
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state