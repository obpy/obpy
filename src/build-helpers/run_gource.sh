#!/bin/bash

# Shell script to run Gource with OpenBlox
# Author: openblocks
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


GOURCE_FLAGS="--hide filenames,dirnames,usernames \
--logo src/doc/source/_static/oblogo.png \
--title OpenBlox --key -s 0.2 -a 2.0 -i 0"

GOURCE="gource"


function usage()
{
    cat << EOF
    Usage: $0
    This script runs Gource (http://code.google.com/p/gource/) over your local
    copy of the OpenBlox Mercurial repository, producing a nice visualization
    of OpenBlox's development of to the current commit in your local
    repository clone. Mostly useless, but fun nonetheless :)

    Environment variables:

    * GOURCE_FLAGS: Flags/options to pass to Gource (currently $GOURCE_FLAGS)
    * GOURCE: The path to the Gource executable (currently $GOURCE)
EOF

}


function run_gource()
{
    cd ../..
    echo $GOURCE $GOURCE_FLAGS

    $GOURCE $GOURCE_FLAGS
}

# We're currently in the "build-helpers" subdirectory, and its parent directory
# contains the Mercurial repository, so change directories

if [ "--help" == "$1" ]; then

    usage
    exit 1

fi

if [ "-h" == "$1" ]; then

    usage
    exit 1

fi

run_gource

exit 0