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
from wx.lib.masked import NumCtrl
from lang import Language

ID_DEPTH = 1

class PipeDialog(wx.Dialog):
    def __init__(self, parent, id, title="window title", pipeType="CSP", flag=None, flag2=None):
        #flag es una variable que indica si la tuberia es la primera tuberia que se coloca
        #o no es la primera
        #en caso de ser la primera la ventana muestra todas las opciones (cedula, NPS, OD, etc)
        #en caso de no ser la primera la ventana solo muestra la opcion de longitud
        #flag2 es una variable que indica si el tipo de calculo es para diametro o para caida de presion
        #en caso de que sea para caida de presion solo se trabaja con diametro minimo
        self.flag2 = flag2
        self.flag = flag
        self.database = "funct/database.pype"
        self.pipeValues = {}
        self.pipeTypeAcron = pipeType
        self.pipeType = self.typeOfPipe(self.pipeTypeAcron)
        self.listOfSchedules = {self.pipeDialogGeneralText()["d1"] : self.pipeDialogGeneralText()["d2"],
                                self.pipeDialogGeneralText()["d3"] : self.pipeDialogGeneralText()["d4"],
                                self.pipeDialogGeneralText()["d5"] : self.pipeDialogGeneralText()["d6"],
                                "None" : "None"}
        self.widgetsIds = None
        if self.pipeTypeAcron == self.pipeDialogGeneralText()["d5"]:
            self.unit = self.pipeDialogGeneralText()["d7"]
        else:
            self.unit = self.pipeDialogGeneralText()["d8"]
        wx.Dialog.__init__(self, parent, id, title, size=(300, 320))
        self.firstPanel = wx.Panel(self, -1)
        self.secondPanel = wx.Panel(self, -1, style=wx.SUNKEN_BORDER)#self.scrolledWindow(self)
        mainBox = wx.BoxSizer(wx.VERTICAL)

        self.radioBoxId = wx.NewId()
        self.radioBox2Id = wx.NewId()
        radioBoxList = self.pipeDialogGeneralText()["d9"]
        self.radioBox = wx.RadioBox(self.firstPanel, self.radioBoxId, self.pipeDialogGeneralText()["d10"],
                    (5, 5), (130, 65), radioBoxList, 1, wx.RA_SPECIFY_COLS)
        radioBoxList2 = self.pipeDialogGeneralText()["d11"]
        self.radioBox2 = wx.RadioBox(self.firstPanel, self.radioBox2Id, self.pipeDialogGeneralText()["d10"],
                    (175, 5), (115, 65), radioBoxList2, 2, wx.RA_SPECIFY_COLS)

        self.setPanelWidgets(self.secondPanel, self.dataWidgets())

        self.thirdPanel = wx.Panel(self, -1)
        self.okButton = wx.Button(self.thirdPanel, wx.ID_OK, self.pipeDialogGeneralText()["d12"],
                                  size=(70, 30), pos=(220, 2))
        self.closeButton = wx.Button(self.thirdPanel, wx.ID_CANCEL, self.pipeDialogGeneralText()["d13"],
                                     size=(70, 30), pos=(145, 2))

        mainBox.Add(self.firstPanel, 2, wx.EXPAND)
        mainBox.Add(self.secondPanel, 5, wx.EXPAND)
        mainBox.Add(self.thirdPanel, 1, wx.EXPAND)

        self.radioBox.Bind(wx.EVT_RADIOBOX, self.onAny)
        self.radioBox2.Bind(wx.EVT_RADIOBOX, self.onAny)
        self.SetSizer(mainBox)

        self.okButton.Bind(wx.EVT_BUTTON, self.onOkButton)
        self.closeButton.Bind(wx.EVT_BUTTON, self.onClose)
        self.okButton.SetDefault()
        self.Centre()
        self.setDisabledInitWidget(flag)

    def setDisabledInitWidget(self, flag):
        if not self.flag2:
            #si se va a calcular caida de presion y perdidas
            if not flag:
                #si la tuberia es la primera que se coloca en el sistema
                #flag == None (if NOT flag)
                NPSPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[1][0]]["panel"])
                ODPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[2][0]]["panel"])
                IDPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[3][0]]["panel"])
                if self.pipeType != "None":
                    MinDiamPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[4][0]]["panel"])
                    NPSPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[1][0]]["panel"])
                    ODPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[2][0]]["panel"])
                    IDPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[3][0]]["panel"])
                    MinDiamPanel.Enable(False)
                    NPSPanel.Enable(False)
                    ODPanel.Enable(False)
                    IDPanel.Enable(False)
                else:
                    schedulePanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[0][0]]["panel"])
                    NPSPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[1][0]]["panel"])
                    ODPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[2][0]]["panel"])
                    IDPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[3][0]]["panel"])
                    NPSPanel.Enable(False)
                    ODPanel.Enable(False)
                    IDPanel.Enable(False)
                    schedulePanel.Enable(False)
                    self.radioBox.Enable(False)
                    self.radioBox2.Enable(False)
            else:
                schedulePanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[0][0]]["panel"])
                NPSPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[1][0]]["panel"])
                ODPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[2][0]]["panel"])
                IDPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[3][0]]["panel"])
                MinDiamPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[4][0]]["panel"])
                MinDiamPanel.Enable(False)
                NPSPanel.Enable(False)
                ODPanel.Enable(False)
                IDPanel.Enable(False)
                schedulePanel.Enable(False)
                self.radioBox.Enable(False)
                self.radioBox2.Enable(False)

        else:
            #si se va a calcular diametro minimo
            if not flag:
                #si la tuberia es la primera que se coloca en el sistema
                #flag == None (if NOT flag)
                NPSPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[1][0]]["panel"])
                ODPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[2][0]]["panel"])
                IDPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[3][0]]["panel"])
                schedulePanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[0][0]]["panel"])
                NPSPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[1][0]]["panel"])
                ODPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[2][0]]["panel"])
                IDPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[3][0]]["panel"])
                NPSPanel.Enable(False)
                ODPanel.Enable(False)
                IDPanel.Enable(False)
                schedulePanel.Enable(False)
                self.radioBox.Enable(False)
                self.radioBox2.Enable(False)
            else:
                schedulePanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[0][0]]["panel"])
                NPSPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[1][0]]["panel"])
                ODPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[2][0]]["panel"])
                IDPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[3][0]]["panel"])
                MinDiamPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[4][0]]["panel"])
                MinDiamPanel.Enable(False)
                NPSPanel.Enable(False)
                ODPanel.Enable(False)
                IDPanel.Enable(False)
                schedulePanel.Enable(False)
                self.radioBox.Enable(False)
                self.radioBox2.Enable(False)

    def typeOfPipe(self, pipeTypeAcron):
        if pipeTypeAcron == self.pipeDialogGeneralText()["d1"]:
            pipeType = "Commercial_Steel_Pipe_c"
        elif pipeTypeAcron == self.pipeDialogGeneralText()["d3"]:
            pipeType = "Stainless_Steel_Pipe_c"
        elif pipeTypeAcron == self.pipeDialogGeneralText()["d5"]:
            pipeType = "PVC_Pipe_c"
        else:
            pipeType = "None"
#            msg = self.pipeDialogGeneralText()["d14"]
#            raise Exception, msg
        return pipeType

    def dataBaseConsult(self, sched):
        if (sched == "STD" or
            sched == "XS" or
            sched == "DXS"):
            typeOfPipe = self.pipeType[:-1]
        else:
            typeOfPipe = self.pipeType
        ID = []
        OD = []
        NPS = []
        flag = 0
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        sqlcommand = """SELECT Nominal_Pipe_size, Outside_Diameter, Inside_Diameter FROM %s""" % typeOfPipe+sched
        cursor.execute(sqlcommand)
        system_data = cursor.fetchall()
        connection.close()

        for value in system_data:
            if flag:
                NPS.append(str(value[0]))
                OD.append(str(value[1]))
                ID.append(str(value[2]))
            else:
                flag += 1

        return NPS, OD, ID
#        print system_data

    def onClose(self, evt):
        self.Destroy()

    def onOkButton(self, evt):
        okToClose = False #variable que sirve como flag para decidir
                          #si los valores se han seleccionado correctamente
        dataWidgets = self.dataWidgets()
        scheduleValue = self.secondPanel.FindWindowById(self.widgetsIds[dataWidgets[0][0]]["units"])
        NPSValue = self.secondPanel.FindWindowById(self.widgetsIds[dataWidgets[1][0]]["units"])
        ODValue = self.secondPanel.FindWindowById(self.widgetsIds[dataWidgets[2][0]]["units"])
        IDValue = self.secondPanel.FindWindowById(self.widgetsIds[dataWidgets[3][0]]["units"])
        minDiamValue = self.secondPanel.FindWindowById(self.widgetsIds[dataWidgets[4][0]]["value"])
        minDiamUnit = self.secondPanel.FindWindowById(self.widgetsIds[dataWidgets[4][0]]["units"])
        lenghtValue = self.secondPanel.FindWindowById(self.widgetsIds[dataWidgets[5][0]]["value"])
        lenghtUnit = self.secondPanel.FindWindowById(self.widgetsIds[dataWidgets[5][0]]["units"])

        if self.flag:
            #si la tuberia no es la primera en colocarse en el sistema
            if lenghtUnit.GetSelection() == -1:
                dialog = wx.MessageDialog(self, self.pipeDialogGeneralText()["d15"],
                                          self.pipeDialogGeneralText()["d16"], style=wx.OK | wx.ICON_EXCLAMATION)
                dialog.ShowModal()
                dialog.Destroy()
                okToClose = False

            else: #si existe un valor seleccionado para las unidades de la longitud
                self.pipeValues["length"] = lenghtValue.GetValue()
                self.pipeValues["length_unit"] = lenghtUnit.GetStringSelection()
                okToClose = True


        else:
            #si la tuberia es la primera en colocarse en el sistema
            if lenghtUnit.GetSelection() == -1:
                dialog = wx.MessageDialog(self, self.pipeDialogGeneralText()["d15"],
                                          self.pipeDialogGeneralText()["d16"], style=wx.OK | wx.ICON_EXCLAMATION)
                dialog.ShowModal()
                dialog.Destroy()
                okToClose = False

            else: #si existe un valor seleccionado para las unidades de la longitud
                self.pipeValues["length"] = lenghtValue.GetValue()
                self.pipeValues["length_unit"] = lenghtUnit.GetStringSelection()

                if minDiamUnit.IsEnabled(): #si esta activa la casilla para diametro minimo
                    if minDiamUnit.GetSelection() == -1:
                        dialog = wx.MessageDialog(self, self.pipeDialogGeneralText()["d17"],
                                                  self.pipeDialogGeneralText()["d16"], style=wx.OK | wx.ICON_EXCLAMATION)
                        dialog.ShowModal()
                        dialog.Destroy()
                        okToClose = False
                    else: #si existe un valor seleccionado para las unidades del diametro minimo
                        self.pipeValues["minimum_diameter"] = minDiamValue.GetValue()
                        self.pipeValues["minimum_diameter_unit"] = minDiamUnit.GetStringSelection()
                        self.pipeValues["schedule"] = "None"
                        okToClose = True

                else: #si esta activada la casilla para seleccionar cedula
                    if scheduleValue.GetSelection() == -1:
                        dialog = wx.MessageDialog(self, self.pipeDialogGeneralText()["d18"],
                                                  self.pipeDialogGeneralText()["d16"], style=wx.OK | wx.ICON_EXCLAMATION)
                        dialog.ShowModal()
                        dialog.Destroy()
                        okToClose = False
                    else: #si existe un valor seleccionado para la cedula
                        self.pipeValues["schedule"] = scheduleValue.GetStringSelection()
                        self.pipeValues["minimum_diameter"] = "None"
                        self.pipeValues["minimum_diameter_unit"] = "None"
                        NPSwidget = NPSValue.IsEnabled()
                        ODwidget = ODValue.IsEnabled()
                        IDwidget = IDValue.IsEnabled()

                        if NPSwidget: #si se ha seleccionado NPS
                            if NPSValue.GetSelection() == -1:
                                dialog = wx.MessageDialog(self, self.pipeDialogGeneralText()["d19"],
                                                         self.pipeDialogGeneralText()["d16"],
                                                         style=wx.OK | wx.ICON_EXCLAMATION)
                                dialog.ShowModal()
                                dialog.Destroy()
                                okToClose = False
                            else: #si se ha seleccionado un valor en la casilla para el NPS
                                self.pipeValues["NPS"] = NPSValue.GetStringSelection()
                                okToClose = True

                        elif ODwidget: #si se ha seleccionado OD
                            if ODValue.GetSelection() == -1:
                                dialog = wx.MessageDialog(self, self.pipeDialogGeneralText()["d20"],
                                                         self.pipeDialogGeneralText()["d16"],
                                                         style=wx.OK | wx.ICON_EXCLAMATION)
                                dialog.ShowModal()
                                dialog.Destroy()
                                okToClose = False
                            else: #si se ha seleccionado un valor en la casilla para OD
                                self.pipeValues["OD"] = ODValue.GetStringSelection()
                                okToClose = True

                        elif IDwidget: #si se ha seleccionado ID
                            if IDValue.GetSelection() == -1:
                                dialog = wx.MessageDialog(self, self.pipeDialogGeneralText()["d21"],
                                                         self.pipeDialogGeneralText()["d16"],
                                                         style=wx.OK | wx.ICON_EXCLAMATION)
                                dialog.ShowModal()
                                dialog.Destroy()
                                okToClose = False
                            else: #si se ha seleccionado un valor en la casilla para ID
                                self.pipeValues["ID"] = IDValue.GetStringSelection()
                                okToClose = True

                        else: #colocar un mensaje de error aqui en caso de que se cumpla
                              #aunque debido a la manera en que se ha planteado la logica
                              #no deberia de darse nunca el caso de "else"
                            msg = self.pipeDialogGeneralText()["d14"]
                            raise Exception, msg

        if  okToClose:
            self.pipeValues["type"] = "pipe"
            self.pipeValues["pipe_type"] = self.pipeTypeAcron
            self.EndModal(wx.ID_OK)

    def onAny(self, evt):
        """Funcion unica que sera llamada si cualquier evento de la ventana es ejecutado
        (EVT_RADIOBOX, EVT_CHOICE)
        """
        widget = evt.GetEventObject()
        widgetId = widget.GetId()

        scheduleChoice = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[0][0]]["units"])
        scheduleChoiceId = self.widgetsIds[self.dataWidgets()[0][0]]["units"]
        SchedulePanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[0][0]]["panel"])
        MinDiamPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[4][0]]["panel"])
        NPSPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[1][0]]["panel"])
        NPSChoice = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[1][0]]["units"])
        ODPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[2][0]]["panel"])
        ODChoice = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[2][0]]["units"])
        IDPanel = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[3][0]]["panel"])
        IDChoice = self.secondPanel.FindWindowById(self.widgetsIds[self.dataWidgets()[3][0]]["units"])

        radioBoxSelection = self.radioBox.GetSelection()
        radioBox2Selection = self.radioBox2.GetSelection()
        scheduleSelection = scheduleChoice.GetStringSelection()

        if (widgetId == self.radioBoxId or
            widgetId == self.radioBox2Id):
            radioBoxSelection = self.radioBox.GetSelection()
            radioBox2Selection = self.radioBox2.GetSelection()

            if radioBoxSelection == 1:
                SchedulePanel.Enable(False)
                NPSPanel.Enable(False)
                ODPanel.Enable(False)
                IDPanel.Enable(False)
                self.radioBox2.Enable(False)
                MinDiamPanel.Enable(True)

            elif radioBoxSelection == 0:
                SchedulePanel.Enable(True)
                self.radioBox2.Enable(True)
                MinDiamPanel.Enable(False)

                if radioBox2Selection == 0:
                    NPSPanel.Enable(True)
                    ODPanel.Enable(False)
                    IDPanel.Enable(False)

                elif radioBox2Selection == 1:
                    NPSPanel.Enable(False)
                    ODPanel.Enable(True)
                    IDPanel.Enable(False)

                elif radioBox2Selection == 2:
                    NPSPanel.Enable(False)
                    ODPanel.Enable(False)
                    IDPanel.Enable(True)

        elif widgetId == scheduleChoiceId:
            NPS, OD, ID = self.dataBaseConsult(scheduleSelection)
            NPSChoice.SetItems(NPS)
            ODChoice.SetItems(OD)
            IDChoice.SetItems(ID)

            if radioBox2Selection == 0:
                NPSPanel.Enable(True)
                ODPanel.Enable(False)
                IDPanel.Enable(False)
            elif radioBox2Selection == 1:
                NPSPanel.Enable(False)
                ODPanel.Enable(True)
                IDPanel.Enable(False)
            elif radioBox2Selection == 2:
                NPSPanel.Enable(False)
                ODPanel.Enable(False)
                IDPanel.Enable(True)

    def setPanelWidgets(self, parent, list):
        listOfIds = {}
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        for values in list:
            ids = []
            if len(values) > 2:
                for x in range(4):
                    id = wx.NewId()
                    ids.append(id)
                panel = wx.Panel(parent, ids[0])
                sizer = wx.BoxSizer(wx.HORIZONTAL)
                label = wx.StaticText(panel, ids[1], values[0])
                value = NumCtrl(panel, ids[2], integerWidth=values[1][0], fractionWidth=values[1][1])
                units = wx.Choice(panel, ids[3], choices=values[2])
                units.Bind(wx.EVT_CHOICE, self.onAny)
                sizer.Add(label, 1, flag=wx.ALL | wx.ALIGN_RIGHT, border=2)
                sizer.Add(value, 2, flag=wx.ALL | wx.ALIGN_LEFT, border=2)
                sizer.Add(units, 1, flag=wx.ALL, border=2)
                listOfIds[values[0]] = {"panel" : ids[0], "label" : ids[1],
                                        "value" : ids[2], "units" : ids[3]}
            else:
                for x in range(3):
                    id = wx.NewId()
                    ids.append(id)
                panel = wx.Panel(parent, ids[0])
                sizer = wx.BoxSizer(wx.HORIZONTAL)
                label = wx.StaticText(panel, ids[1], values[0])
                units = wx.Choice(panel, ids[2], choices=values[1])
                units.Bind(wx.EVT_CHOICE, self.onAny)
                sizer.Add(label, 1, flag=wx.ALL | wx.ALIGN_LEFT, border=2)
                sizer.Add(units, 1, flag=wx.ALL, border=2)
                listOfIds[values[0]] = {"panel" : ids[0], "label" : ids[1],
                                        "units" : ids[2]}
            panel.SetSizer(sizer)
            panel.Fit()
            mainSizer.Add(panel, 1, wx.EXPAND)

        parent.SetSizer(mainSizer)
        parent.Fit()
        self.widgetsIds = listOfIds

    def dataWidgets(self):
        return ((self.pipeDialogGeneralText()["d22"], self.listOfSchedules[self.pipeTypeAcron]),
                (self.pipeDialogGeneralText()["d23"]+self.pipeDialogGeneralText()["d7"], ("")),
                (self.pipeDialogGeneralText()["d24"]+self.unit, ("")),
                (self.pipeDialogGeneralText()["d25"]+self.unit, ("")),
                (self.pipeDialogGeneralText()["d26"], (7, 5), self.pipeDialogGeneralText()["d28"]),
                (self.pipeDialogGeneralText()["d27"], (7, 2), self.pipeDialogGeneralText()["d28"])
                )

    def pipeDialogGeneralText(self):
        text = Language()
        return text.pipeDialogGeneralText()

        
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
        foo = PipeDialog(None, -1)
        re = foo.ShowModal()
        if re == wx.ID_OK:
            values = foo.pipeValues
        else:
            values = None
        
        foo.Destroy()
        print values

if __name__ == "__main__":
    app = wx.App()
    Frame(None, -1, '')
    app.MainLoop()
