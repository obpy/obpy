#!/usr/bin/env python

# A script that takes a normal OpenBlox game and turns it into a stand-alone,
# directly executable file.
# See <TODO: no Sphinx docs yet - add some> for the main source of documentation
# for this script.

#
# This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


__author__="openblocks"
__date__ ="$Jun 7, 2011 9:57:13 PM$"

import os
import optparse

OBRUNTIME_LOC = os.path.abspath(os.path.join(os.pardir, 'build', 'obruntime.zip'))

def main():

    option_parser = optparse.OptionParser()
    option_parser.add_option(
    '-r',
    '--runtime-loc',
    dest = 'runtime_loc',
    help = 'Path to the OpenBlox runtime (by default, %s)' % OBRUNTIME_LOC,
    default = OBRUNTIME_LOC
    )

    options, args = option_parser.parse_args()

    print 'Sorry, script not yet implemented!'

if __name__ == '__main__':
    main()