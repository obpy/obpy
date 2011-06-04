#!/usr/bin/env python

# A script that converts all non-binary files that have
# Windows newlines to UNIX-style newlines.

__author__ = "openblocks"
__date__  = "$Jun 3, 2011 2:26:02 PM$"

import os
import difflib
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

if __name__ == '__main__':

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