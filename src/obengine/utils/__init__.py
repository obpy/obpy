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
__author__="alexander"
__date__ ="$Sep 28, 2010 1:35:13 PM$"

import logging
import os
import sys
import time

import obengine.cfg

loglevels = { 'debug' : logging.DEBUG,
                'info' : logging.INFO,
                'warning' : logging.WARNING,
                'error' : logging.ERROR,
                'critical' : logging.CRITICAL}

def init():

    level = obengine.cfg.get_config_var('loglevel')
    logfile = obengine.cfg.get_config_var('logfile')
    
    logging.basicConfig(level = loglevels.get(level, logging.NOTSET), filename = os.path.join(obengine.cfg.get_config_var('cfgdir'), logfile))

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
            method(*args, **kwargs)

        finally:
            after(*args, **kwargs)

    

    return wrapper