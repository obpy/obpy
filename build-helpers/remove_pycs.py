#!/usr/bin/env python

# A simple script to remove all .pyc files, so OpenBlox's
# Mercurial repository isn't polluted with needless files.

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
__date__  = "$Jun 1, 2011 8:36:59 PM$"


import os
import optparse


usage = '''%prog [options] [search directories]
Recursively removes all .pyc files from the specified search directories.
If no search directories are given,
either the current directory is searched (if this script is invoked from the root OpenBlox directory,
that is, the one containing the "obengine" directory), or the
parent directory (if this script invoked from this script's parent directory).
'''


def remove_pycs(dirs, loud = False):

    if dirs == []:

        if os.path.exists(os.path.join(os.curdir, 'obengine')):
            dirs = [os.curdir]

        else:
            dirs = [os.curdir, os.pardir]

    found_pycs = 0

    for directory in dirs:

        if loud is True:
            print 'Looking in directory %s for .pyc files...' % directory

        for dirpath, dirnames, filenames in os.walk(directory):

            for filename in filenames:

                if filename.endswith('.pyc'):

                    path = os.path.join(dirpath, filename)
                    os.remove(path)
                    
                    if loud is True:

                        print '\t(%s) Removed pyc file %s' % (dirpath, filename)
                        found_pycs += 1

    if loud is True:

        print '=' * 5, 'RESULTS', '=' * 5
        print '\t* Found and removed %d .pyc file(s)' % found_pycs


def main():

    option_parser = optparse.OptionParser(usage = usage)

    option_parser.add_option(
    '-v',
    '--verbose',
    dest = 'verbose',
    help = 'Print status messages to stdout (by default, this isn\'t done)',
    action = 'store_true',
    default = False
    )

    options, args = option_parser.parse_args()

    remove_pycs(args, options.verbose)


if __name__ == '__main__':
    main()
