#!/usr/bin/env python

# A simple script to remove all .pyc files, so OpenBlox's
# Mercurial repository isn't polluted with needless files.

__author__ = "openblocks"
__date__  = "$Jun 1, 2011 8:36:59 PM$"

import os
#!/usr/bin/env python

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
