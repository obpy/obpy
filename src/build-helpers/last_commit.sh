#!/bin/bash

# Shell script to output information about the last commit to the local
# OpenBlox Mercurial repository
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


HG="hg"


function usage()
{
    cat << EOF
    Usage: $0
    This shell script prints out information about the last commit
    to this computer's local copy of the OpenBlox Mercurial repository.
    Environment variables:

     * HG - the command to run Mercurial (by default, $HG)
EOF

}


function run_hg()
{
    $HG log --template \
    'Last revision {rev} commited by {author|person} on {date|shortdate} ({date|age})\n' \
    | tac | tail -n 1
}


if [ "--help" == "$1" ]; then

    usage
    exit 1

fi

if [ "-h" == "$1" ]; then

    usage
    exit 1

fi

run_hg