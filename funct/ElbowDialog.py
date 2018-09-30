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

class ElbowDialog(wx.Dialog):
    def __init__(self, parent, id, title, flag="90"):
        self.flag = flag
        self.elbowValues = {}
        self.listOfIds = []
        for x in range(5):
            NewId = wx.NewId()
            self.listOfIds.append(NewId)

        wx.Dialog.__init__(self, parent, id, title, size=(300, 175))
        self.firstPanel = wx.Panel(self, self.listOfIds[0])
        self.secondPanel = wx.Panel(self, self.listOfIds[1], style=wx.SUNKEN_BORDER)#self.scrolledWindow(self)
        self.thirdPanel = wx.Panel(self, self.listOfIds[2])
        mainBox = wx.BoxSizer(wx.VERTICAL)
        if self.flag == "90":
            radioBoxList = self.elbowDialogGeneralText()["e1"]
        elif self.flag == "180":
            radioBoxList = self.elbowDialogGeneralText()["e6"]
        self.radioBox = wx.RadioBox(self.firstPanel, self.listOfIds[3], self.elbowDialogGeneralText()["e2"],
                    (50, 5), (200, 65), radioBoxList, 1, wx.RA_SPECIFY_COLS)

        self.setMiddlePanel(self.secondPanel)
        self.secondPanel.Enable(False)
 
        self.okButton = wx.Button(self.thirdPanel, wx.ID_OK, self.elbowDialogGeneralText()["e3"],
                                  size=(70, 30), pos=(220, 2))
        self.closeButton = wx.Button(self.thirdPanel, wx.ID_CANCEL, self.elbowDialogGeneralText()["e4"],
                                     size=(70, 30), pos=(145, 2))

        mainBox.Add(self.firstPanel, 12, wx.EXPAND)
        mainBox.Add(self.secondPanel, 5, wx.EXPAND)
        mainBox.Add(self.thirdPanel, 5, wx.EXPAND)

        self.radioBox.Bind(wx.EVT_RADIOBOX, self.onAny)
        self.SetSizer(mainBox)

        self.okButton.Bind(wx.EVT_BUTTON, self.onOkButton)
        self.closeButton.Bind(wx.EVT_BUTTON, self.onClose)
        self.okButton.SetDefault()
        self.Centre()


    def onClose(self, evt):
        self.Destroy()

    def onOkButton(self, evt):
        if self.flag == "90":
            if self.radioBox.GetSelection() == 0:
                self.elbowValues["type"] = "90_standard_elbow"

            elif self.radioBox.GetSelection() == 1:
                valueWidget = self.secondPanel.FindWindowById(self.listOfIds[4])
                value = valueWidget.GetValue()
                self.elbowValues["radius"] = value
                self.elbowValues["type"] = "90_welding_elbow"

            self.EndModal(wx.ID_OK)
        elif self.flag == "180":
            if self.radioBox.GetSelection() == 0:
                self.elbowValues["type"] = "180_close_pattern_return"

            elif self.radioBox.GetSelection() == 1:
                valueWidget = self.secondPanel.FindWindowById(self.listOfIds[4])
                value = valueWidget.GetValue()
                self.elbowValues["radius"] = value
                self.elbowValues["type"] = "180_bend"

            self.EndModal(wx.ID_OK)

#        print self.elbowValues

    def onAny(self, evt):
        if self.radioBox.GetSelection() == 0:
            self.secondPanel.Enable(False)

        elif self.radioBox.GetSelection() == 1:
            self.secondPanel.Enable(True)

    def setMiddlePanel(self, parent):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(parent, -1, self.elbowDialogGeneralText()["e5"])
        value = NumCtrl(parent, self.listOfIds[4], integerWidth=7, fractionWidth=0)
        sizer.Add(label, 1, flag=wx.ALL | wx.ALIGN_RIGHT, border=2)
        sizer.Add(value, 2, flag=wx.ALL | wx.ALIGN_LEFT, border=2)
        parent.SetSizer(sizer)
        parent.Fit()

    def elbowDialogGeneralText(self):
        text = Language()
        return text.elbowDialogGeneralText()

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
#        toolbar.AddLabelTool(ID_DEPTH, '', bmp)
#
#        self.Bind(wx.EVT_TOOL, self.onButton, id=ID_DEPTH)

        self.Centre()
        self.Show(True)

    def onButton(self, event):
        foo = ElbowDialog(None, -1, "window title")
        re = foo.ShowModal()
        if re == wx.ID_OK:
            values = foo.elbowValues
        else:
            values = None

        foo.Destroy()
        print values

if __name__ == "__main__":
    app = wx.App()
    Frame(None, -1, '')
    app.MainLoop()
