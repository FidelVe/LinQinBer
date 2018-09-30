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
from wx.lib.masked import NumCtrl
from lang import Language

ID_DEPTH = 1

class FirstSystemDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        self.endedInOk = False
        self.systemValues = None
        wx.Dialog.__init__(self, parent, id, title, size=(260, 230))
        self.panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)

        choiceList = [self.firstSystemDialogGeneralText()["b2"],
                      self.firstSystemDialogGeneralText()["b3"]]
        self.radioBox = wx.RadioBox(self.panel, -1, self.firstSystemDialogGeneralText()["b4"],
                    (10, 10), (230, 140), choiceList, 1, wx.RA_SPECIFY_COLS)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.cancelButton = wx.Button(self, wx.ID_CANCEL, self.firstSystemDialogGeneralText()["b5"],
                                      size=(70, 30))
        self.nextButton = wx.Button(self, wx.ID_OK, self.firstSystemDialogGeneralText()["b6"], size=(70, 30))
        self.cancelButton.Bind(wx.EVT_BUTTON, self.onCancel)
        self.nextButton.Bind(wx.EVT_BUTTON, self.onNext)

        hbox.Add(self.cancelButton, 1)
        hbox.Add(self.nextButton, 1, wx.LEFT, 5)

        vbox.Add(self.panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)

        self.SetSizer(vbox)
        self.Bind(wx.EVT_CLOSE, self.onCancel)

    def onCancel(self, evt):
        self.EndModal(wx.ID_CANCEL)

    def onNext(self, evt):
        selection = self.radioBox.GetSelection()
        if selection == 1:
            self.Hide()
            dialog = SecondSystemDialog(self, -1)
            secondDialogReturnCode = dialog.ShowModal()
            secondDialogPrevReturnCode = dialog.prevReturnCode
            if secondDialogReturnCode == wx.ID_OK:
                self.systemValues = dialog.systemValues
                self.systemValues["type_of_calculation"] = "losses"
                self.endedInOk = True
            elif secondDialogReturnCode == wx.ID_CANCEL:
                dialog.Destroy()
            elif secondDialogReturnCode == secondDialogPrevReturnCode:
                self.ShowModal()
        elif selection == 0:
            self.Hide()
            dialog = SecondSystemDialog(self, -1, flag="True")
            secondDialogReturnCode = dialog.ShowModal()
            secondDialogPrevReturnCode = dialog.prevReturnCode
            if secondDialogReturnCode == wx.ID_OK:
                self.systemValues = dialog.systemValues
                self.systemValues["type_of_calculation"] = "diameter"
                self.endedInOk = True
            elif secondDialogReturnCode == wx.ID_CANCEL:
                dialog.Destroy()
            elif secondDialogReturnCode == secondDialogPrevReturnCode:
                self.ShowModal()

    def firstSystemDialogGeneralText(self):
        text = Language()
        return text.firstSystemDialogGeneralText()

class SecondSystemDialog(wx.Dialog):
    def __init__(self, parent, id, flag=None):
        #flag es una variable que indica si el calculo es de caida de presion o de diametro
        self.prevReturnCode = None
        self.systemValues = {}
        wx.Dialog.__init__(self, parent, id, self.secondSystemDialogGeneralText()["c1"],
                           size=(460, 350))
        self.panel = wx.Panel(self, -1)

        vbox = wx.BoxSizer(wx.VERTICAL)

        firstList = self.secondSystemDialogGeneralText()["c2"]
        self.radioBox1 = wx.RadioBox(self.panel, -1, self.secondSystemDialogGeneralText()["c3"],
                    (50, 10), (100, 70), firstList, 1, wx.RA_SPECIFY_COLS)
        secondList = self.secondSystemDialogGeneralText()["c4"]
        self.radioBox2 = wx.RadioBox(self.panel, -1, self.secondSystemDialogGeneralText()["c5"],
                                     (300, 10), (100, 70), secondList, 2, wx.RA_SPECIFY_COLS)
    ### flow label value and units
        self.flowLabel = wx.StaticText(self.panel, -1, self.secondSystemDialogGeneralText()["c6"],
                                       pos=(10, 94))
        self.flowValue = NumCtrl(self.panel, -1, pos=(10, 110), integerWidth = 7,
                                 fractionWidth = 2)
        self.flowValue.SetMin(0.01)
        self.flowValue.SetValue(0.01)
        flowUnitList = self.secondSystemDialogGeneralText()["c7"]
        self.flowUnit = wx.Choice(self.panel, -1, (115, 110), choices=flowUnitList)

    ### temperature label value and units
        self.temperatureLabel = wx.StaticText(self.panel, -1, self.secondSystemDialogGeneralText()["c8"],
                                              pos=(10, 140))
        self.temperatureValue = NumCtrl(self.panel, -1, pos=(10, 156), integerWidth = 7,
                                        fractionWidth = 2)#, SetMin=0.01, SetMax=373.94)
        self.temperatureValue.SetMin(0.01)
        self.temperatureValue.SetMax(373.94)
        self.temperatureValue.SetLimitOnFieldChange(True)
        self.temperatureValue.SetValue(0.01)
        temperatureUnitList = self.secondSystemDialogGeneralText()["c9"]
        self.temperatureUnit = wx.Choice(self.panel, -1, (115, 156), choices=temperatureUnitList)
        self.temperatureUnit.Bind(wx.EVT_CHOICE, self.onTemperatureUnitChange)

    ### density label value and units
        self.densityLabel = wx.StaticText(self.panel, -1, self.secondSystemDialogGeneralText()["c10"],
                                          pos=(10, 186))
        self.densityValue = NumCtrl(self.panel, -1, pos=(10, 202), integerWidth = 4,
                                    fractionWidth = 2)
        self.densityValue.SetMin(0.01)
        self.densityValue.SetValue(0.01)
        densityUnitList = self.secondSystemDialogGeneralText()["c11"]
        self.densityUnit = wx.Choice(self.panel, -1, (115, 202), choices=densityUnitList)
        self.densityLabel.Enable(False)
        self.densityUnit.Enable(False)
        self.densityValue.Enable(False)

    ### viscosity label value and units
        self.viscosityLabel = wx.StaticText(self.panel, -1, self.secondSystemDialogGeneralText()["c12"],
                                            pos=(10, 228))
        self.viscosityValue = NumCtrl(self.panel, -1, pos=(10, 244), integerWidth = 3,
                                      fractionWidth = 7)
        self.viscosityValue.SetMin(0.0000001)
        self.viscosityValue.SetValue(0.0000001)
        viscosityUnitList = self.secondSystemDialogGeneralText()["c13"]
        self.viscosityUnit = wx.Choice(self.panel, -1, (115, 244), choices=viscosityUnitList)
        self.viscosityLabel.Enable(False)
        self.viscosityUnit.Enable(False)
        self.viscosityValue.Enable(False)

    ### roughness label value and units
        self.roughnessLabel = wx.StaticText(self.panel, -1, self.secondSystemDialogGeneralText()["c14"],
                                            pos=(260, 94))
        self.roughnessValue = NumCtrl(self.panel, -1, pos=(260, 110), integerWidth = 1,
                                     fractionWidth = 7)
        self.roughnessValue.SetMin(0.0000001)
        self.roughnessValue.SetValue(0.0000001)
        roughnessUnitList = self.secondSystemDialogGeneralText()["c15"]
        self.roughnessUnit = wx.Choice(self.panel, -1, (345, 110), choices=roughnessUnitList)
        self.roughnessLabel.Enable(False)
        self.roughnessUnit.Enable(False)
        self.roughnessValue.Enable(False)

    ### pressure drop label value and units
        self.pressureDropLabel = wx.StaticText(self.panel, -1, self.secondSystemDialogGeneralText()["c23"],
                                    pos=(260, 140))
        self.pressureDropValue = NumCtrl(self.panel, -1, pos=(260, 156), integerWidth = 7,
                                      fractionWidth = 3)
        self.pressureDropValue.SetMin(0.01)
        self.pressureDropValue.SetValue(0.01)
        pressureDropUnitList = self.secondSystemDialogGeneralText()["c24"]
        self.pressureDropUnit = wx.Choice(self.panel, -1, (370, 156), choices=pressureDropUnitList)
        if flag:
            self.pressureDropLabel.Enable(True)
            self.pressureDropUnit.Enable(True)
            self.pressureDropValue.Enable(True)
        else:
            self.pressureDropLabel.Enable(False)
            self.pressureDropUnit.Enable(False)
            self.pressureDropValue.Enable(False)

        self.radioBox1.Bind(wx.EVT_RADIOBOX, self.onRadioBox1)
        self.radioBox2.Bind(wx.EVT_RADIOBOX, self.onRadioBox2)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.prevButton = wx.Button(self, -1, self.secondSystemDialogGeneralText()["c16"], size=(70, 30))
        self.cancelButton = wx.Button(self, -1, self.secondSystemDialogGeneralText()["c17"], size=(70, 30))
        self.nextButton = wx.Button(self, -1, self.secondSystemDialogGeneralText()["c18"], size=(70, 30))
        self.prevButton.Bind(wx.EVT_BUTTON, self.onPrev)
        self.cancelButton.Bind(wx.EVT_BUTTON, self.onCancel)
        self.nextButton.Bind(wx.EVT_BUTTON, self.onNext)

        hbox.Add(self.prevButton, 1 )
        hbox.Add(self.nextButton, 1, wx.LEFT, 5)
        hbox.Add(self.cancelButton, 1, wx.LEFT, 5)

        vbox.Add(self.panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)

        self.SetSizer(vbox)
        self.nextButton.SetDefault() #set the nextButton as default
        self.Bind(wx.EVT_CLOSE, self.onCancel) #bind the window close icon on the top right corner of the window

    def onTemperatureUnitChange(self, evt):
        unitSelected = self.temperatureUnit.GetStringSelection()
        if unitSelected == "F":
            self.temperatureValue.SetMin(32.02)
            self.temperatureValue.SetMax(705.1)
            self.temperatureValue.SetValue(32.02)
        elif unitSelected == "C":
            self.temperatureValue.SetMin(0.01)
            self.temperatureValue.SetMax(373.94)
            self.temperatureValue.SetValue(0.01)
        pass

    def onRadioBox1(self, evt):
        selected = self.radioBox1.GetSelection()
        if selected == 0:
            self.densityLabel.Enable(False)
            self.densityUnit.Enable(False)
            self.densityValue.Enable(False)
            self.viscosityLabel.Enable(False)
            self.viscosityUnit.Enable(False)
            self.viscosityValue.Enable(False)
            self.temperatureLabel.Enable()
            self.temperatureUnit.Enable()
            self.temperatureValue.Enable()
        elif selected == 1:
            self.temperatureLabel.Enable(False)
            self.temperatureUnit.Enable(False)
            self.temperatureValue.Enable(False)
            self.densityLabel.Enable()
            self.densityUnit.Enable()
            self.densityValue.Enable()
            self.viscosityLabel.Enable()
            self.viscosityUnit.Enable()
            self.viscosityValue.Enable()
        else:
            pass

    def onRadioBox2(self, evt):
        selected = self.radioBox2.GetSelection()
        if (selected == 0 or
            selected == 1 or
            selected == 2):
            self.roughnessLabel.Enable(False)
            self.roughnessUnit.Enable(False)
            self.roughnessValue.Enable(False)
        elif selected == 3:
            self.roughnessLabel.Enable()
            self.roughnessUnit.Enable()
            self.roughnessValue.Enable()
        else:
            pass

    def onCancel(self, evt):
        self.EndModal(wx.ID_CANCEL)

    def onPrev(self, evt):
        self.prevReturnCode = wx.NewId()
        self.EndModal(self.prevReturnCode)

    def onNext(self, evt):
        radioBox1Selection = self.radioBox1.GetSelection()
        radioBox2Selection = self.radioBox2.GetSelection()
        okToClose = [False, False, False]

        #begin segmento para la caida de presion
        if self.pressureDropValue.IsEnabled():
            #si el calculo es para diametro minimo
            if self.pressureDropUnit.GetSelection() == -1:
                #si no se ha especificado valor en las unidades de caida de presion
                dialog = wx.MessageDialog(self.panel, self.secondSystemDialogGeneralText()["c25"],
                                          self.secondSystemDialogGeneralText()["c26"],
                                          style=wx.OK | wx.ICON_EXCLAMATION)
                dialog.ShowModal()
                dialog.Destroy()
                okToClose[2] = False
            else:
                self.systemValues["pressure_drop"] = self.pressureDropValue.GetValue()
                self.systemValues["pressure_drop_unit"] = self.pressureDropUnit.GetStringSelection()
                okToClose[2] = True
        #end segmento para la caida de presion

        if radioBox1Selection == 0:
            if (self.flowUnit.GetSelection() == -1 or
                self.temperatureUnit.GetSelection() == -1):
                dialog = wx.MessageDialog(self.panel, self.secondSystemDialogGeneralText()["c19"],
                                          self.secondSystemDialogGeneralText()["c20"],
                                          style=wx.OK | wx.ICON_EXCLAMATION)
                dialog.ShowModal()
                dialog.Destroy()
                okToClose[0] = False
            else:
                self.systemValues["water"] = "yes"
                self.systemValues["flow"] = self.flowValue.GetValue()
                self.systemValues["flow_unit"] = self.flowUnit.GetStringSelection()
                self.systemValues["temperature"] = self.temperatureValue.GetValue()
                self.systemValues["temperature_unit"] = self.temperatureUnit.GetStringSelection()
                okToClose[0] = True

        elif radioBox1Selection == 1:
            if (self.flowUnit.GetSelection() == -1 or
                self.viscosityUnit.GetSelection() == -1 or
                self.densityUnit.GetSelection() == -1):
                dialog = wx.MessageDialog(self.panel, self.secondSystemDialogGeneralText()["c21"],
                                          self.secondSystemDialogGeneralText()["c20"],
                                          style=wx.OK | wx.ICON_EXCLAMATION)
                dialog.ShowModal()
                dialog.Destroy()
                okToClose[0] = False
            else:
                self.systemValues["water"] = "None"
                self.systemValues["flow"] = self.flowValue.GetValue()
                self.systemValues["flow_unit"] = self.flowUnit.GetStringSelection()
                self.systemValues["viscosity"] = self.viscosityValue.GetValue()
                self.systemValues["viscosity_unit"] = self.viscosityUnit.GetStringSelection()
                self.systemValues["density"] = self.densityValue.GetValue()
                self.systemValues["density_unit"] = self.densityUnit.GetStringSelection()
                okToClose[0] = True

        if radioBox2Selection == 0:
            self.systemValues["pipe_type"] = "CSP"
            okToClose[1] = True
        elif radioBox2Selection == 1:
            self.systemValues["pipe_type"] = "SSP"
            okToClose[1] = True
        elif radioBox2Selection == 2:
            self.systemValues["pipe_type"] = "PVC"
            okToClose[1] = True
        elif radioBox2Selection == 3:
            self.systemValues["pipe_type"] = "None"
            if self.roughnessUnit.GetSelection() == -1:
                dialog = wx.MessageDialog(self.panel, self.secondSystemDialogGeneralText()["c22"],
                                          self.secondSystemDialogGeneralText()["c20"],
                                          style=wx.OK | wx.ICON_EXCLAMATION)
                dialog.ShowModal()
                dialog.Destroy()
                okToClose[1] = False
            else:
                self.systemValues["roughness"] = self.roughnessValue.GetValue()
                self.systemValues["roughness_unit"] = self.roughnessUnit.GetStringSelection()
                okToClose[1] = True
                
        if self.pressureDropValue.IsEnabled():
            if okToClose[0] and okToClose[1] and okToClose[2]:
    #            print self.systemValues
                self.EndModal(wx.ID_OK)
        else:
            if okToClose[0] and okToClose[1]:
    #            print self.systemValues
                self.EndModal(wx.ID_OK)

    def secondSystemDialogGeneralText(self):
        text = Language()
        return text.secondSystemDialogGeneralText()
    
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
        foo = FirstSystemDialog(None, -1, 'Change Color Depth')
        foo.ShowModal()
        values = foo.systemValues
        print values

        foo.Destroy()



if __name__ == "__main__":
    app = wx.App()
    Frame(None, -1, '')
    app.MainLoop()
