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

    This module provides configuration utilites for other modules.
    Creation of configuration variables by calling add_config_var is non-persistent.
"""

__author__="openblocks"
__date__ ="$Aug 3, 2010 2:36:03 PM$"

import os
import sys
import ConfigParser

import datatypes
import depman

depman.gendeps()

__all__ = ['Config']

def init():

    if hasattr(Config, 'parser') is False:
        Config().load(CFG_FILE)

class Config(datatypes.Borg):
    """Provides basic configuration utilites.
    This is a Monostate/Borg class - sections and option values are
    maintained across class instances.
    """

    options = {}

    def load(self, filename):
        """Loads a configuration from filename
        Arguments:
        * filename - absolute path to the configuration file to be loaded.
        It must be in INI format (*not* with the extended Windows syntax).
        """

        WINDOWS_CFG_LOC = 'C:\\Program Files\\OpenBlox'
        UNIX_CFG_LOC = os.path.join(os.getenv('HOME', '/home/' + os.getlogin()), 'OpenBlox')
        CFG_FILE = 'obconf.cfg'

        # If this is True, then we're running normally
        if '.zip' not in __file__:
            basedir = __file__[:len(__file__) - len(os.path.join('obengine', 'cfg.py')) - 1]

        # We're running inside a .zip archive, probably for BloxWorks
        else:

            if sys.platform == 'win32':
                basedir = WINDOWS_CFG_LOC

            else:
                basedir = UNIX_CFG_LOC

        self.parser = ConfigParser.ConfigParser()
        self._root_dir = os.path.abspath(os.path.dirname(filename))

        lualibdir = os.path.join(self._root_dir, 'lualibs')
        datadir = os.path.join(self._root_dir, 'data')

        self.parser.read(filename)

        self.add_var('cfgdir', self._root_dir)
        self.add_var('lualibdir', lualibdir)
        self.add_var('datadir', datadir)

    def add_var(self, name, val, section = 'core'):
        """Adds a configuration variable
        Arguments:
        * name - the name of the variable
        * val - the value of this variable (anything will do)
        * section - the section to add the variable in.
        By default, this is `core`.
        """
        
        self.options.setdefault(section, {})[name] = val

    def get_var(self, name, section = 'core'):
        """Retrieves a configuration variable
        Retrieves ``name`` out of ``section``, if it exists.
        Otherwise, if ``name`` is not inside ``section``, then
        NoOptionError is raised.
        If ``section`` doesn't exist, then NoSectionError is raised.

        You probably want to use one of the other, higher-level methods instead,
        unless you've somehow managed to store a custom data type :)
        """

        try:
            return self.options[section][name]

        except KeyError:

            try:
                val = self.parser.get(section, name)

            except ConfigParser.NoOptionError:
                raise NoOptionError(name)

            except ConfigParser.NoSectionError:
                raise NoSectionError(section)

            else:

                self.add_var(name, val, section)
                return val

    def get_str(self, name, section = 'core'):
        """Returns configuration variable ``name``, stringified
        See Logger.get_var for more documentation.
        """
        return str(self.get_var(name, section))

    def get_int(self, name, section = 'core'):
        """Returns configuration variable ``name`` as an integer
        See Logger.get_var for more documentation.
        """
        return int(self.get_var(name, section))

    def get_float(self, name, section = 'core'):
        """Returns configuration variable ``name`` as a float
        See Logger.get_var for more documentation.
        """
        return float(self.get_var(name, section))

    def get_bool(self, name, section = 'core'):
        """Returns configuration variable ``name`` as a boolean
        If the variable marked by ``name``'s value is "yes", then ``True`` is returned.
        Otherwise, if variable ``name``'s value is "no", then False is returned.
        If it is neither, ValueError is raised.
        
        See Logger.get_var for more documentation.
        """

        conv_dict = {'yes' : True, 'no' : False}

        try:
            return conv_dict[self.get_var(name, section)]

        except KeyError:
            raise ValueError('Config variable %s in section %s was not a valid boolean' % (name, section))


class ConfigException(Exception): pass
class NoOptionError(ConfigException): pass
class NoSectionError(ConfigException): pass