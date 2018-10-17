#!/usr/bin/env python

###################################################################################
# LinQinber: Is and open source pipe system design software written in python.    #
#    Copyright (C) 2010 Fidel Sanchez-Bueno                                       #
#    			Fidellira@hotmail.com                                             # 
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
#from wx.lib.masked import NumCtrl
from funct.lang import Language
#import funct.funct as f
from funct.PipeDialog import PipeDialog
from funct.SystemDialog import FirstSystemDialog
from funct.ElbowDialog import ElbowDialog
from funct.ContExpDialog import ContExpDialog
from funct.ValveDialog import ValveDialog
from funct.DataManager import DataManager
from funct.PressureDropDialog import PressureDropDialog
#import wx.lib.inspection

class MainFrame(wx.Frame):
    def __init__(self, parent, id, title):
        self.systemValues = None
        self.accessoryValues = None
        self.systemDialogEndedInOk = wx.NewId()
        self.backgroundColourIsGray = 1
        self.buttonsId = {}
        self.images = [("foo", "bar")]
        self.position = (100, 100)
        self.initPos = self.position
        self.lastPos = (0, 0)
        self.scrolledVirtualSize = (690, 495)
        self.imageDirection = None
        self.listOfDirection = []
        wx.Frame.__init__(self, parent, id, title, size=(800, 570))
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.createMenuBar()
        self.createToolBar()
        self.statusBar = self.createStatusBar()
        self.statusBar.SetStatusText(self.generalText()["a1"])
        self.mainPanel = self.panel()
        self.leftWindow = self.scrolledWindow(self.mainPanel)
        self.rightWindow = self.bareWindow(self.mainPanel)
        
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.leftWindow, 1, wx.EXPAND)
        box.Add(self.rightWindow, 0)
        self.mainPanel.SetSizer(box)
        
        self.Centre()
        wx.EVT_PAINT(self.leftWindow, self.OnDrawing)

    def panel(self):
        """Funcion para crear un panel
        """
        self.panel = wx.Panel(self, id=-1)
        return self.panel

    def scrolledWindow(self, parent):
        """Funcion para crear la ventana con scroll
        """
        self.window = wx.ScrolledWindow(parent, -1, style=wx.SUNKEN_BORDER)
        #self.window.SetScrollbars(1, 1, 1200, 1200)
        self.window.SetVirtualSize((690, 495))
        self.window.SetBackgroundColour("gray")
        self.window.SetScrollRate(10, 10)
        return self.window

    def bareWindow(self, parent):
        """Funcion para crear la barra lateral
        """
        self.window = wx.Window(parent, -1, style=wx.RAISED_BORDER)
        self.panel = wx.Panel(self.window, -1)
        self.window.SetBackgroundColour("dark turquoise")

        sizer = wx.GridSizer(rows=0, cols=2, hgap=3, vgap=3)
        for buttonData in self.rightButtonsData():
            button = self.createButton(self.panel, buttonData)
            sizer.Add(button, 0, 0)
#        BUTTONTEST = wx.Button(self.panel, -1, size=(40, 30))
#        sizer.Add(BUTTONTEST, 0, 0)
        self.panel.SetSizer(sizer)
        self.panel.Fit()
        return self.window

    def createButton(self, parent, buttonData):
        """Funcion para crear los botons de la barra lateral
        """
        buttonId = wx.NewId()
        self.buttonsId[buttonId] = (buttonData[1], buttonData[2])
        self.button = wx.BitmapButton(parent, buttonId, wx.Bitmap(buttonData[0]))
        self.button.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterButton)
        self.button.Bind(wx.EVT_LEAVE_WINDOW, self.OnExitWindow)
        self.button.Bind(wx.EVT_BUTTON, self.OnButtonsClic)
        return self.button

    def OnButtonsClic(self, evt):
        """Funcion que se ejecuta luego de hacer clic en algun boton
        del panel derecho de la ventana principal
        """
        if not self.backgroundColourIsGray:
            button = evt.GetEventObject()
            id = button.GetId()
            accessoryType = self.buttonsId[id][0]
            flag, values = self.accessoryWindow(accessoryType)
#            print values

            if flag == "pipe_horizontal":
            #si el accesorio es una tuberia horizontal
                prevLen = len(self.images)
                image = self.workingImages()[accessoryType][0]
                self.calculatePosition(self.images[-1][0], image)
                self.leftWindow.Refresh()
                evt.Skip()
                postLen = len(self.images)
                if postLen > prevLen:
                    self.accessoryValues = values
                    managedata = DataManager(pipeData=self.accessoryValues)
                    foo = managedata.pipeData
                    for x in foo:
                        print str(x)+" = "+str(foo[x])
                    print "*"*20
                    print "\n"
                    
            elif flag == "pipe_vertical":
                #si el accesorio es una tuberia vertical
                prevLen = len(self.images)
                image = self.workingImages()[accessoryType][0]
                self.calculatePosition(self.images[-1][0], image)
                self.leftWindow.Refresh()
                evt.Skip()
                postLen = len(self.images)

                if postLen > prevLen:
                    self.accessoryValues = values

                    if self.imageDirection == self.generalText()["a26"]:
                        #si la tuberia tiene direccion "Abajo-Arriba"
                        self.accessoryValues["orientation"] = "vertical up"

                    elif self.imageDirection == self.generalText()["a27"]:
                        #si la tuberia tiene direccion "Arriba-Abajo"
                        self.accessoryValues["orientation"] = "vertical down"

                    else:
                        #no deberia cumplirse!!
                        msg = "se cumplio condicion else\nmodulo: OnButtonsClic\nvarible: orientacion de tuberia vertical"
                        raise Exception, msg

                    managedata = DataManager(pipeData=self.accessoryValues)
                    foo = managedata.pipeData
                    for x in foo:
                        print str(x)+" = "+str(foo[x])
                    print "*"*20
                    print "\n"

            elif flag == "accessory":
                #si el accesorio es codo, valvula o contraccion
                prevLen = len(self.images)
                image = self.workingImages()[accessoryType][0]
                self.calculatePosition(self.images[-1][0], image)
                self.leftWindow.Refresh()
                evt.Skip()
                postLen = len(self.images)
                if postLen > prevLen:
                    self.accessoryValues = values
#                    print self.accessoryValues
                    managedata = DataManager(accessoryData=self.accessoryValues)
                    foo = managedata.accessoryData
                    for x in foo:
                        print str(x)+" = "+str(foo[x])
                    print "*"*20
                    print "\n"
            else:
                msg = """se ha hecho clic en un boton que no se ha configurado todavia
                      modulo: OnButtonsClic
                     """
                raise Exception, msg
                #si flag = None (no hay codigo de retorno)
                #no realizar nada
                
#            print self.accessoryValues

    def accessoryWindow(self, accessoryType):
        returnCode = None
        accessoryValues = None

        if self.systemValues["type_of_calculation"] == "losses":
            flag2 = None
        elif self.systemValues["type_of_calculation"] == "diameter":
            flag2 = "True"
        if accessoryType == self.rightButtonsData()[0][1]:
            #si el accesorio es una tuberia horizontal
            if len(self.images) == 1:
                #si la tuberia es la primera en colocarse
                pipeDialog = PipeDialog(None, -1, title="Tuberia", pipeType=self.systemValues["pipe_type"], flag2=flag2)
                re = pipeDialog.ShowModal()
                if re == wx.ID_OK:
                    accessoryValues = pipeDialog.pipeValues
                    accessoryValues["orientation"] = "horizontal"
                    returnCode = "pipe_horizontal"
                else:
                    returnCode = False
                pipeDialog.Destroy()
            else:
                #si ya se han colocado segmentos anteriormente
                pipeDialog = PipeDialog(None, -1, title="Tuberia", pipeType=self.systemValues["pipe_type"], flag="foo", flag2=flag2)
                re = pipeDialog.ShowModal()
                if re == wx.ID_OK:
                    accessoryValues = pipeDialog.pipeValues
                    accessoryValues["orientation"] = "horizontal"
                    returnCode = "pipe_horizontal"
                else:
                    returnCode = False
                pipeDialog.Destroy()

        elif accessoryType == self.rightButtonsData()[1][1]:
            #si el accesorio es una tuberia vertical
            if len(self.images) == 1:
                #si la tuberia es la primera en colocarse
                pipeDialog = PipeDialog(None, -1, title="Tuberia", pipeType=self.systemValues["pipe_type"], flag2=flag2)
                re = pipeDialog.ShowModal()
                if re == wx.ID_OK:
                    accessoryValues = pipeDialog.pipeValues
    #                accessoryValues["orientation"] = "vertical"
                    returnCode = "pipe_vertical"
                else:
                    returnCode = False
                pipeDialog.Destroy()
            else:
                #si ya se han colocado segmentos anteriormente
                pipeDialog = PipeDialog(None, -1, title="Tuberia", pipeType=self.systemValues["pipe_type"], flag="foo", flag2=flag2)
                re = pipeDialog.ShowModal()
                if re == wx.ID_OK:
                    accessoryValues = pipeDialog.pipeValues
    #                accessoryValues["orientation"] = "vertical"
                    returnCode = "pipe_vertical"
                else:
                    returnCode = False
                pipeDialog.Destroy()

        elif (accessoryType == self.rightButtonsData()[2][1] or
              accessoryType == self.rightButtonsData()[3][1] or
              accessoryType == self.rightButtonsData()[4][1] or
              accessoryType == self.rightButtonsData()[5][1]):
            #si el accesorio es un codo de 90 grados
            elbow90Dialog = ElbowDialog(None, -1, "codo de 90 grados")
            re = elbow90Dialog.ShowModal()
            if re == wx.ID_OK:
                accessoryValues = elbow90Dialog.elbowValues
                returnCode = "accessory"
            else:
                returnCode = False
            elbow90Dialog.Destroy()

        elif (accessoryType == self.rightButtonsData()[10][1] or
              accessoryType == self.rightButtonsData()[11][1] or
              accessoryType == self.rightButtonsData()[12][1] or
              accessoryType == self.rightButtonsData()[13][1]):
            #si el accesorio es un codo de 180 grados
            elbow180Dialog = ElbowDialog(None, -1, "codo de 180 grados", flag="180")
            re = elbow180Dialog.ShowModal()
            if re == wx.ID_OK:
                accessoryValues = elbow180Dialog.elbowValues
                returnCode = "accessory"
            else:
                returnCode = False
            elbow180Dialog.Destroy()


        elif (accessoryType == self.rightButtonsData()[8][1] or
              accessoryType == self.rightButtonsData()[9][1]):
            #si el accesorio es una contraccion o una expansion
#            if flag2 == "True":
#                #si se esta diametro minimo no esta habilitado las contracciones/expansiones
#                returnCode, accessoryValues = None, None
#
#            else:
                #si se esta calculando perdidas
#            print self.systemValues["type_of_calculation"]
            if self.systemValues["type_of_calculation"] == "losses":
#                print "here"
                contExpDialog = ContExpDialog(None, -1, "Contraccion/Expansion")
                re = contExpDialog.ShowModal()
                if re == wx.ID_OK:
                    accessoryValues = contExpDialog.contExpValues
                    returnCode = "accessory"
                else:
                    returnCode = False
                contExpDialog.Destroy()
               
        elif (accessoryType == self.rightButtonsData()[6][1] or
              accessoryType == self.rightButtonsData()[7][1]):
            #si el accesorio es una valvula
            valveDialog = ValveDialog(None, -1, "Valvula")
            re = valveDialog.ShowModal()
            if re == wx.ID_OK:
                accessoryValues = valveDialog.valveValues
                returnCode = "accessory"
            else:
                returnCode = False
            valveDialog.Destroy()

        return returnCode, accessoryValues

    def OnEnterButton(self, evt):
        """Funcion para modificar el mensaje en la barra de estado
        cuando el mouse esta encima del area de un boton
        """
        button = evt.GetEventObject()
        id = button.GetId()
        self.statusBar.SetStatusText(self.buttonsId[id][1])
        evt.Skip()

    def OnExitWindow(self, evt):
        """Funcion para modificar el mensaje de la barra de estado
        cuando el mouse sale del area de un boton
        """
        self.statusBar.SetStatusText(self.generalText()["a1"])
        evt.Skip()

    def createToolBar(self):
        """Funcion para crear la barra de herramienta"""
        toolbar = self.CreateToolBar()
        for each in self.toolbarData():
            self.createSimpleTool(toolbar, *each)
        toolbar.Realize()

    def createSimpleTool(self, toolbar, label, filename, help, handler):
        """Funcion llamada por 'createToolbar' para la creacion de la barra
        de herramientas
        """
        if not label:
            toolbar.AddSeparator()
            return
        bmp = wx.Image(filename, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        tool = toolbar.AddSimpleTool(-1, bmp, label, help)
        self.Bind(wx.EVT_MENU, handler, tool)

    def createMenuBar(self):
        """Funcion para crear la barra de menu"""
        menuBar = wx.MenuBar()
        for eachMenu in self.menuData():
            menuLabel = eachMenu[0]
            menuItems = eachMenu[1]
            menuBar.Append(self.createMenu(menuItems), menuLabel)
        self.SetMenuBar(menuBar)

    def createMenu(self, menuItems):
        """Funcion llamada por "createMenuBar" para la creacion de
        la barra de menu
        """
        menu = wx.Menu()
        for eachItem in menuItems:
            if eachItem[0] == "":
                menu.AppendSeparator()
            else:
                menuItem = menu.Append(eachItem[0], eachItem[1], eachItem[2])
                self.Bind(wx.EVT_MENU, eachItem[3],menuItem)
        return menu

    def createStatusBar(self):
        """Funcion para crear la barra de estado
        """
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-1, -4])
        return self.statusbar

    def exitDialog(self):
        """Mensaje que se muestra al intentar cerrar el programa
        """
        dialog = wx.MessageDialog(None, self.generalText()["a2"],
                                  self.generalText()["a3"],
                                  wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        re = dialog.ShowModal()
        if re == wx.ID_YES:
            self.Destroy()

    def OnCloseWindow(self, evt):
        """Funcion para mostrar mensaje de confirmacion al intentar
        cerrar el programa

        """
        self.exitDialog()

    def OnNew(self, evt):
        def systemDialogs(self):
            systemDialog = FirstSystemDialog(None, -1, '')
            retCode = systemDialog.ShowModal()
            if systemDialog.systemValues:
                self.systemValues = systemDialog.systemValues
                managedata = DataManager(self.systemValues)
#                print managedata.systemData
            if systemDialog.endedInOk:
                retCode = self.systemDialogEndedInOk
            systemDialog.Destroy()
            return retCode
            

        if len(self.images) > 1:
            dialog = wx.MessageDialog(None, self.generalText()["a37"],
                                      self.generalText()["a38"],
                                      wx.YES_NO | wx.CANCEL | wx.YES_DEFAULT | wx.ICON_QUESTION)
            re = dialog.ShowModal()

            if re == wx.ID_YES:
                self.OnSave("From On New")
                self.images = [("foo", "bar")]
                self.position = (100, 100)
                self.initPos = self.position
                self.lastPos = (0, 0)
                self.imageDirection = None
                self.listOfDirection = []
                self.leftWindow.SetBackgroundColour("gray")
                self.backgroundColourIsGray = 1
                self.leftWindow.Refresh()

                retCode = systemDialogs(self)
                if retCode == self.systemDialogEndedInOk:
                    self.images = [("foo", "bar")]
                    self.position = (100, 100)
                    self.initPos = self.position
                    self.lastPos = (0, 0)
                    self.imageDirection = None
                    self.listOfDirection = []

                    self.leftWindow.SetBackgroundColour("white")
                    self.backgroundColourIsGray = 0
                    self.leftWindow.Refresh()
                else:
                    pass
                
                
            elif re == wx.ID_NO:
                self.images = [("foo", "bar")]
                self.position = (100, 100)
                self.initPos = self.position
                self.lastPos = (0, 0)
                self.imageDirection = None
                self.listOfDirection = []
                self.leftWindow.SetBackgroundColour("gray")
                self.backgroundColourIsGray = 1
                self.leftWindow.Refresh()

                retCode = systemDialogs(self)
                if retCode == self.systemDialogEndedInOk:
                    self.images = [("foo", "bar")]
                    self.position = (100, 100)
                    self.initPos = self.position
                    self.lastPos = (0, 0)
                    self.imageDirection = None
                    self.listOfDirection = []

                    self.leftWindow.SetBackgroundColour("white")
                    self.backgroundColourIsGray = 0
                    self.leftWindow.Refresh()
                else:
                    pass

            elif re == wx.ID_CANCEL:
                pass

            dialog.Destroy()

        else:
            retCode = systemDialogs(self)
            if retCode == self.systemDialogEndedInOk:
                self.leftWindow.SetBackgroundColour("white")
                self.backgroundColourIsGray = 0
                self.leftWindow.Refresh()
            else:
                pass

    def OnOpen(self, evt): print "On open"
    def OnSave(self, evt):
        if evt == "From On New":
            print "On Save from On New"
        else:
            print "On Save"
    def OnUndo(self, evt): print "on Undo"
    def OnRedo(self, evt): print "Redo"
    def OnRun(self, evt):
        if self.systemValues["type_of_calculation"] == "losses":
            data = DataManager()
            totalLosses, total_dP = data.lossesCalculation()

        elif self.systemValues["type_of_calculation"] == "diameter":
            data = DataManager(sysCalculation="foo")
            if data.dPOutOFBounds:
                min_dP = data.minPressureDrop
                max_dP = data.maxPressureDrop
#                dPDialog = PressureDropDialog()
                dPDialog = PressureDropDialog(None, -1, "window title", min_dP=min_dP, max_dP=max_dP)
                re = dPDialog.ShowModal()
                if re == wx.ID_OK:
                    values = dPDialog.dPValues
#                    print values
                else:
                    values = None
                dPDialog.Destroy()

                if values:
                    sysData = data.fetchSystemValues()
                    total_losses = data.calculateTotalLosses(values["pressure_drop_metric"])
                    data.minDiamCalculation(total_losses, sysData)
#                    oldvalues = data.fetchSystemValues()
#                    oldvalues["pressure_drop"] = values["pressure_drop"]
#                    oldvalues["pressure_drop_unit"] = values["pressure_drop_unit"]
#                    oldvalues["total_losses"] = "None"
#                    diam = data.getDiameter()
#                    col_names = data.fetchSegmentsColNames()
#                    orden_de_segmentos = data.changeDBValues(col_names, diam)
#                    data.lossesCalculation(orden_de_segmentos=orden_de_segmentos, sistema=oldvalues, doPrint="No")
##                    data = DataManager(sysCalculation="foo")
            else:
                pass


    def OnDrawing(self, evt):
        dc = wx.PaintDC(self.leftWindow)
        self.leftWindow.PrepareDC(dc)
        dc.Clear()
        for image in self.images[1:]:
            x = image[1][0]
            y = image[1][1]
            img = wx.Image(image[0], wx.BITMAP_TYPE_ANY)
            bmp = wx.BitmapFromImage(img)
            dc.DrawBitmap(bmp, x, y, True)

    def directionDialog(self, var):
        images = self.workingImages()
        if var == "horizontal":
            choices = [self.generalText()["a25"], self.generalText()["a24"]]
            title = self.generalText()["a31"]
            staticText = self.generalText()["a30"]

        elif var == "vertical":
            choices = [self.generalText()["a26"], self.generalText()["a27"]]
            title = self.generalText()["a31"]
            staticText = self.generalText()["a30"]

        elif (var == images["180BendE"][0] or
              var == images["180BendO"][0]):
            choices = [self.generalText()["a35"], self.generalText()["a36"]]
            title = self.generalText()["a31"]
            staticText = self.generalText()["a32"]

        elif (var == images["180BendN"][0] or
              var == images["180BendS"][0]):
            choices = [self.generalText()["a33"], self.generalText()["a34"]]
            title = self.generalText()["a31"]
            staticText = self.generalText()["a32"]

        dialog = DirectionDialog(self, -1, title, choices, staticText)
        dialog.ShowModal()
        dialog.Destroy()
        return dialog.stringSelected

    def calculatePosition(self, lastImage, newImage):

        images = self.workingImages()

        def foo(newImage, a=0, b=0, c=0, d=0, imageDirection=None):
            imagePos = self.lastPos[0]+a, self.lastPos[1]+b
            self.images.append([newImage, imagePos])
            self.lastPos = (imagePos[0]+c, imagePos[1]+d)

            if imageDirection:
                self.imageDirection = self.generalText()[imageDirection]
                self.listOfDirection.append(self.imageDirection)

        def leftToRightFunction(newImage):
            if newImage == images["pipe_horizontal"][0]:
                foo(newImage, c=100)
                #si la nueva imagen es una tuberia

            elif newImage == images["valve_horizontal"][0]:
                foo(newImage, b=-2, c=14, d=2)

            elif newImage == images["contraction_horizontal"][0]:
                foo(newImage, c=15)
                #si la nueva imagen es una contraccion horizontal

            elif newImage == images["90BendSO"][0]:
                foo(newImage, c=6, d=17, imageDirection="a27")
                #si la nueva imagen es un codo de 90 SO

            elif newImage == images["90BendNO"][0]:
                foo(newImage, b=-7, c=7,imageDirection="a26")
                #si la nueva imagen es un codo de 90 NO

            elif newImage == images["180BendO"][0]:
                direction = self.directionDialog(newImage)
                if direction == self.generalText()["a35"]:
                    foo(newImage, d=13,imageDirection="a24")
                elif direction == self.generalText()["a36"]:
                    foo(newImage, b=-13,imageDirection="a24")

        def rightToLeftFunction(newImage):
            if newImage == images["pipe_horizontal"][0]:
                foo(newImage, a=-100)
                #si la nueva imagen es una tuberia horizontal

            elif newImage == images["valve_horizontal"][0]:
                foo(newImage, a=-14, b=-2, d=2)
                #si la nueva imagen es una valvula horizontal

            elif newImage == images["contraction_horizontal"][0]:
                foo(newImage, a=-15)
                #si la nueva imagen es una contraccion horizontal

            elif newImage == images["90BendSE"][0]:
                foo(newImage, a=-17, d=17,imageDirection="a27")
                #si la nueva imagen es un codo de 90 NO

            elif newImage == images["90BendNE"][0]:
                foo(newImage, a=-17, b=-7,imageDirection="a26")

            elif newImage == images["180BendE"][0]:
                direction = self.directionDialog(newImage)
                if direction == self.generalText()["a35"]:
                    foo(newImage, a=-15, c=15, d=13, imageDirection="a25")
                elif direction == self.generalText()["a36"]:
                    foo(newImage, a=-15, b=-13, c=15, imageDirection="a25")

        def upDownFunction(newImage):
            if newImage == images["pipe_vertical"][0]:
                foo(newImage, d=100)
                #si la nueva imagen es una tuberia vertical

            elif newImage == images["valve_vertical"][0]:
                foo(newImage, d=14)
                #si la nueva imagen es una valvula vertical

            elif newImage == images["contraction_vertical"][0]:
                foo(newImage, d=15)
                #si la nueva imagen es una contraccion vertical

            elif newImage == images["90BendNE"][0]:
                #si la nueva imagen es un codo de 90 NE
                foo(newImage, c=17, d=7,imageDirection="a25")

            elif newImage == images["90BendNO"][0]:
                #si la nueva imagen es un codo de 90 NE
                foo(newImage, a=-7, d=7, imageDirection="a24")

            elif newImage == images["180BendN"][0]:
                direction = self.directionDialog(newImage)
                if direction == self.generalText()["a34"]:
                    foo(newImage, c=13, imageDirection="a26")
                elif direction == self.generalText()["a33"]:
                    foo(newImage, a=-13, imageDirection="a26")

        def downUpFunction(newImage):
            if newImage == images["pipe_vertical"][0]:
                foo(newImage, b=-100)
                #si la nueva imagen es una tuberia vertical

            elif newImage == images["valve_vertical"][0]:
                foo(newImage, b=-14)
                #si la nueva imagen es una valvula vertical

            elif newImage == images["contraction_vertical"][0]:
                foo(newImage, b=-15)
                #si la nueva imagen es una contraccion vertical

            elif newImage == images["90BendSO"][0]:
                foo(newImage, a=-7, b=-17, imageDirection="a24")
                #si la nueva imagen es un codo 90 SO

            elif newImage == images["90BendSE"][0]:
                foo(newImage, b=-17, c=17, d=1, imageDirection="a25")
                #si la nueva imagen es un codo 90 SE

            elif newImage == images["180BendS"][0]:
                direction = self.directionDialog(newImage)
                if direction == self.generalText()["a34"]:
                    foo(newImage, b=-15, c=13, d=15, imageDirection="a27")
                elif direction == self.generalText()["a33"]:
                    foo(newImage, b=-15, a=-13, d=15, imageDirection="a27")

        if len(self.images) == 1:
            if newImage == images["pipe_horizontal"][0]:
                #si la primera imagen es una tuberia horizontal
                direction = self.directionDialog("horizontal")
                if direction == self.generalText()["a24"]:
                    #si la direccion es derecha-izquierda
                    virtualSize = self.leftWindow.GetVirtualSize()
                    imagePos = virtualSize[0]-110, self.initPos[1]
                    self.images.append([newImage,imagePos])
                    self.lastPos = imagePos
                    self.imageDirection = self.generalText()["a24"]
                    self.listOfDirection.append(self.imageDirection)

                elif direction == self.generalText()["a25"]:
                    #si la direccion es izquierda-derecha
                    self.images.append([newImage,self.initPos])
                    self.lastPos = (self.initPos[0]+100, self.initPos[1])
                    self.imageDirection = self.generalText()["a25"]
                    self.listOfDirection.append(self.imageDirection)
                else:
                    pass #aqui se cumple cuando se hace clic en "cancel"
                         #en el dialogo

            elif newImage == images["pipe_vertical"][0]:
                #si la primera imagen es una tuberia vertical
                direction = self.directionDialog("vertical")
                if direction == self.generalText()["a26"]:
                    #si el sentido es abajo-arriba
                    virtualSize = self.leftWindow.GetVirtualSize()
                    imagePos = (self.initPos[0], virtualSize[1]-100)
                    self.images.append([newImage,imagePos])
                    self.lastPos = imagePos
                    self.imageDirection = self.generalText()["a26"]
                    self.listOfDirection.append(self.imageDirection)

                elif direction == self.generalText()["a27"]:
                    #si el sentido es arriba-abajo
                    imagePos = (self.initPos[0], self.initPos[1])
                    self.images.append([newImage,imagePos])
                    self.lastPos = (imagePos[0], imagePos[1]+100)
                    self.imageDirection = self.generalText()["a27"]
                    self.listOfDirection.append(self.imageDirection)
                else:
                    pass #aqui se cumple cuando se hace clic en "cancel"
                         #en el dialogo

            else:
                pass #aqui se cumpliria que la primera imagen no es una tuberia vertical u horizontal
        else:
            if self.imageDirection == self.generalText()["a25"]:
                #si el sentido es izquierda-derecha
                if lastImage == images["pipe_horizontal"][0]:
                    #si la ultima imagen es una tuberia
                    leftToRightFunction(newImage)

                elif lastImage == images["90BendSE"][0]:
                    leftToRightFunction(newImage)

                elif lastImage == images["valve_horizontal"][0]:
                    #si la ultima imagen es una valvula horizontal
                    leftToRightFunction(newImage)

                elif lastImage == images["90BendNE"][0]:
                    #si la ultima imagen es un codo de 90 NE
                    leftToRightFunction(newImage)

                elif lastImage == images["contraction_horizontal"][0]:
                    #si la nueva imagen es una contraccion horizontal
                    leftToRightFunction(newImage)

                elif lastImage == images["180BendE"][0]:
                    #si la nueva imagen es un codo de 180 E
                    leftToRightFunction(newImage)

            elif self.imageDirection == self.generalText()["a24"]:
                #si la direccion es derecha-izquierda
                if lastImage == images["pipe_horizontal"][0]:
                    #si la ultima imagen es un tuberia horizontal
                    rightToLeftFunction(newImage)

                elif lastImage == images["contraction_horizontal"][0]:
                    #si la ultima imagen es una contraccion horizontal
                    rightToLeftFunction(newImage)

                elif lastImage == images["valve_horizontal"][0]:
                    #si la ultima imagen es una valvula horizontal
                    rightToLeftFunction(newImage)

                elif lastImage == images["90BendSO"][0]:
                    #si la ultima imagen es un codo 90 SO
                    rightToLeftFunction(newImage)

                elif lastImage == images["90BendNO"][0]:
                    #si la ultima imagen es un codo 90 NO
                    rightToLeftFunction(newImage)

                elif lastImage == images["180BendO"][0]:
                    #si la ultima imagen es un codo de 180 O
                    rightToLeftFunction(newImage)
                    
            elif self.imageDirection == self.generalText()["a27"]:
                #si el sentido es arriba-abajo
                if lastImage == images["pipe_vertical"][0]:
                    #si la ultima imagen es una tuberia vertical
                    upDownFunction(newImage)

                elif lastImage == images["contraction_vertical"][0]:
                    #si la ultima imagen es una contraccion vertical
                    upDownFunction(newImage)

                elif lastImage == images["valve_vertical"][0]:
                    #si la ultima imagen es una valvula vertical
                    upDownFunction(newImage)

                elif lastImage == images["90BendSE"][0]:
                    #si la ultima imagen es una contraccion vertical
                    upDownFunction(newImage)

                elif lastImage == images["90BendSO"][0]:
                    #si la ultima imagen es un codo 90 SO
                    upDownFunction(newImage)

                elif lastImage == images["180BendS"][0]:
                    upDownFunction(newImage)

            elif self.imageDirection == self.generalText()["a26"]:
                #si el sentido es abajo-arriba
                if lastImage == images["pipe_vertical"][0]:
                    #si la ultima imagen es una tiberua vertical
                    downUpFunction(newImage)

                elif lastImage == images["contraction_vertical"][0]:
                    downUpFunction(newImage)

                elif lastImage == images["valve_vertical"][0]:
                    downUpFunction(newImage)

                elif lastImage == images["90BendNE"][0]:
                    downUpFunction(newImage)

                elif lastImage == images["90BendNO"][0]:
                    downUpFunction(newImage)

                elif lastImage == images["180BendN"][0]:
                    downUpFunction(newImage)
                    
        self.calculateVirtualSize()
#        print self.images[-1], self.listOfDirection[-1]
      
    def calculateVirtualSize(self):
        mostRight = 0
        mostDown = 0
        virtualSize = self.leftWindow.GetVirtualSize()

        if self.lastPos[0] > virtualSize[0]:
            newWidth = virtualSize[0] + (self.lastPos[0] - virtualSize[0]) + 100
        else:
            newWidth = virtualSize[0]

        if self.lastPos[1] > virtualSize[1]:
            newHeight = virtualSize[1] + (self.lastPos[1] - virtualSize[1]) + 100
        else:
            newHeight = virtualSize[1]

        if self.lastPos[0] < 0:
            widthToAppend = abs(self.lastPos[0]) + 50
        else:
            widthToAppend = 0

        if self.lastPos[1] < 0:
            heightToAppend = abs(self.lastPos[1]) + 50
        else:
            heightToAppend = 0

        if widthToAppend or heightToAppend:
            cont = 1
            for image in self.images[1:]:
                imagePos = (image[1][0]+widthToAppend, image[1][1]+heightToAppend)
                self.images[cont][1] = imagePos
                cont += 1
                if imagePos[0] > mostRight:
                    mostRight = imagePos[0]
                if imagePos[1] > mostDown:
                    mostDown = imagePos[1]
            self.lastPos = self.lastPos[0]+widthToAppend, self.lastPos[1]+heightToAppend
            newWidth = mostRight + 100 #+ widthToAppend
            newHeight = mostDown + 100 #+ heightToAppend

        self.leftWindow.SetVirtualSize((newWidth, newHeight))

#-------------------------------------------------------------------------#
#---------------------------------GUI data--------------------------------#
#-------------------------------------------------------------------------#
    def generalText(self):
        text = Language()
        return text.generalText()

    def menuData(self):
        return [("&"+self.generalText()["a14"], (
                    (wx.NewId(), "&"+self.generalText()["a4"], self.generalText()["a5"], self.OnNew),
                    (wx.NewId(), "&"+self.generalText()["a6"], self.generalText()["a7"], self.OnOpen),
                    (wx.NewId(), "&"+self.generalText()["a8"], self.generalText()["a9"], self.OnSave),
                    ("", "", ""),
                    (wx.NewId(), "&"+self.generalText()["a10"], self.generalText()["a11"], self.OnCloseWindow))),
                ("&"+self.generalText()["a15"], (
                           (wx.NewId(), "&"+self.generalText()["a12"], self.generalText()["a13"], self.OnUndo),
                           (wx.NewId(), "&"+self.generalText()["a16"], self.generalText()["a17"], self.OnRedo)))]

    def toolbarData(self):
        return ((self.generalText()["a4"], "img/new.png", self.generalText()["a5"], self.OnNew),
                (self.generalText()["a6"], "img/open.png", self.generalText()["a7"], self.OnOpen),
                (self.generalText()["a8"], "img/save.png", self.generalText()["a9"], self.OnSave),
                ("", "", "", ""),
                (self.generalText()["a12"], "img/undo.png", self.generalText()["a13"], self.OnUndo),
                (self.generalText()["a16"], "img/redo.png", self.generalText()["a17"], self.OnRedo),
                (self.generalText()["a40"], "img/application_go.png", self.generalText()["a39"], self.OnRun),
                ("", "", "", ""),
                (self.generalText()["a10"], "img/exit.png", self.generalText()["a11"], self.OnCloseWindow))

    def rightButtonsData(self):
        return (("img/btnpipehorizontal.png", "pipe_horizontal", self.generalText()["a18"]),
                ("img/btnpipevertical.png", "pipe_vertical", self.generalText()["a19"]),
                ("img/btn90bendSE.png", "90BendSE", self.generalText()["a20"]),
                ("img/btn90bendNO.png", "90BendNO", self.generalText()["a20"]),
                ("img/btn90bendSO.png", "90BendSO", self.generalText()["a20"]),
                ("img/btn90bendNE.png", "90BendNE", self.generalText()["a20"]),
                ("img/btnvalvehorizontal.png", "valve_horizontal", self.generalText()["a21"]),
                ("img/btnvalvevertical.png", "valve_vertical", self.generalText()["a21"]),
                ("img/btncontrhorizontal.png", "contraction_horizontal", self.generalText()["a22"]),
                ("img/btncontrvertical.png", "contraction_vertical", self.generalText()["a22"]),
                ("img/btn180bendE.png", "180BendE", self.generalText()["a23"]),
                ("img/btn180bendN.png", "180BendN", self.generalText()["a23"]),
                ("img/btn180bendO.png", "180BendO", self.generalText()["a23"]),
                ("img/btn180bendS.png", "180BendS", self.generalText()["a23"]))

    def workingImages(self):
        return {self.rightButtonsData()[0][1] : ("img/pipesmallH.png", (100, 10)),
                self.rightButtonsData()[1][1] : ("img/pipesmallV.png", (10, 100)),
                self.rightButtonsData()[2][1] : ("img/bendsmallSE.png", (17, 17)),
                self.rightButtonsData()[3][1] : ("img/bendsmallNO.png", (17, 17)),
                self.rightButtonsData()[4][1] : ("img/bendsmallSO.png", (17, 17)),
                self.rightButtonsData()[5][1] : ("img/bendsmallNE.png", (17, 17)),
                self.rightButtonsData()[6][1] : ("img/valvesmallH.png", (14, 12)),
                self.rightButtonsData()[7][1] : ("img/valvesmallV.png", (14, 12)),
                self.rightButtonsData()[8][1] : ("img/contrsmallH.png", (15, 10)),
                self.rightButtonsData()[9][1] : ("img/contrsmallV.png", (10, 15)),
                self.rightButtonsData()[10][1] : ("img/180bendsmallE.png", (15, 23)),
                self.rightButtonsData()[11][1] : ("img/180bendsmallN.png", (23, 15)),
                self.rightButtonsData()[12][1] : ("img/180bendsmallO.png", (15, 23)),
                self.rightButtonsData()[13][1] : ("img/180bendsmallS.png", (23, 15))
                }

#-------------------------------------------------------------------------#

class DirectionDialog(wx.Dialog):
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
        self.Close()

    def OnNo(self, evt):
        self.Close()

class App(wx.App):
    def OnInit(self):
        frame = MainFrame(None, -1, __appName__)
        frame.Show(True)
        return True


if __name__ == "__main__":
    app = App()
#    wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
    
