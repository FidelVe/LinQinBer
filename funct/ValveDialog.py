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

#import sqlite3
import wx
from wx.lib.masked import NumCtrl
from lang import Language

ID_DEPTH = 1

class ValveDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        self.valveValues = {}
        self.listOfIds = []
        for x in range(5):
            NewId = wx.NewId()
            self.listOfIds.append(NewId)

        wx.Dialog.__init__(self, parent, id, title, size=(300, 175))
        self.firstPanel = wx.Panel(self, self.listOfIds[0])#, style=wx.BORDER_SUNKEN)
        self.secondPanel = wx.Panel(self, self.listOfIds[2], style=wx.BORDER_RAISED)
        mainBox = wx.BoxSizer(wx.VERTICAL)

        self.okButton = wx.Button(self.secondPanel, wx.ID_OK, self.valveDialogGeneralText()["e3"],
                                  size=(70, 30), pos=(219, 2))
        self.closeButton = wx.Button(self.secondPanel, wx.ID_CANCEL, self.valveDialogGeneralText()["e4"],
                                     size=(70, 30), pos=(144, 2))
        text = self.valveDialogGeneralText()["e7"]
        self.staticText = wx.StaticText(self.firstPanel, -1, text, pos=(40, 15))
        valveChoices = self.valveDialogGeneralText()["e8"]
        self.choices = wx.Choice(self.firstPanel, -1, (40, 35), choices=valveChoices)
        mainBox.Add(self.firstPanel, 12, wx.EXPAND)
        mainBox.Add(self.secondPanel, 5, wx.EXPAND)

        self.SetSizer(mainBox)

        self.okButton.Bind(wx.EVT_BUTTON, self.onOkButton)
        self.closeButton.Bind(wx.EVT_BUTTON, self.onClose)
        self.okButton.SetDefault()
        self.Centre()


    def onClose(self, evt):
        self.Destroy()

    def onOkButton(self, evt):
        okToClose = False
#        print self.choices.GetSelection()
        if  self.choices.GetSelection() == -1:
            dialog = wx.MessageDialog(self, self.valveDialogGeneralText()["e9"],
                                      self.valveDialogGeneralText()["e10"],
                                      style=wx.OK | wx.ICON_EXCLAMATION)
            dialog.ShowModal()
            dialog.Destroy()
            okToClose = False
        else:
            okToClose = True
            if self.choices.GetStringSelection() == self.valveDialogGeneralText()["e8"][0]:
                self.valveValues["type"] = "globe_valve_type_A"
            elif self.choices.GetStringSelection() == self.valveDialogGeneralText()["e8"][1]:
                self.valveValues["type"] = "globe_valve_type_B"
            elif self.choices.GetStringSelection() == self.valveDialogGeneralText()["e8"][2]:
                self.valveValues["type"] = "lift_check_valve_type_A"
            elif self.choices.GetStringSelection() == self.valveDialogGeneralText()["e8"][3]:
                self.valveValues["type"] = "lift_check_valve_type_B"
            elif self.choices.GetStringSelection() == self.valveDialogGeneralText()["e8"][4]:
                self.valveValues["type"] = "gate_valve"
            elif self.choices.GetStringSelection() == self.valveDialogGeneralText()["e8"][5]:
                self.valveValues["type"] = "stop_check_valve_type_A"
            elif self.choices.GetStringSelection() == self.valveDialogGeneralText()["e8"][6]:
                self.valveValues["type"] = "stop_check_valve_type_B"
            elif self.choices.GetStringSelection() == self.valveDialogGeneralText()["e8"][7]:
                self.valveValues["type"] = "stop_check_valve_type_C"
            elif self.choices.GetStringSelection() == self.valveDialogGeneralText()["e8"][8]:
                self.valveValues["type"] = "ball_valve"

        if okToClose:
#            pass
            self.EndModal(wx.ID_OK)


    def onAny(self, evt):
        pass
     
    def valveDialogGeneralText(self):
        text = Language()
        return text.valveDialogGeneralText()

class Frame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(350, 220))
        label="label"
        help="help"
        toolbar = self.CreateToolBar()
        bmp = wx.Image('accept.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        tool = toolbar.AddSimpleTool(-1, bmp, label, help)
        self.Bind(wx.EVT_MENU, self.onButton, tool)
        toolbar.Realize()

        self.Centre()
        self.Show(True)

    def onButton(self, event):
        foo = ValveDialog(None, -1, "window title")
        re = foo.ShowModal()
        if re == wx.ID_OK:
            values = foo.valveValues
        else:
            values = None

        foo.Destroy()
        print values

if __name__ == "__main__":
    app = wx.App()
    Frame(None, -1, '')
    app.MainLoop()
