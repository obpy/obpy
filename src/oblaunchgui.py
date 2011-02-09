#!/usr/bin/env python
"""
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
__author__="openblocks"
__date__ ="$Feb 4, 2011 10:29:57 PM$"

import obengine
import obengine.cfg
import obengine.utils

import os
import sys
import shutil

import wx

class GameBrowser(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self, None, wx.ID_ANY, 'OpenBlox Games Browser', size=(650, 450))

        self.game_panel = wx.Panel(self, wx.ID_ANY)
        self.games = wx.ListCtrl(self.game_panel, -1, style=wx.LC_REPORT)
        self.games.InsertColumn(0, 'Game', width=650)

        global_box = wx.BoxSizer(wx.VERTICAL)
        button_box = wx.BoxSizer(wx.HORIZONTAL)

        install_game_button = wx.Button(self.game_panel, wx.ID_NEW, 'Install new game')
        play_game_button = wx.Button(self.game_panel, 25, 'Play game')

        button_box.Add(install_game_button, 1, wx.LEFT)
        button_box.Add(play_game_button, 1, wx.RIGHT)

        global_box.Add(self.games, 1, wx.EXPAND)
        global_box.Add(button_box)

        self.game_panel.SetSizer(global_box)

        gamedir = os.listdir(os.path.join(os.getcwd(), 'games'))
        self.gamecount = 0

        for game in gamedir:

            if game.endswith('.zip'):

                index = self.games.InsertStringItem(sys.maxint, game.strip('.zip'))
                self.gamecount += 1

        self.Bind(wx.EVT_BUTTON, self.install_game, id=wx.ID_NEW)
        self.Bind(wx.EVT_BUTTON, self.play_game, id=25)

        self.Show(True)
        self.Centre()

    def install_game(self, event):

        initial_dir = os.getcwd()
        dialog = wx.FileDialog(self, 'Choose a game to install', initial_dir, '', 'OpenBlox games(*.zip)|*.zip', wx.OPEN)

        if dialog.ShowModal() == wx.ID_OK:

            filename = dialog.GetFilename()
            dirname = dialog.GetDirectory()

            path = os.path.join(dirname, filename)

            shutil.copyfile(path, os.path.join('games', filename))

            index = self.games.InsertStringItem(sys.maxint, filename.strip('.zip'))

            self.games.SetItemData(index, self.gamecount)
            self.games.itemDataMap[self.gamecount] = (filename.strip('.zip'),)

            self.gamecount += 1

        dialog.Destroy()

    def play_game(self, event):
        
        import oblaunch
        oblaunch.load_world(self.games.GetItemText(self.games.GetFocusedItem()))

obengine.cfg.init()
obengine.utils.init()

app = wx.App(False)
g = GameBrowser()
app.MainLoop()