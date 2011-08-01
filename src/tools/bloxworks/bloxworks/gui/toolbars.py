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
__date__  = "$Jul 31, 2011 8:48:24 PM$"


import obengine.math
import obengine.vfs
import obengine.gui


class TopToolbar(object):

    def __init__(self):

        widget_factory = obengine.gui.WidgetFactory()

        self._toolbar = widget_factory.make('shutter',
        position = obengine.math.Vector2D(0, 90))

        new_button = widget_factory.make('button',
        icon = obengine.vfs.getsyspath('bloxworks-data/icons/new.png'))
        self._toolbar.add(new_button)
        self.on_new_button_clicked = new_button.on_click

        open_button = widget_factory.make('button',
        icon = obengine.vfs.getsyspath('bloxworks-data/icons/open.png'))
        self._toolbar.add(open_button)
        self.on_open_button_clicked = open_button.on_click

        save_button = widget_factory.make('button',
        icon = obengine.vfs.getsyspath('bloxworks-data/data/icons/save.png'))
        self._toolbar.add(save_button)
        self.on_save_button_clicked = save_button.on_click

        pack_button = widget_factory.make('button',
        icon = obengine.vfs.getsyspath('bloxworks-data/data/icons/save.png'))
        self._toolbar.add(pack_button)
        self.on_pack_button_clicked = pack_button.on_click


class BottomToolbar(object):

    def __init__(self):

        widget_factory = obengine.gui.WidgetFactory()
        self._toolbar = widget_factory.make('shutter',
        position = obengine.math.Vector2D(0, -90))

        move_button = widget_factory.make('button',
        icon = obengine.vfs.getsyspath('bloxworks-data/data/icons/move.png'))
        self._toolbar.add(move_button)
        self.on_move_button_clicked = move_button.on_click

        scale_button = widget_factory.make('button',
        icon = obengine.vfs.getsyspath('bloxworks-data/data/icons/scale.png'))
        self._toolbar.add(scale_button)
        self.on_scale_button_clicked = scale_button.on_click

        repaint_button = widget_factory.make('button',
        icon = obengine.vfs.getsyspath('bloxworks-data/data/icons/repaint.png'))
        self._toolbar.add(repaint_button)


class SideToolbar(object):

    def __init__(self):

        widget_factory = obengine.gui.WidgetFactory()

        self._toolbar = widget_factory.make('shutter',
        position = obengine.math.Vector2D(-90, 0),
        layout_manager = obengine.gui.VerticalLayoutManager)

        sky_button = widget_factory.make('button',
        icon = obengine.vfs.getsyspath('bloxworks-data/data/icons/Sky.png'))
        self._toolbar.add(sky_button)
        self.on_sky_button_clicked = scale_button.on_click

        light_button = widget_factory.make('button',
        icon = obengine.vfs.getsyspath('bloxworks-data/data/icons/light.png'))
        self._toolbar.add(light_button)
        self.on_light_button_clicked = light_button.on_click

        lua_button = widget_factory.make('button',
        icon = obengine.vfs.getsyspath('bloxworks-data/data/icons/Lua.png'))
        self._toolbar.add(lua_button)
        self.on_lua_button_clicked = lua_button.on_click

        brick_button = widget_factory.make('button',
        icon = obengine.vfs.getsyspath('bloxworks-data/data/icons/add-brick.png'))
        self._toolbar.add(brick_button)
        self.on_brick_button_clicked = brick_button.on_click