"""
Copyright (C) 2010 The OpenBlox Project

This file is part of The OpenBlox Game Engine.

    The OpenBlox Game Engine is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    The OpenBlox Game Engine is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with The OpenBlox Game Engine.  If not, see <http://www.gnu.org/licenses/>.

"""

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