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

"""This file contains all the string of the application
Este archivo contiene todas las cadenas de texto de la aplicacion"""


class Language():
    def generalText(self):
        """Strings for the main frame
        Cadenas de la ventana principal
        """
        return {"a1" : "Status",
                "a2" : "Esta seguro que desea salir?",
                "a3" : "Salir",
                "a4" : "New",
                "a5" : "New...",
                "a6" : "Open",
                "a7" : "Open...",
                "a8" : "Save",
                "a9" : "Save...",
                "a10" : "Quit",
                "a11" : "Quit...",
                "a12" : "Undo",
                "a13" : "Undo...",
                "a14" : "File",
                "a15" : "Edit",
                "a16" : "Redo",
                "a17" : "Redo...",
                "a18" : "Insert Horizontal pipe",
                "a19" : "Insert Vertical Pipe",
                "a20" : "Insert 90 degree bend",
                "a21" : "Insert valve",
                "a22" : "Insert contraction or expansion",
                "a23" : "Insert 180 degree bend",
                "a24" : "Derecha-Izquierda",
                "a25" : "Izquierda-Derecha",
                "a26" : "Abajo-Arriba",
                "a27" : "Arriba-Abajo",
                "a28" : "Elegir direccion:",
                "a29" : "Direccion",
                "a30" : "Seleccionar sentido del flujo",
                "a31" : "Seleccion",
                "a32" : "",
                "a33" : "Conectar a la derecha",
                "a34" : "Conectar a la izquierda",
                "a35" : "Conectar arriba",
                "a36" : "Conectar abajo",
                "a37" : "Guardar trabajo actual?",
                "a38" : "Nuevo",
                "a39" : "Calcular..",
                "a40" : "Calcular"
                }

    def firstSystemDialogGeneralText(self):
        """Strings of the first dialog for the input of the system values
        cadenas del primer dialogo para la entrada de los valores del sistema
        """
        return {"b1" : "Caudal de operacion",
                "b2" : "Diametro minimo de operacion",
                "b3" : "Caida de presion y perdidas por friccion",
                "b4" : "Seleccione variable a calcular",
                "b5" : "Cancel",
                "b6" : "Next",
                "b7" : None,
                "b8" : None,
                "b9" : None,
                "b10" : None,
                }

    def secondSystemDialogGeneralText(self):
        """Strings of the second dialog for the input of the system values
        cadenas del segundo dialogo para la entrada de los valores del sistema
        """
        return {"c1" : "title",
                "c2" : ["Agua", "Otro"],
                "c3" : "Fluido",
                "c4" : ["CSP", "SSP", "PVC", "Otro"],
                "c5" : "Tuberia",
                "c6" : "Caudal",
                "c7" : ["gal/seg", "gal/min", "l/min", "l/seg", "l/h", "barriles/h", "m3/seg"],
                "c8" : "Temperatura",
                "c9" : ["F", "C"],
                "c10" : "densidad",
                "c11" : ["lb/ft3", "kg/m3"],
                "c12" : "viscosidad",
                "c13" : ["cP", "Pa*seg"],
                "c14" : "Rugosidad",
                "c15" : ["mm", "inch", "ft", "m"],
                "c16" : "Back",
                "c17" : "Cancel",
                "c18" : "Next",
                "c19" : "Debe seleccionar unidades \npara Caudal y temperatura",
                "c20" : "",
                "c21" : "Debe seleccionar unidades \npara Caudal densidad y viscosidad",
                "c22" : "Debe seleccionar unidades \npara la rugosidad",
                "c23" : "Caida de presion",
                "c24" : ["Pa", "atm", "psi", "torr", "bar"],
                "c25" : "Debe seleccionar unidades \npara la caida de presion",
                "c26" : ""
                }

    def pipeDialogGeneralText(self):
        """Strings of the dialog for the input of the pipe values
        cadenas del dialogo para la entrada de los valores del tuberia
        """
        return {"d1" : "CSP",
                "d2" : ("STD", "XS", "DXS", "10", "20", "30", "40",
                        "60", "80", "100", "140", "160"),
                "d3" : "SSP",
                "d4" : ("05", "10", "40", "80"),
                "d5" : "PVC",
                "d6" : ("40", "80", "120"),
                "d7" : " (inch)",
                "d8" : " (mm)",
                "d9" : ["Usar cedula", "Usar diametro minimo"],
                "d10" : "Seleccionar",
                "d11" : ["NPS", "OD", "ID"],
                "d12" : "Ok",
                "d13" : "Close",
                "d14" : "se cumplio condicion else \nmodulo: typeOfPipe\nvariable: pipeTypeAcron",
                "d15" : "Debe seleccionar unidades \npara la Longitud",
                "d16" : "Dialog title",
                "d17" : "Debe seleccionar unidades \npara  el Diametro minimo",
                "d18" : "Debe seleccionar un valor\npara la cedula de la tuberia",
                "d19" : "Debe seleccionar un valor\npara el NPS",
                "d20" : "Debe seleccionar un valor\npara el OD",
                "d21" : "Debe seleccionar un valor\npara el ID",
                "d22" : "Schedule",
                "d23" : "NPS",
                "d24" : "OD",
                "d25" : "ID",
                "d26" : "Min diameter",
                "d27" : "Lenght",
                "d28" : ["mm", "inch", "ft", "m"],
                "d29" : None,
                }
    def elbowDialogGeneralText(self):
        """Strings of the dialog for the input of the 90 degree elbow values
        cadenas del dialogo para la entrada de los valores de codos de 90 grados
        """
        return {"e1" : ["codo de 90 standar", "codo de 90 soldado"],
                "e2" : "Elegir tipo de codo",
                "e3" : "Ok",
                "e4" : "Close",
                "e5" : "Radio (mm)",
                "e6" : ["codo de 180 standar", "codo de 180 soldado"]
                }

    def valveDialogGeneralText(self):
        """Strings of the dialog for the input of the 90 degree elbow values
        cadenas del dialogo para la entrada de los valores de codos de 90 grados
        """
        return {"e1" : ["codo de 90 standar", "codo de 90 soldado"],
                "e2" : "Elegir tipo de codo",
                "e3" : "Ok",
                "e4" : "Close",
                "e5" : "Radio (mm)",
                "e6" : ["codo de 180 standar", "codo de 180 soldado"],
                "e7" : "Seleccione el tipo de valvula:",
                "e8" : ["globo (tipo A)", "globo (tipo B)", "retencion de obturador ascendente (tipo A)",
                        "retencion de obturador ascendente (tipo B)", "compuerta", "retencion y cierre (tipo A)",
                        "retencion y cierre (tipo B)", "retencion y cierre (tipo C)", "bola o esfera"],
                "e9" : "Debe seleccionar un tipo de valvula",
                "e10" : "Error"
                }

    def dPDialogGeneralText(self):
        """Strings of the dialog to change the pressure drop
        cadenas del dialogo para el cambio de la caida de presion
        """
        return {"f1" : "Enter a new value for the pressure drop\n\n Note: Value of pressure Drop must be\nbetween this range",
                "f2" : ["Pa", "atm", "psi", "torr", "bar"],
                "f3" : "Ok",
                "f4" : "Close",
                "f5" : "dP",
                "f6" : "Value of pressure Drop must be\nbetween this range",
                "f7" : ""
                }
    def contExpDialogGeneralText(self):
        """Strings of the dialog for the input of the 90 degree elbow values
        cadenas del dialogo para la entrada de los valores de codos de 90 grados
        """
        return {"e1" : ["expansion", "contraccion"],
                "e2" : "Seleccionar",
                "e3" : "Ok",
                "e4" : "Close",
                "e5" : "El valor de NPS elegido\ndebe ser mayor a",
                "e6" : "Error",
                "e7" : "El valor de NPS elegido\ndebe ser menor a",
                "e8" : "El valor de OD elegido\ndebe ser mayor a",
                "e9" : "El valor de OD elegido\ndebe ser menor a",
                "e10" : "El valor de diametro elegido\ndebe ser mayor a",
                "e11" : "El valor de diametro elegido\ndebe ser menor a",
                "e12" : "      Seleccionar diametro\n          de salida para la\n      contraccion/expansion",
                "e13" : "Usar",
                "e14" : ["mm", "inch", "ft", "m"],
                "e15" : "Diametro Min",
                "e16" : None

                }
                
if __name__ == "__main__":
    """This file contains all the string of the application
Este archivo contiene todas las cadenas de texto de la aplicacion"""