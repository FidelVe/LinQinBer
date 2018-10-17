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
import sqlite3
import wx
import funct as f
from wx.lib.masked import NumCtrl
from lang import Language

ID_DEPTH = 1

class ContExpDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        self.database = "funct/database.pype"
        self.contExpValues = {}
        self.listOfIds = []
        for x in range(17):
            NewId = wx.NewId()
            self.listOfIds.append(NewId)

        wx.Dialog.__init__(self, parent, id, title, size=(300, 265))
        self.firstPanel = wx.Panel(self, self.listOfIds[0])
        self.secondPanel = wx.Panel(self, self.listOfIds[1], style=wx.SUNKEN_BORDER)#self.scrolledWindow(self)
        self.thirdPanel = wx.Panel(self, self.listOfIds[2])
        mainBox = wx.BoxSizer(wx.VERTICAL)

        radioBoxList = self.contExpDialogGeneralText()["e1"]
        self.radioBox = wx.RadioBox(self.firstPanel, self.listOfIds[3], self.contExpDialogGeneralText()["e2"],
                    (50, 5), (200, 65), radioBoxList, 1, wx.RA_SPECIFY_COLS)

        self.setMiddlePanel(self.secondPanel)
#        self.secondPanel.Enable(False)

        self.okButton = wx.Button(self.thirdPanel, wx.ID_OK, self.contExpDialogGeneralText()["e3"],
                                  size=(70, 30), pos=(220, 2))
        self.closeButton = wx.Button(self.thirdPanel, wx.ID_CANCEL, self.contExpDialogGeneralText()["e4"],
                                     size=(70, 30), pos=(145, 2))

        mainBox.Add(self.firstPanel, 9, wx.EXPAND)
        mainBox.Add(self.secondPanel, 15, wx.EXPAND)
        mainBox.Add(self.thirdPanel, 4, wx.EXPAND)

        self.radioBox.Bind(wx.EVT_RADIOBOX, self.analizeSelection)
        self.SetSizer(mainBox)

        self.okButton.Bind(wx.EVT_BUTTON, self.onOkButton)
        self.closeButton.Bind(wx.EVT_BUTTON, self.onClose)
        self.okButton.SetDefault()
        self.lastSegmentValues = self.setDisabledWidget()

        self.Centre()

    def typeOfPipe(self, pipeTypeAcron):
        if pipeTypeAcron == "CSP":
            pipeType = "Commercial_Steel_Pipe_c"
        elif pipeTypeAcron == "SSP":
            pipeType = "Stainless_Steel_Pipe_c"
        elif pipeTypeAcron == "PVC":
            pipeType = "PVC_Pipe_c"
        else:
            pipeType = "None"
#            msg = self.pipeDialogGeneralText()["d14"]
#            raise Exception, msg
        return pipeType

    def dataBaseConsult(self, sched, pipeType):
#        ID = []
        OD = []
        NPS = []
        flag = 0

        if (sched == "STD" or
            sched == "XS" or
            sched == "DXS"):
            typeOfPipe = pipeType[:-1]
        else:
            typeOfPipe = pipeType

            connection = sqlite3.connect("funct/database.pype")
            cursor = connection.cursor()
            sqlcommand = """SELECT Nominal_Pipe_size, Outside_Diameter FROM %s""" % typeOfPipe+sched
            cursor.execute(sqlcommand)
            system_data = cursor.fetchall()
            connection.close()

            for value in system_data:
#                print value
                if flag:
                    NPS.append(str(value[0]))
                    OD.append(str(value[1]))
#                    ID.append(str(value[2]))
                else:
                    flag += 1

            return NPS, OD
#        print system_data

    def onClose(self, evt):
        self.Destroy()

    def onOkButton(self, evt):
        okToClose = False
#        print self.lastSegmentValues
        schedule = self.lastSegmentValues[0][1]
        NPS = self.lastSegmentValues[0][2]
        OD  = self.lastSegmentValues[0][3]
#        ID = self.lastSegmentValues[0][4]
        minimunDiameter = self.lastSegmentValues[0][5]

        if schedule != "None":
            #si la cedula fue especificada en el segmento anterior

            if self.NPSChoice.IsEnabled():
                #si la casilla de NPS esta habilitada
                selected = float(self.NPSChoice.GetStringSelection())
                if self.radioBox.GetSelection() == 0:
                    #si se selecciona expansion
                    self.contExpValues["type"] = "sudden_expansion"
                    if selected > NPS:
                        self.contExpValues["D_2"] = selected
                        self.contExpValues["D_2_type"] = "NPS"
                        okToClose = True
                    else:
                        text = self.contExpDialogGeneralText()["e5"] + " %s" % NPS
                        dialog = wx.MessageDialog(self, text, self.contExpDialogGeneralText()["e6"],
                                                  style=wx.OK | wx.ICON_EXCLAMATION)
                        dialog.ShowModal()
                        dialog.Destroy()
                        okToClose = False

                elif self.radioBox.GetSelection() == 1:
                    #si se selecciona contraccion
                    self.contExpValues["type"] = "sudden_contraction"
                    if selected < NPS:
                        self.contExpValues["D_2"] = selected
                        self.contExpValues["D_2_type"] = "NPS"
                        okToClose = True
                    else:
                        text = self.contExpDialogGeneralText()["e7"] + " %s" % NPS
                        dialog = wx.MessageDialog(self, text, self.contExpDialogGeneralText()["e6"],
                                                  style=wx.OK | wx.ICON_EXCLAMATION)
                        dialog.ShowModal()
                        dialog.Destroy()
                        okToClose = False

            elif self.ODChoice.IsEnabled():
                #si la casilla de OD esta habilitada
                selected = float(self.ODChoice.GetStringSelection())
                if self.radioBox.GetSelection() == 0:
                    #si se selecciona expansion
                    self.contExpValues["type"] = "sudden_expansion"
                    if selected > OD:
                        self.contExpValues["D_2"] = selected
                        self.contExpValues["D_2_type"] = "OD"
                        okToClose = True
                    else:
                        text = self.contExpDialogGeneralText()["e8"] + " %s" % OD
                        dialog = wx.MessageDialog(self, text, self.contExpDialogGeneralText()["e6"],
                                                  style=wx.OK | wx.ICON_EXCLAMATION)
                        dialog.ShowModal()
                        dialog.Destroy()
                        okToClose = False

                elif self.radioBox.GetSelection() == 1:
                    #si se selecciona contraccion
                    self.contExpValues["type"] = "sudden_contraction"
                    if selected < OD:
                        self.contExpValues["D_2"] = selected
                        self.contExpValues["D_2_type"] = "OD"
                        okToClose = True
                    else:
                        text = self.contExpDialogGeneralText()["e9"] + " %s" % OD
                        dialog = wx.MessageDialog(self, text, self.contExpDialogGeneralText()["e6"],
                                                  style=wx.OK | wx.ICON_EXCLAMATION)
                        dialog.ShowModal()
                        dialog.Destroy()
                        okToClose = False

#            elif self.IDChoice.IsEnabled():
#                #si la casilla de ID esta habilitada
#                selected = float(self.IDChoice.GetStringSelection())
#                if self.radioBox.GetSelection() == 0:
#                    #si se selecciona expansion
#                    self.contExpValues["type"] = "sudden_expansion"
#                    if selected > ID:
#                        self.contExpValues["D_2"] = selected
#                        self.contExpValues["D_2_type"] = "ID"
#                        okToClose = True
#                    else:
#                        text = "El valor de ID elegido\ndebe ser mayor a %s" % ID
#                        dialog = wx.MessageDialog(self, text,
#                                                  "titulo", style=wx.OK | wx.ICON_EXCLAMATION)
#                        dialog.ShowModal()
#                        dialog.Destroy()
#                        okToClose = False
#
#                elif self.radioBox.GetSelection() == 1:
#                    #si se selecciona contraccion
#                    self.contExpValues["type"] = "sudden_contraction"
#                    if selected < ID:
#                        self.contExpValues["D_2"] = selected
#                        self.contExpValues["D_2_type"] = "ID"
#                        okToClose = True
#                    else:
#                        text = "El valor de ID elegido\ndebe ser menor a %s" % ID
#                        dialog = wx.MessageDialog(self, text,
#                                                  "titulo", style=wx.OK | wx.ICON_EXCLAMATION)
#                        dialog.ShowModal()
#                        dialog.Destroy()
#                        okToClose = False

            else:
                #la condicion "else" no deberia darse pero por si acaso
                msg = "se cumplio condicion else en calculo de expansion/contraccion\nmodulo: onOkButton"
                raise Exception, msg

        else:
            #si no fue especificada la cedula se esta trabajando con el diametro minimo
            selected = self.minimumDiamValue.GetValue()
            units = self.minimumDiamUnit.GetStringSelection()
            if self.radioBox.GetSelection() == 0:
                #si se selecciona expansion
                self.contExpValues["type"] = "sudden_expansion"
                minimumDiameterOtherUnit = f.DistanceConvert(minimunDiameter, "m", units)
                if selected > minimumDiameterOtherUnit:
                    self.contExpValues["minimum_diameter"] = selected
                    self.contExpValues["minimum_diameter_unit"] = units
                    okToClose = True
                else:
                    text = self.contExpDialogGeneralText()["e10"] + " %s %s" % (minimumDiameterOtherUnit,units)
                    dialog = wx.MessageDialog(self, text, self.contExpDialogGeneralText()["e6"],
                                                  style=wx.OK | wx.ICON_EXCLAMATION)
                    dialog.ShowModal()
                    dialog.Destroy()
                    okToClose = False

            elif self.radioBox.GetSelection() == 1:
                #si se selecciona contraccion
                self.contExpValues["type"] = "sudden_contraction"
                minimumDiameterOtherUnit = f.DistanceConvert(minimunDiameter, "m", units)
                if selected < minimumDiameterOtherUnit:
                    self.contExpValues["minimum_diameter"] = selected
                    self.contExpValues["minimum_diameter_unit"] = units
                    okToClose = True
                else:
                    text = self.contExpDialogGeneralText()["e11"] + " %s %s" % (minimumDiameterOtherUnit,units)
                    dialog = wx.MessageDialog(self, text, self.contExpDialogGeneralText()["e6"],
                                                  style=wx.OK | wx.ICON_EXCLAMATION)
                    dialog.ShowModal()
                    dialog.Destroy()
                    okToClose = False
            
        if okToClose:
#            print self.contExpValues
            self.EndModal(wx.ID_OK)
#        print self.contExpValues

    def analizeSelection(self, evt):
        """Modulo que activa y desactiva widgets
        dependiendo de las seleciones de los radiobox
        """
        schedule = self.lastSegmentValues[0][1]
#        NPS = self.lastSegmentValues[0][2]
#        OD  = self.lastSegmentValues[0][3]
#        ID = self.lastSegmentValues[0][4]
#        minimunDiameter = self.lastSegmentValues[0][5]
        
        if schedule != "None":
            #si la cedula fue especificada en el segmento anterior
#            NPSselection = self.NPSChoice.GetStringSelection()
#            ODselection = self.ODChoice.GetStringSelection()
#            IDselection =self.IDChoice.GetStringSelection()

            if self.middlePanelRadioBox.GetSelection() == 0:
                #si se selecciona NPS para usar
                self.NPSChoice.Enable(True)
                self.ODChoice.Enable(False)
#                self.IDChoice.Enable(False)
    #            if NPSselection != -1:
    #                self.contExpValues["D_2"] = NPSselection
    #                self.contExpValues["D_2_type"] = "NPS"

            elif self.middlePanelRadioBox.GetSelection() == 1:
                #si se selecciona OD para usar
                self.NPSChoice.Enable(False)
                self.ODChoice.Enable(True)
#                self.IDChoice.Enable(False)
    #            if ODselection != -1:
    #                self.contExpValues["D_2"] = ODselection
    #                self.contExpValues["D_2_type"] = "OD"

            elif self.middlePanelRadioBox.GetSelection() == 2:
                #si se selecciona ID para usar
                self.NPSChoice.Enable(False)
                self.ODChoice.Enable(False)
#                self.IDChoice.Enable(True)
    #            if IDselection != -1:
    #                self.contExpValues["D_2"] = IDselection
    #                self.contExpValues["D_2_type"] = "ID"

        else:
            #si no fue especificada la cedula se esta trabajando con el diametro minimo
            pass
#    def onAny(self, evt):
#        schedule = self.lastSegmentValues[0][1]

#        if schedule != "None":
#            #si la cedula fue especificada en el segmento anterior
#
#            if self.radioBox.GetSelection() == 0:
#                #si se selecciona expansion
##                self.contExpValues["type"] = "sudden_expansion"
##                self.analizeSelection(self)
#                pass
#
#            elif self.radioBox.GetSelection() == 1:
#                #si se selecciona una contraccion
##                self.contExpValues["type"] = "sudden_contraction"
##                self.analizeSelection(self)
#                pass
#        else:
#            #si no fue especificada la cedula se esta trabajando con el diametro minimo
#            if self.radioBox.GetSelection() == 0:
#                #si se selecciona expansion
##                self.contExpValues["type"] = "sudden_expansion"
#                "foo"
#
#            elif self.radioBox.GetSelection() == 1:
#                #si se selecciona una contraccion
##                self.contExpValues["type"] = "sudden_contraction"
#                "baar"


    def setMiddlePanel(self, parent):

        sizer = wx.GridBagSizer(hgap=0, vgap=5)

        self.textLabel = wx.StaticText(parent, self.listOfIds[16], self.contExpDialogGeneralText()["e12"],
                                       size=(150, 30))
        sizer.Add(self.textLabel, pos=(0,0), span=(1,2), flag=wx.EXPAND)

        radioBoxChoices = ["NPS", "OD"]
        self.middlePanelRadioBox = wx.RadioBox(parent, self.listOfIds[13], self.contExpDialogGeneralText()["e13"],  size=(100, 40),
                                               choices=radioBoxChoices, majorDimension=3, style=wx.RA_SPECIFY_COLS)
        self.middlePanelRadioBox.Bind(wx.EVT_RADIOBOX, self.analizeSelection)
        sizer.Add(self.middlePanelRadioBox, pos=(0,2), span=(1,2), flag=wx.EXPAND)

        self.NPSLabel = wx.StaticText(parent, self.listOfIds[14], "NPS", size=(150, 21))
        sizer.Add(self.NPSLabel, pos=(1,0), span=(1,2), flag=wx.EXPAND)
        self.NPSChoice = wx.Choice(parent, self.listOfIds[15], choices=self.contExpDialogGeneralText()["e14"], size=(145, 21))
        self.NPSChoice.Bind(wx.EVT_CHOICE, self.analizeSelection)
        sizer.Add(self.NPSChoice, pos=(1,2), span=(1,2), flag=wx.EXPAND)

        self.ODLabel = wx.StaticText(parent, self.listOfIds[4], "OD", size=(150, 21))
        sizer.Add(self.ODLabel, pos=(2,0), span=(1,2), flag=wx.EXPAND)
        self.ODChoice = wx.Choice(parent, self.listOfIds[5], choices=self.contExpDialogGeneralText()["e14"], size=(145, 21))
        self.ODChoice.Bind(wx.EVT_CHOICE, self.analizeSelection)
        sizer.Add(self.ODChoice, pos=(2,2), span=(1,2), flag=wx.EXPAND)

#        self.IDLabel = wx.StaticText(parent, self.listOfIds[6], "ID", size=(150, 21))
#        sizer.Add(self.IDLabel, pos=(3,0), span=(1,2), flag=wx.EXPAND)
#        self.IDChoice = wx.Choice(parent, self.listOfIds[7], choices=["on", "off"], size=(145, 21))
#        self.IDChoice.Bind(wx.EVT_CHOICE, self.analizeSelection)
#        sizer.Add(self.IDChoice, pos=(3,2), span=(1,2), flag=wx.EXPAND)

        self.minimumDiamLabel = wx.StaticText(parent, self.listOfIds[10], self.contExpDialogGeneralText()["e15"], size=(75, 21))
        sizer.Add(self.minimumDiamLabel, pos=(3,0))
        self.minimumDiamValue = NumCtrl(parent, self.listOfIds[11], integerWidth=7, fractionWidth=0,
                                   size=(145, 21), autoSize=False)
        sizer.Add(self.minimumDiamValue, pos=(3,1), span=(1,2), flag=wx.EXPAND)
        self.minimumDiamUnit = wx.Choice(parent, self.listOfIds[12], choices=self.contExpDialogGeneralText()["e14"], size=(75, 21))
        self.minimumDiamUnit.Bind(wx.EVT_CHOICE, self.analizeSelection)
        sizer.Add(self.minimumDiamUnit, pos=(3,3))

        sizer.AddGrowableCol(0)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableCol(2)
        sizer.AddGrowableCol(3)
#        sizer.AddGrowableCol(4)
        parent.SetSizer(sizer)
        parent.Fit()

    def setDisabledWidget(self):
        connection = sqlite3.connect("custom.pype")
        cursor = connection.cursor()
        command = """SELECT rowid, schedule, NPS, OD, ID, minimum_diameter_metric FROM segments ORDER BY rowid DESC LIMIT 1"""
        cursor.execute(command)
        data = cursor.fetchall()
        schedule = data[0][1]
        command = """SELECT pipe_type FROM system WHERE rowid=1"""
        cursor.execute(command)
        pipeType = cursor.fetchall()[0][0]
        data.append(pipeType)
        connection.close()
#        print data

        if schedule != "None":
            #si la cedula fue especificada en el segmento anterior
            self.NPSLabel.Enable(True)
            self.NPSChoice.Enable(True)
            self.ODLabel.Enable(False)
            self.ODChoice.Enable(False)
#            self.IDLabel.Enable(False)
#            self.IDChoice.Enable(False)
            self.minimumDiamLabel.Enable(False)
            self.minimumDiamValue.Enable(False)
            self.minimumDiamUnit.Enable(False)
            pipe_type = self.typeOfPipe(pipeType)
            NPS, OD = self.dataBaseConsult(schedule, pipe_type)

            self.NPSChoice.SetItems(NPS)
            self.ODChoice.SetItems(OD)
#            self.IDChoice.SetItems(ID)

        else:
            #si no fue especificada la cedula se esta trabajando con el diametro minimo
            self.NPSLabel.Enable(False)
            self.NPSChoice.Enable(False)
            self.ODLabel.Enable(False)
            self.ODChoice.Enable(False)
#            self.IDLabel.Enable(False)
#            self.IDChoice.Enable(False)
            self.minimumDiamLabel.Enable(True)
            self.minimumDiamValue.Enable(True)
            self.minimumDiamUnit.Enable(True)

        return data

    def contExpDialogGeneralText(self):
        text = Language()
        return text.contExpDialogGeneralText()

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
        foo = ContExpDialog(None, -1, "window title")
        re = foo.ShowModal()
        if re == wx.ID_OK:
            values = foo.contExpValues
        else:
            values = None

        foo.Destroy()
        print values

if __name__ == "__main__":
    app = wx.App()
    Frame(None, -1, '')
    app.MainLoop()
