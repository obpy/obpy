#!/usr/bin/env python

# A script that converts all non-binary files that have
# Windows newlines to UNIX-style newlines.

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
__date__  = "$Jun 3, 2011 2:26:02 PM$"

import os
import optparse


usage = '''%prog [options] [search directories]
Recursively converts all files under the given directories to use UNIX newlines.
If no search directories are given, either the
current directory is searched (if this script is invoked from the root
OpenBlox directory, that is, the one containing the "obengine" directory), or the parent
directory (the parent directory of the directory containing this script).
'''

exclude_exts = [
'.bat',
'.png',
'.egg.pz',
'.blend',
'.blend1',
'.dll',
'.so',
'.pyc',
'.pyd',
'.dblite',
'.zip',
]


def convert_newlines(dirs, loud = False, exclude_exts = exclude_exts):

    if dirs == []:

        if os.path.exists(os.path.join(os.curdir, 'obengine')):
            dirs = [os.curdir]

        else:
            dirs = [os.curdir, os.pardir]

    found_files = 0

    for directory in dirs:

        if loud is True:
            print 'Looking in directory %s for files with Windows newlines...' % directory

        for dirpath, dirnames, filenames in os.walk(directory):

            for filename in filenames:

                if os.path.splitext(filename)[1] in exclude_exts:

                    if loud is True:
                        print '\t(%s) Ignoring file %s' % (dirpath, filename)

                    continue

                candidate_file_path = os.path.join(dirpath, filename)
                original_data = open(candidate_file_path, 'rb').read()
                unixed_file_data = original_data.replace('\r\n', '\n')

                if original_data != unixed_file_data:

                    open(candidate_file_path, 'wb').write(unixed_file_data)

                    if loud is True:

                        print '\t(%s) Converted file %s' % (dirpath, filename)
                        found_files += 1

    if loud is True:

        print '=' * 5, 'RESULTS', '=' * 5
        print '\t* Found %d file(s) with at least 1 Windows newline' % found_files

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

    convert_newlines(args, options.verbose)

if __name__ == '__main__':
    main()