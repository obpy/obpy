#
# This module implements a simple text label.
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
#
# Copyright (C) 2011 The OpenBlox Project
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
__date__  = "$Jun 10, 2011 4:44:38 PM$"


import obengine.datatypes
import obengine.event
import obengine.depman
from obengine.gui import TextWidget, TextWidgetPresenter, MockTextWidgetView
obengine.depman.gendeps()


class Label(TextWidget):
    """Represents a simple label"""

    def __init__(self, text, position = None):
        TextWidget.__init__(self, text, position)


class LabelPresenter(TextWidgetPresenter):

    def __init__(self, label_model, label_view):
        TextWidgetPresenter.__init__(self, label_model, label_view)


class MockLabelView(MockTextWidgetView):

    def __init__(self, text, position = None):
        MockTextWidgetView.__init__(self, text, position)