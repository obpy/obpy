#!/usr/bin/env python

# A script that automatically packs a directory into an OpenBlox-compatible
# .zip archive (i.e, an OpenBlox game).
# See <TODO: no Sphinx docs yet - add some> for the main source of documentation
# for this script.

#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


__author__="openblocks"
__date__ ="$Mar 29, 2011 2:39:03 PM$"


import os
import zipfile
import xml
import xml.etree.ElementTree as xmlparser

import wx


missing_world_xml = """
The file world.xml could not be found inside %s.

See http://openblox.tuxfamily.org/DirectoryLayout on how to add one.
"""

invalid_xml = """
Your world.xml file contains erroneous XML markup at %s.
See http://openblox.tuxfamily.org/GameDevelopersManual for more info on this.
"""


class GamePacker(object):

    def __init__(self):

        self.setup_dialog()
        self.pack_game()

    def setup_dialog(self):
        
        initial_dir = os.getcwd()
        self.dir_dialog = wx.DirDialog(None, 'Select game directory', initial_dir)

    def pack_game(self):

        self.dir_dialog.ShowModal()

        directory = self.dir_dialog.GetPath()

        if self.validate_game(directory) == True:

            dest = self.get_output_zip()
            directory = os.path.basename(directory)
            self.write_game(directory, directory, dest)

    def write_game(self, name, directory, dest, archive = None):

         if archive is None:
            archive = zipfile.ZipFile(dest, 'w')

         paths = os.listdir(directory)

         for p in paths:

             if os.path.isdir(p):
                self.write_game(p, os.path.join(directory, dest), archive)

             else:

                 if directory == name:
                    archive.write(os.path.join(directory, p), arcname=p)


                 else:
                      archive.write(os.path.join(directory, p))

    def get_output_zip(self):

        style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        initial_dir = os.getcwd()
        filetype = 'OpenBlox games (*.zip)|*.zip'

        dialog = wx.FileDialog(None, 'Select packed game filename', initial_dir, wildcard = filetype, style = style)
        dialog.ShowModal()

        return dialog.GetPath()

    def validate_game(self, game_dir):

        dialog_caption = 'Validation results'

        if not os.path.exists(os.path.join(game_dir, 'world.xml')):

            style = wx.ICON_ERROR | wx.OK

            wx.MessageDialog(None, missing_world_xml % game_dir, dialog_caption, style).ShowModal()
            return False

        try:
            xmlparser.parse(open(os.path.join(game_dir, 'world.xml')))

        except xml.parsers.expat.ExpatError, exception:

            style = wx.ICON_ERROR | wx.OK
            location = exception.args[0].split(':')[1][1:]

            wx.MessageDialog(None, invalid_xml % location, dialog_caption, style).ShowModal()
            return False

        return True

if __name__ == '__main__':

    app = wx.App(False)
    g = GamePacker()
    app.MainLoop()
