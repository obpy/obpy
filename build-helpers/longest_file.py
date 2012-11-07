#!/usr/bin/env python

# A small Python script that finds the top-n longest Python modules

#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


__author__ = "openblocks"
__date__ = "Nov 16, 2011 10:54:00 AM"


import os
import optparse


IGNORED_DIRECTORIES = ['pyinstaller-1.5.1']


def ignored_directory(dir):

    if dir.startswith(os.pardir):
        dir = dir[len(os.pardir) + len(os.sep):]

    for ignored_dir in IGNORED_DIRECTORIES:
        if dir.startswith(ignored_dir) or dir.startswith(os.path.join(os.curdir, ignored_dir)):
            return True

    return False


def find_longest_modules(dirs = [], loud = False):

    if dirs == []:

        if os.path.exists(os.path.join(os.curdir, 'obengine')):
            dirs = [os.curdir]
        else:
            dirs = [os.curdir, os.pardir]

    python_modules = []

    for directory in dirs:

        if loud is True:
            print 'Looking in directory %s for .py files...' % directory

        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:

                if ignored_directory(dirpath):
                    continue

                if filename.endswith('.py'):

                    full_file_path = os.path.join(dirpath, filename)

                    if loud is True:
                        print 'Found Python module %s' % full_file_path

                    python_modules.append((full_file_path, open(full_file_path, 'r').read().count('\n')))

    if loud is True:
        print 'Found %d Python modules' % len(python_modules)

    python_modules.sort(key = lambda t: t[1], reverse = True)

    return python_modules


def main():

    option_parser = optparse.OptionParser()

    option_parser.add_option(
    '-v',
    '--verbose',
    dest = 'verbose',
    help = 'Print status messages to stdout (by default, this isn\'t done)',
    action = 'store_true',
    default = False
    )

    option_parser.add_option(
    '-n',
    '--top',
    dest = 'module_count',
    type = 'int',
    help = 'Display the top MODULE_COUNT longest Python modules (by default, 10)',
    default = 10
    )

    options, args = option_parser.parse_args()

    longest_modules = find_longest_modules(args, options.verbose)
    module_count = options.module_count

    print 'Top %d-longest Python modules:' % module_count

    module_line_count = []

    for standing, (module_name, line_count) in enumerate(longest_modules[:module_count]):

        print '#%d: %s - %d line(s)' % (standing + 1, module_name, line_count)

    for _, line_count in longest_modules:
        module_line_count.append(line_count)

    print 'Average module length: %d lines' % (sum(module_line_count) / len(module_line_count))


if __name__ == '__main__':
    main()
