#
# This module provides logging facilites to other OpenBlox packages/modules (al-
# though you can certainly use it for your own purposes).
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
#
#
# Copyright (C) 2011 The OpenBlox Project
#
# This file is part of The OpenBlox Game Engine.
#
#     The OpenBlox Game Engine is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     The OpenBlox Game Engine is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with The OpenBlox Game Engine.  If not, see <http://www.gnu.org/licenses/>.
#


__author__ = "openblocks"
__date__ = "$May 4, 2011 7:09:12 PM$"


import sys
import os
from sys import _getframe as getframe
import logging
import datetime

import obengine.cfg
import obengine.datatypes
import obengine.depman

obengine.depman.gendeps()


def init():
    if hasattr(Logger, '_level') is False:
        Logger().autoconfig()


class Logger(obengine.datatypes.Borg):

    log_levels = {
    'debug' : logging.DEBUG,
    'info' : logging.INFO,
    'warning' : logging.WARNING,
    'error' : logging.ERROR,
    'critical' : logging.CRITICAL,
    'dontcare' : logging.NOTSET
    }

    format_str = '%(levelname)s:%(name)s:%(asctime)s: %(message)s'

    def __init__(self):
        self.config_src = obengine.cfg.Config()

    def autoconfig(self):

        log_level = self.config_src.get_str('log-level')
        log_file = self.config_src.get_str('log-file')

        if sys.platform == 'win32':
            default_dir = os.path.join(os.getenv('APPDATA'), 'OpenBlox')

        else:
            default_dir = self.config_src.get_str('cfgdir')

        if os.path.isabs(log_file) is False:
            log_file = os.path.join(default_dir, log_file)

        self.config(log_level, log_file)

    def config(self, log_level, log_file):

        formatter = logging.Formatter(self.format_str)

        self._level = self.log_levels[log_level]
        self._file = log_file

        self._handler = logging.FileHandler(log_file)
        self._handler.setLevel(self._level)
        self._handler.setFormatter(formatter)

    def debug(self, message):

        logger = self._create_logger()
        logger.debug(message)

    def info(self, message):

        logger = self._create_logger()
        logger.info(message)

    def warn(self, message):

        logger = self._create_logger()
        logger.warn(message)

    def error(self, message):

        logger = self._create_logger()
        logger.error(message)

        print >> sys.stderr, Logger.format_str % {'levelname' : 'ERROR',
                                   'name' : _get_calling_package(2),
                                   'asctime' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3],
                                   'message' : message}


    def critical(self, message):

        logger = self._create_logger()
        logger.critical(message)

        print >> sys.stderr, Logger.format_str % {'levelname' : 'CRITICAL',
                                   'name' : _get_calling_package(2),
                                   'asctime' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3],
                                   'message' : message}

    def _create_logger(self):

        logger = logging.getLogger(_get_calling_package())
        logger.setLevel(self._level)
        logger.addHandler(self._handler)

        return logger


def debug(string):
    Logger().debug(string)


def info(string):
    Logger().info(string)


def warn(string):
    Logger().warn(string)


def error(string):
    Logger().error(string)


def critical(string):
    Logger().critical(string)


def _get_calling_package(stack_level = 3):
    return getframe(stack_level).f_globals.get('__name__', 'root')
