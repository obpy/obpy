#
# This module provides basic configuration functionality to OpenBlox.
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
#
#
# Copyright (C) 2010-2011 The OpenBlox Project
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
__date__  = "$Aug 3, 2010 2:36:03 PM$"

import os
import ConfigParser

import obengine.datatypes
import obengine.depman

obengine.depman.gendeps()


__all__ = ['Config', 'CFG_FILE']
CFG_FILE = 'obconf.cfg'


def init():

    if Config.options == {} and os.path.exists(CFG_FILE):
        Config().load(CFG_FILE)


class Config(obengine.datatypes.Borg):
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

    def get_var(self, name, section = 'core', default = None):
        """Retrieves a configuration variable
        Retrieves `name` out of section, if it exists.
        Otherwise, if`name` is not inside section, then
        NoOptionError is raised.
        If section doesn't exist, then NoSectionError is raised.

        You probably want to use one of the other, higher-level methods instead,
        unless you've somehow managed to store a custom data type :)
        """

        try:
            return self.options[section][name]

        except KeyError:

            try:
                val = self.parser.get(section, name)

            except ConfigParser.NoSuchOptionError:

                if default is None:
                    raise NoSuchOptionError(name)

                return default

            except ConfigParser.NoSectionError:

                if default is None:
                    raise NoSuchSectionError(section)

                return default

            else:

                self.add_var(name, val, section)
                return val

    def get_str(self, name, section = 'core', default = None):
        """Returns configuration variable `name`, stringified
        See Config.get_var for more documentation.
        """
        return str(self.get_var(name, section, default))

    def get_int(self, name, section = 'core', default = None):
        """Returns configuration variable `name` as an integer
        See Config.get_var for more documentation.
        """
        return int(self.get_var(name, section, default))

    def get_float(self, name, section = 'core', default = None):
        """Returns configuration variable `name` as a float
        See Config.get_var for more documentation.
        """
        return float(self.get_var(name, section, default))

    def get_bool(self, name, section = 'core', default = None):
        """Returns configuration variable `name` as a boolean
        If the variable marked by `name`'s value is "yes", then True is returned.
        Otherwise, if variable `name`'s value is "no", then False is returned.
        If it is neither, ValueError is raised.
        
        See Config.get_var for more documentation.
        """

        conv_dict = {'yes' : True, 'no' : False}

        try:
            return conv_dict[self.get_var(name, section)]

        except KeyError:
            raise ValueError('Config variable %s in section %s was not a valid boolean' % (name, section))

class ConfigException(Exception): pass
class NoSuchOptionError(ConfigException): pass
class NoSuchSectionError(ConfigException): pass