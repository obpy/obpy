#
# This package contains various OpenBlox utilites that haven't found their way
# into another package yet.
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
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
__date__  = "$Sep 28, 2010 1:35:13 PM$"


import obengine.depman
from obengine.datatypes import *
from obengine.log import *

obengine.depman.gendeps()


def search_dict(searched_dict, key, modifier = lambda a: a):
    return [k for k, v in searched_dict.iteritems() if key == modifier(v)]


def interp_range(given_range, requested_range, num):

    if (given_range[0] <= num <= given_range[1]) is False:
        raise ValueError('%d not in range %s' % (num, given_range))

    max_given_range = float(given_range[1])
    requested_range_diff = float(requested_range[1]) - float(requested_range[0])
    given_range_diff = float(given_range[1]) - float(given_range[0])
    
    min_requested_range = float(requested_range[0])

    percen = float(num) / max_given_range
    result = requested_range_diff * percen + min_requested_range

    return result


def sign(num):
    return cmp(num, 0)


def xfrange(start, end = None, inc = None):

    if end is None:

        end = start + 0.0
        start = 0.0

    if inc is None:
        inc = 1.0

    result_list = []

    while True:

        next = start + len(result_list) * inc

        if inc > 0 and next >= end:
            break

        elif inc < 0 and next <= end:
            break

        result_list.append(next)
        yield next


def frange(start, end = None, inc = None):
    return list(xfrange(start, end, inc))