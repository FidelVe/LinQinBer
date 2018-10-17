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

class MyDialog(wx.Dialog):
    def __init__(self, parent, id, title, choices, staticText):
        wx.Dialog.__init__(self, parent, id, title, size=(200, 200))
        self.stringSelected = None
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.stline = wx.StaticText(self, -1, staticText)
        vbox.Add(self.stline, 1, wx.ALIGN_LEFT|wx.TOP, 10)
        self.listBox = wx.ListBox(self, -1, choices=choices, style=wx.LB_SINGLE)
        self.listBox.SetSelection(0)
        vbox.Add(self.listBox, 5, wx.EXPAND)
        sizer =  self.CreateButtonSizer(wx.NO|wx.YES)
        vbox.Add(sizer, 0, wx.ALIGN_CENTER)
        self.SetSizer(vbox)
        self.Bind(wx.EVT_BUTTON, self.OnYes, id=wx.ID_YES)
        self.Bind(wx.EVT_BUTTON, self.OnNo, id=wx.ID_NO)

    def OnYes(self, evt):
        self.stringSelected = self.listBox.GetStringSelection()
        print self.stringSelected
        self.Close()

    def OnNo(self, evt):
        self.Close()


class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        panel = wx.Panel(self, -1)
        wx.Button(panel, 1, 'Show custom Dialog', (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnShowCustomDialog, id=1)

    def OnShowCustomDialog(self, event):
        dia = MyDialog(self, -1, "title", ["first", "second"], "Seleccionar sentido del flujo")
        val = dia.ShowModal()
        dia.Destroy()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'customdialog2.py')
        frame.Show(True)
        frame.Centre()
        return True

app = MyApp(0)
app.MainLoop()
