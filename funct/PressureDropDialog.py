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
from funct import PressureConvert

ID_DEPTH = 1

class PressureDropDialog(wx.Dialog):
    def __init__(self, parent, id, title, min_dP=50, max_dP=100):
        self.min_dP = min_dP
        self.max_dP = max_dP
        textMsg = self.dPDialogGeneralText()["f1"] + " %s Pa - %s Pa" % (self.min_dP, self.max_dP)
        self.dPValues = {}
        self.listOfIds = []
        for x in range(6):
            NewId = wx.NewId()
            self.listOfIds.append(NewId)

        wx.Dialog.__init__(self, parent, id, title, size=(300, 175))
        self.firstPanel = wx.Panel(self, self.listOfIds[0])
        self.secondPanel = wx.Panel(self, self.listOfIds[1], style=wx.SUNKEN_BORDER)#self.scrolledWindow(self)
        self.thirdPanel = wx.Panel(self, self.listOfIds[2])
        mainBox = wx.BoxSizer(wx.VERTICAL)
        self.mainText = wx.StaticText(self.firstPanel, -1, textMsg, pos=(50,10))
        self.setMiddlePanel(self.secondPanel)

        self.okButton = wx.Button(self.thirdPanel, wx.ID_OK, self.dPDialogGeneralText()["f3"],
                                  size=(70, 30), pos=(220, 2))
        self.closeButton = wx.Button(self.thirdPanel, wx.ID_CANCEL, self.dPDialogGeneralText()["f4"],
                                     size=(70, 30), pos=(145, 2))

        mainBox.Add(self.firstPanel, 12, wx.EXPAND)
        mainBox.Add(self.secondPanel, 5, wx.EXPAND)
        mainBox.Add(self.thirdPanel, 5, wx.EXPAND)

        self.SetSizer(mainBox)

        self.okButton.Bind(wx.EVT_BUTTON, self.onOkButton)
        self.closeButton.Bind(wx.EVT_BUTTON, self.onClose)
        self.okButton.SetDefault()
        self.Centre()


    def onClose(self, evt):
        self.Destroy()

    def onOkButton(self, evt):
        okToClose = False
        valueWidget = self.secondPanel.FindWindowById(self.listOfIds[4])
        unitWidget = self.secondPanel.FindWindowById(self.listOfIds[5])
        valueEntered = valueWidget.GetValue()
        unitSelected = unitWidget.GetStringSelection()
        
        if unitWidget.GetSelection() != -1:
            pressure_drop_metric = PressureConvert(valueEntered, unitSelected, "Pa")
            print pressure_drop_metric,self.min_dP, self.max_dP
            if (pressure_drop_metric > self.min_dP and
                pressure_drop_metric < self.max_dP):
                self.dPValues["pressure_drop"] = valueEntered
                self.dPValues["pressure_drop_unit"] = str(unitSelected)
                self.dPValues["pressure_drop_metric"] = pressure_drop_metric
                okToClose = True
            else:
                msg = self.dPDialogGeneralText()["f6"] + " %s Pa - %s Pa" % (self.min_dP, self.max_dP)
                dialog = wx.MessageDialog(self, msg, self.dPDialogGeneralText()["f7"], style=wx.OK | wx.ICON_EXCLAMATION)
                dialog.ShowModal()
                dialog.Destroy()
                okToClose = False

        if okToClose:
            self.EndModal(wx.ID_OK)

    def onAny(self, evt):
        pass

    def setMiddlePanel(self, parent):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(parent, -1, self.dPDialogGeneralText()["f5"])
        value = NumCtrl(parent, self.listOfIds[4], integerWidth=7, fractionWidth=3)
        choices = self.dPDialogGeneralText()["f2"]
        units = wx.Choice(parent, self.listOfIds[5], choices=choices)
        sizer.Add(label, 1, flag=wx.ALL | wx.ALIGN_RIGHT, border=2)
        sizer.Add(value, 2, flag=wx.ALL | wx.ALIGN_LEFT, border=2)
        sizer.Add(units, 1, flag=wx.ALL | wx.ALIGN_LEFT, border=2)
        parent.SetSizer(sizer)
        parent.Fit()

    def dPDialogGeneralText(self):
        text = Language()
        return text.dPDialogGeneralText()

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
        foo = PressureDropDialog(None, -1, "window title")
        re = foo.ShowModal()
        if re == wx.ID_OK:
            values = foo.dPValues
        else:
            values = None

        foo.Destroy()
        print values

if __name__ == "__main__":
    app = wx.App()
    Frame(None, -1, '')
    app.MainLoop()
