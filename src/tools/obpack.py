#!/usr/bin/env python

"""
Copyright (C) 2011 The OpenBlox Project

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
import os.path
__author__="openblocks"
__date__ ="$Mar 29, 2011 2:39:03 PM$"

import os

import zipfile
import xml.etree.ElementTree as xmlparser

import wx

missing_world_xml = """
The file world.xml could not be found inside %s.

See http://openblox.tuxfamily.org/DirectoryLayout on how to add one.
"""

invalid_xml = """
Your world.xml file contains erroneous XML markup.
See http://openblox.tuxfamily.org/GameDevelopersManual for more info on this.
"""

class GamePacker(object):

    def __init__(self):
        self.setup_dialog()

    def setup_dialog(self):
        
        initial_dir = os.getcwd()
        self.dir_dialog = wx.DirDialog(None, 'Select game directory', initial_dir)

        self.dir_dialog.ShowModal()
        self.validate_game(self.dir_dialog.GetPath())

    def validate_game(self, game_dir):

        dialog_caption = 'Validation results'

        if not os.path.exists(os.path.join(game_dir, 'world.xml')):

            style = wx.ICON_ERROR | wx.OK

            wx.MessageDialog(None, missing_world_xml % game_dir, dialog_caption, style).ShowModal()
            return False


app = wx.App(False)
g = GamePacker()
app.MainLoop()
