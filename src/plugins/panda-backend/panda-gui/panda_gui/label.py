
#
# <module description>
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
__date__  = "$Jul 1, 2011 4:07:21 PM$"


import direct.gui.DirectGui
import direct.gui.DirectGuiGlobals

import obengine.math
import obengine.datatypes
import obengine.event
import widget


class LabelView(widget.WidgetView):

    def __init__(self, text = '', position = None):

        self._widget = direct.gui.DirectGui.DirectLabel(
        scale = widget.WidgetView.WIDGET_SCALE,
        frameColor = (0, 0, 0, 0),
        textMayChange = True
        )

        widget.WidgetView.__init__(self, position)
        self.text = text

    @obengine.datatypes.nested_property
    def text():

        def fget(self):
            return self._widget['text']

        def fset(self, new_text):

            old_size = self.size
            self._widget['text'] = new_text
            self._widget.setText()
            self._widget.resetFrameSize()
            new_size = self.size

            if old_size.x != new_size.x or old_size.y != new_size.y:
                self.on_size_changed(new_size)

        return locals()