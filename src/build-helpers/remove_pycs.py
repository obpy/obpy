#!/usr/bin/env python

# A simple script to remove all .pyc files, so OpenBlox's
# Mercurial repository isn't polluted with needless files.

__author__ = "openblocks"
__date__  = "$Jun 1, 2011 8:36:59 PM$"

import os
import optparse

def remove_pycs(dirs, loud = False):

    if dirs == []:
        dirs = [os.path.abspath(os.pardir), os.path.abspath(os.curdir)]

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

                        print '\t (%s) Removed pyc file %s' % (dirpath, filename)
                        found_pycs += 1

    if loud is True:

        print '=' * 5, 'RESULTS', '=' * 5
        print '* Found and removed %d .pyc files' % found_pycs


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

    options, args = option_parser.parse_args()

    remove_pycs(args, options.verbose)

if __name__ == '__main__':
    main()