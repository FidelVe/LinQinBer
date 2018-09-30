#!/usr/bin/env python

###################################################################################
# LinQinber: Is and open source pipe system design software written in python.    #
#    Copyright (C) 2010 Fidel Sanchez-Bueno                                       #
#                                                                                 # 
#                                                                                 #
# This file is part of LinQinBer.                                                 #
#                                                                                 #
#   LinQinBer is free software: you can redistribute it and/or modify             #
#    it under the terms of the GNU General Public License as published by         #
#    the Free Software Foundation, either version 3 of the License, or            #
#    (at your option) any later version.                                          #
#                                                                                 #
#    LinQinBer is distributed in the hope that it will be useful,                 #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of               #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
#    GNU General Public License for more details.                                 #
#                                                                                 #
#    You should have received a copy of the GNU General Public License            #
#    along with LinQinBer.  If not, see <http://www.gnu.org/licenses/>.           #
###################################################################################

__author__ = "Fidel Sanchez-Bueno"
__date__  = "$16/06/2010 08:00:00 PM$"
__appName__ = "LinQinBer"

import wx

ID_DEPTH = 1

class ChangeDepth(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(260, 230))

        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)

        wx.StaticBox(panel, -1, 'Colors', (5, 5), (240, 150))
        wx.RadioButton(panel, -1, '256 Colors', (15, 30), style=wx.RB_GROUP)
        wx.RadioButton(panel, -1, '16 Colors', (15, 55))
        wx.RadioButton(panel, -1, '2 Colors', (15, 80))
        wx.RadioButton(panel, -1, 'Custom', (15, 105))
        wx.TextCtrl(panel, -1, '', (95, 105))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, -1, 'Ok', size=(70, 30))
        closeButton = wx.Button(self, -1, 'Close', size=(70, 30))
        hbox.Add(okButton, 1)
        hbox.Add(closeButton, 1, wx.LEFT, 5)

        vbox.Add(panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)

        self.SetSizer(vbox)


class Frame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(350, 220))
        label="label"
        help="help"
        toolbar = self.CreateToolBar()
        bmp = wx.Image('accept.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        tool = toolbar.AddSimpleTool(-1, bmp, label, help)
        self.Bind(wx.EVT_MENU, self.OnChangeDepth, tool)
        toolbar.Realize()
#        toolbar.AddLabelTool(ID_DEPTH, '', bmp)
#
#        self.Bind(wx.EVT_TOOL, self.onButton, id=ID_DEPTH)

        self.Centre()
        self.Show(True)

    def onButton(self, event):
        chgdep = ChangeDepth(None, -1, 'Change Color Depth')
        chgdep.ShowModal()
        chgdep.Destroy()

app = wx.App()
Frame(None, -1, '')
app.MainLoop()
