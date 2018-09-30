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

"""Este modulo contiene todas las funciones usadas por la aplicacion"""

import sqlite3
import os

from math import sin, radians, pi, log, log10, sqrt


databaseName = "funct/database.pype"    #nombre de la base de datos
gravity = 9.8                      #aceleracion de la gravedad (m/seg2)

###############################################################################################
###Funciones generales

def CreateCustomDB(flag=False):
    """Funcion para crear base de datos "custom" la cual tendra la
    informacion de el sistema de tuberia
    """
    if not flag:
        database = "custom.pype"
    else:
        database = flag

    try:
        os.remove(database)
    except:
        pass
    else:
        pass

    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    system_table = """CREATE TABLE system (flow REAL, flow_unit TEXT, flow_metric REAL, fluid_name TEXT,
                                           temperature REAL, temperature_unit TEXT, viscosity REAL,
                                           viscosity_unit REAL,  viscosity_metric REAL, density REAL, density_unit REAL,
                                           density_metric REAL, total_losses REAL, total_losses_metric REAL,
                                           total_losses_unit REAL, pressure_drop REAL, pressure_drop_metric REAL,
                                           pressure_drop_unit REAL, water TEXT, schedule TEXT, pipe_type TEXT,
                                           roughness REAL, roughness_unit TEXT, roughness_metric REAL,
                                           type_of_calculation TEXT
                                           )
                   """
    cursor.execute(system_table)
    connection.commit()

    segments_table = """CREATE TABLE segments (height REAL, name TEXT, type TEXT, pipe_type TEXT, NPS REAL, OD REAL, ID REAL, WT REAL,
                                               minimum_diameter REAL, minimum_diameter_unit TEXT, losses REAL, minimum_diameter_metric REAL,
                                               losses_unit TEXT, losses_metric REAL, pressure_drop REAL, pressure_drop_unit TEXT,
                                               pressure_drop_metric REAL, schedule TEXT, minimum_velocity REAL,
                                               minimum_velocity_unit TEXT, minimum_velocity_metric REAL, friction_factor REAL,
                                               reynolds REAL, orientation TEXT, connected_from TEXT, connected_to TEXT,
                                               roughness REAL, roughness_unit TEXT, roughness_metric REAL, length REAL,
                                               length_unit TEXT, Length_metric REAL, class TEXT, D_2 REAL, D_2_type TEXT,
                                               k_factor REAL, cv REAL, radius REAL, turbulent_friccion_factor REAL)
                     """
    cursor.execute(segments_table)
    connection.commit()
    connection.close()

def InsertSystemValues(system, flag=False):
    """funcion para insertar los datos del sistema en la base de datos "custom"
    en la tabla "system"

    """
    if not flag:
        database = "custom.pype"
    else:
        database = flag

    #si el usuario ingresa el tipo de tuberia, la rugosidad absoluta de la misma
    #se obtiene automaticamente
    #si el usuario no agrega el tipo de tuberia, debe agregar obligatoriamente
    #el valor de la rugosidad absoluta

    if system["flow"] != "None":  #si el caudal es especificado
        system["flow_metric"] = FlowConvert(Q=system["flow"], unitin=system["flow_unit"], unitout="m3/seg")

    if system["water"] != "None":  #si el flujo es agua
        #en caso de que sea agua, las propiedades son sacadas de la base de datos
        system["fluid_name"] = "water"
        temperature_celsius = TemperatureConvert(temp=system["temperature"], unitin=system["temperature_unit"],
                                                   unitout="C")
        water_properties = WaterProperties(temperature_celsius)
        system["density_metric"] = water_properties["Density"][0]
        system["density"] = system["density_metric"]
        system["density_unit"] = water_properties["Density"][1]
        system["viscosity_metric"] = water_properties["Viscosity"][0]
        system["viscosity"] = system["viscosity_metric"]
        system["viscosity_unit"] = water_properties["Viscosity"][1]
    else:                #si el flujo no es agua
        #en caso de que no sea agua, la densidad y viscosidad son valores especificados
        system["density_metric"] = DensityConvert(x=system["density"], unitin=system["density_unit"],
                                                    unitout="kg/m3")
        system["viscosity_metric"] = ViscosityConv(x=system["viscosity"], unitin=system["viscosity_unit"],
                                                     unitout="Pa*seg")


    if system["total_losses"] != "None":  #si las perdidas son especificadas
        system["total_losses_metric"] = DistanceConvert(x=system["total_losses"], unitin=system["total_losses_unit"],
                                                          unitout="m")
        system["pressure_drop_metric"] = PressureLossesConvert(ro=system["density_metric"],
                                                                 ht=system["total_losses_metric"])
        system["pressure_drop"] = system["pressure_drop_metric"]
        system["pressure_drop_unit"] = "Pa"

    elif system["pressure_drop"] != "None":   #si la caida de presion es especificada
        system["pressure_drop_metric"] = PressureConvert(x=system["pressure_drop"], unitin=system["pressure_drop_unit"],
                                                           unitout="Pa")
        system["total_losses_metric"] = PressureLossesConvert(ro=system["density_metric"],
                                                                 dP=system["pressure_drop_metric"])
        system["total_losses"] = system["total_losses_metric"]
        system["total_losses_unit"] = "m"

    if system["pipe_type"] != "None": #si el tipo de tuberia es especificado
        if (system["pipe_type"] == "PVC" or system["pipe_type"] == "SSP"):
            system["roughness_metric"] = 0.00005

        elif system["pipe_type"] == "CSP":
            system["roughness_metric"] = 0.000045
    else: #en caso de que no se especifique el tipo de tuberia debe especificarse el valor de la rugosidad
        system["roughness_metric"] = DistanceConvert(x=system["roughness"], unitin=system["roughness_unit"],
                                                     unitout="m")


    columns = []
    values = []

    for value in system:
        columns.append(value)
        if not system[value]:
            values.append("None")
        else:
            values.append(system[value])

#    print str(tuple(columns))
#    print str(tuple(values))
#    print system
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    command = """INSERT INTO system %s VALUES %s""" % (tuple(columns), tuple(values))
    cursor.execute(command)
    connection.commit()
    connection.close()

def InsertSegmentsValues(segment, flag=False):  #por los momentos solo para calcular perdidas y caida de presion
    """Funcion para agregar los valores de los segmentos (tuberia y/o accesorios)
    en la base de datos "custom"
    """
    if not flag:
        database = "custom.pype"
    else:
        database = flag

    #por los momentos existe una restriccion general la cual es que
    #el primer segmento del sistema debe ser obligatoriamente una tuberia
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    sqlcommand = """SELECT flow_metric, viscosity_metric, density_metric, roughness_metric, pipe_type FROM system WHERE rowid=1"""
    cursor.execute(sqlcommand)
    system_data = cursor.fetchall()
    system_flow = system_data[0][0]
    system_viscosity = system_data[0][1]
    system_density = system_data[0][2]
    system_roughness = system_data[0][3]
    pipe_type = str(system_data[0][4])
#    segment["connected_from"] = str(segment["connected_from"])
#    print system_data

    if segment["type"] == "pipe":
        #si el segmento es una tuberia
        #para este segmento es obligatorio especificar lo siguiente:
        #posicion (horizontal, vertical hacia arriba, vertical hacia abajo)
        #longitud
        #diametro. ya sea especificando el diametro mimino directamente
        #o la cedula y el diametro interno o externo
        #para especificar el diametro con el tipo de cedula
        #debe haberse especificado anteriormente el tipo de
        #tuberia en las propiedades del sistema

        if segment["connected_from"] != "None":  #si la tuberia esta conectada a otro segmento
#            segment["connected_from"] = str(segment["connected_from"])
#            foo = segment["connected_from"]
#            print "here"
            command = """SELECT OD, NPS, WT, ID, schedule, minimum_diameter_metric FROM segments WHERE name=%r""" % segment["connected_from"]
#            print "2"
            cursor.execute(command)
            properties = cursor.fetchall()
#            print properties
            segment["OD"] = properties[0][0]
            segment["NPS"] = properties[0][1]
            segment["WT"] = properties[0][2]
            segment["ID"] = properties[0][3]
            segment["schedule"] = str(properties[0][4])
            segment["minimum_diameter_metric"] = properties[0][5]


        else:         #si la tuberia no esta conectada a nadie aguas arriba
            if pipe_type != "None":
                if segment["schedule"] != "None": #si se especifica la cedula
                    #si el tipo de tuberia es especificado en el sistema se debe especificar
                    #la cedula obligatoriamente y debe especificarse uno de los siguientes valores:
                    #NPS, OD, ID

                    #el siguiente bloque es para agregar  la cedula como propiedad generale a la tabla system
    #                print segment["schedule"]
    #                segment["schedule"] = "40"
                    sqlcommand = """UPDATE system SET schedule="%s" WHERE rowid=1""" % (segment["schedule"])
                    cursor.execute(sqlcommand)
                    connection.commit()
                    if segment["NPS"] != "None":
                        #buscar OD, ID y WT en base de datos
                        pipe_properties = PipeProperties(ced=segment["schedule"], NPS=segment["NPS"],
                                                           pipe=pipe_type)
                        segment["OD"] = pipe_properties[1]
                        segment["ID"] = pipe_properties[3]
                        segment["WT"] = pipe_properties[2]
                        segment["minimum_diameter_metric"] = DistanceConvert(x=segment["ID"], unitin="mm", unitout="m")

                    elif segment["OD"] != "None":
                        #buscar NPS, ID y WT en base de datos
                        pipe_properties = PipeProperties(ced=segment["schedule"], OD=segment["OD"],
                                                           pipe=pipe_type)
                        segment["NPS"] = pipe_properties[0]
                        segment["ID"] = pipe_properties[3]
                        segment["WT"] = pipe_properties[2]
                        segment["minimum_diameter_metric"] = DistanceConvert(x=segment["ID"], unitin="mm", unitout="m")

                    else:
                        msg = """se cumplio condicion else en bloque if == segment["pipe"]
                              modulo: InsertSegmentsValues
#                              extra: no existe NPS ni OD"""
                        raise Exception, msg
                else:
                    #en caso de que no se especifique la cedula
                     #ya en este caso se debe de haber especificado una rugosidad
                     #en las propiedades del sistema y tambien un diametro minimo
                     #en las propiedades de la tuberia
                     segment["minimum_diameter_metric"] = DistanceConvert(x=segment["minimum_diameter"], unitin=segment["minimum_diameter_unit"],
                                                                          unitout="m")

            else:
                segment["minimum_diameter_metric"] = DistanceConvert(x=segment["minimum_diameter"], unitin=segment["minimum_diameter_unit"],
                                                                          unitout="m")
                #si no se especifica la cedula
                #ni ninguna de las propiedades (NPS, OD y/o ID)
                #se trabaja directamente con el diametro minimo el cual debe ser
                #especificado por el usuario
#                pass #NO QUITAR ESTE PASS!!!!
        #a esta altura del ciclo debo tener obligatoriamente almenos estos valores:
        #diametro minimo (minimum_diameter_metric)
        #longitud (length)
        #rugosidad absoluta en metros (roughness_metric)
        segment["length_metric"] = DistanceConvert(x=segment["length"], unitin=segment["length_unit"], unitout="m")
        segment["reynolds"] = Reynolds(ro=system_density, mu=system_viscosity,
                                       D=segment["minimum_diameter_metric"], Q=system_flow)
        segment["friction_factor"] = Churchill(Re=segment["reynolds"], e=system_roughness,
                                               D=segment["minimum_diameter_metric"])
        segment["minimum_velocity_metric"] = VelocityFlow(D=segment["minimum_diameter_metric"], Q=system_flow)
        segment["losses_metric"] = DarcyWeisbach(f=segment["friction_factor"], L=segment["length_metric"],
                                                   Q=system_flow, D=segment["minimum_diameter_metric"])
        segment["pressure_drop_metric"] = PressureDrop(ht=segment["losses_metric"], ro=system_density)
        if segment["orientation"] == "horizontal":
            segment["height"] = 0
        elif segment["orientation"] == "vertical up":
            segment["height"] = segment["length_metric"]
        elif segment["orientation"] == "vertical down":
            segment["height"] = (segment["length_metric"])*(-1)
        else:
            msg = "se cumplio condicion else para bloque en calculo de altura\nmodulo: InsertSegmentsValues\nvarible: height"
            raise Exception, msg

    elif segment["type"] == "90_welding_elbow":
        #si el segmento es un codo soldado de 90 grados
        #para este accesorio es obligatorio especificar lo siguiente
        #radius, connected_from
        #print segment["connected_from"]
        command = "SELECT type, OD, NPS, WT, ID, schedule, minimum_diameter_metric FROM segments WHERE name=%r" % segment["connected_from"]
        cursor.execute(command)
        properties = cursor.fetchall()
        type_from = properties[0][0]
        segment["OD"] = properties[0][1]
        segment["NPS"] = properties[0][2]
        segment["WT"] = properties[0][3]
        segment["ID"] = properties[0][4]
        segment["schedule"] = str(properties[0][5])
        segment["minimum_diameter_metric"] = properties[0][6]
#        print properties
        minimum_diameter_milimiter = DistanceConvert(x=segment["minimum_diameter_metric"], unitin="m", unitout="mm")
#        print minimum_diameter_metric_milimiter, type(minimum_diameter_metric_milimiter)
        if segment["NPS"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(NPS=segment["NPS"])
        elif segment["OD"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(OD=segment["OD"])
        else:
#            print "here"
            segment["turbulent_friccion_factor"] = FtAccesories(ID=minimum_diameter_milimiter)
#            print segment["turbulent_friccion_factor"]

        segment["k_factor"] = K90WeldingElbow(r=segment["radius"], D=minimum_diameter_milimiter,
                                                ft=segment["turbulent_friccion_factor"])
        segment["minimum_velocity_metric"] = VelocityFlow(D=segment["minimum_diameter_metric"], Q=system_flow)

#        print segment["k_factor"],segment["minimum_velocity_metric"],segment["minimum_diameter_metric"]
#        print segment["radius"],segment["turbulent_friccion_factor"]
        segment["losses_metric"] = AccesoriesLosses(K=segment["k_factor"], V=segment["minimum_velocity_metric"])
        segment["pressure_drop_metric"] = PressureDrop(ht=segment["losses_metric"], ro=system_density)

    elif segment["type"] == "180_bend":
        #si el segmento es un codo soldado de 180 grados
        #para este accesorio es obligatorio especificar lo siguiente
        #radius, connected_from
        #print segment["connected_from"]
        command = "SELECT type, OD, NPS, WT, ID, schedule, minimum_diameter_metric FROM segments WHERE name=%r" % segment["connected_from"]
        cursor.execute(command)
        properties = cursor.fetchall()
        type_from = properties[0][0]
        segment["OD"] = properties[0][1]
        segment["NPS"] = properties[0][2]
        segment["WT"] = properties[0][3]
        segment["ID"] = properties[0][4]
        segment["schedule"] = str(properties[0][5])
        segment["minimum_diameter_metric"] = properties[0][6]
#        print properties
        minimum_diameter_milimiter = DistanceConvert(x=segment["minimum_diameter_metric"], unitin="m", unitout="mm")
#        print minimum_diameter_metric_milimiter, type(minimum_diameter_metric_milimiter)
        if segment["NPS"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(NPS=segment["NPS"])
        elif segment["OD"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(OD=segment["OD"])
        else:
#            print "here"
            segment["turbulent_friccion_factor"] = FtAccesories(ID=minimum_diameter_milimiter)
#            print segment["turbulent_friccion_factor"]

        k_90 = K90WeldingElbow(r=segment["radius"], D=minimum_diameter_milimiter,
                                                ft=segment["turbulent_friccion_factor"])
        segment["k_factor"] = K180WeldingElbow(r=segment["radius"], D=minimum_diameter_milimiter,
                                                ft=segment["turbulent_friccion_factor"], k90=k_90)

        segment["minimum_velocity_metric"] = VelocityFlow(D=segment["minimum_diameter_metric"], Q=system_flow)

#        print segment["k_factor"],segment["minimum_velocity_metric"],segment["minimum_diameter_metric"]
#        print segment["radius"],segment["turbulent_friccion_factor"]
        segment["losses_metric"] = AccesoriesLosses(K=segment["k_factor"], V=segment["minimum_velocity_metric"])
        segment["pressure_drop_metric"] = PressureDrop(ht=segment["losses_metric"], ro=system_density)

    elif segment["type"] == "180_close_pattern_return":
        #si el segmento es un codo de 180 grados
        #para este accesorio es obligatorio especificar lo siguiente
        # connected_from
        #print segment["connected_from"]
        command = "SELECT type, OD, NPS, WT, ID, schedule, minimum_diameter_metric FROM segments WHERE name=%r" % segment["connected_from"]
        cursor.execute(command)
        properties = cursor.fetchall()
        type_from = properties[0][0]
        segment["OD"] = properties[0][1]
        segment["NPS"] = properties[0][2]
        segment["WT"] = properties[0][3]
        segment["ID"] = properties[0][4]
        segment["schedule"] = str(properties[0][5])
        segment["minimum_diameter_metric"] = properties[0][6]
#        print properties
        minimum_diameter_milimiter = DistanceConvert(x=segment["minimum_diameter_metric"], unitin="m", unitout="mm")
#        print minimum_diameter_metric_milimiter, type(minimum_diameter_metric_milimiter)
        if segment["NPS"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(NPS=segment["NPS"])
        elif segment["OD"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(OD=segment["OD"])
        else:
#            print "here"
            segment["turbulent_friccion_factor"] = FtAccesories(ID=minimum_diameter_milimiter)
#            print segment["turbulent_friccion_factor"]

        segment["k_factor"] = K180Bend(ft=segment["turbulent_friccion_factor"])
        segment["minimum_velocity_metric"] = VelocityFlow(D=segment["minimum_diameter_metric"], Q=system_flow)
        segment["losses_metric"] = AccesoriesLosses(K=segment["k_factor"], V=segment["minimum_velocity_metric"])
        segment["pressure_drop_metric"] = PressureDrop(ht=segment["losses_metric"], ro=system_density)

    elif segment["type"] == "sudden_contraction":
        msg = "Todavia no se ha creado el bloque para calculo de contracciones"
        raise Exception, msg

    elif segment["type"] == "sudden_expansion":
        #si el segmento es una expansion brusca
        #para este accesorio es obligatorio especificar lo siguiente
        #D_2 (en las unidades apropiadas ya sea NPS o OD), connected_from
        command = "SELECT type, schedule, minimum_diameter_metric FROM segments WHERE name=%r" % segment["connected_from"]
        cursor.execute(command)
        properties = cursor.fetchall()
        type_from = properties[0][0]
        segment["schedule"] = str(properties[0][1])
        diameter_in_metric = properties[0][2] #diametro de entrada en metros
        #segment["minimum_diameter_metric"]
        if segment["schedule"] != "None":
            #si se cumple esta condicion la cedula ha sido especificada anteriormente
            #y el GUI debe mostrar una lista de los diametro externos para esa cedula
            #y tipo de tuberia especifica
            #en este caso "D_2" debe especificarse obligatoriamente
            if segment["D_2_type"] == "NPS":
                pipe_properties = PipeProperties(ced=segment["schedule"], NPS=segment["D_2"], pipe=pipe_type)
                segment["OD"] = pipe_properties[1]
                segment["ID"] = pipe_properties[3]
                segment["WT"] = pipe_properties[2]
                segment["NPS"] = segment["D_2"]
                segment["minimum_diameter_metric"] = DistanceConvert(x=segment["ID"], unitin="mm", unitout="m")

            elif segment["D_2_type"] == "OD":
                pipe_properties = PipeProperties(ced=segment["schedule"], OD=segment["D_2"], pipe=pipe_type)
                segment["NPS"] = pipe_properties[0]
                segment["ID"] = pipe_properties[3]
                segment["WT"] = pipe_properties[2]
                segment["OD"] = segment["D_2"]
                segment["minimum_diameter_metric"] = DistanceConvert(x=segment["ID"], unitin="mm", unitout="m")

            else:
                msg = "se cumplio condicion else para bloque en calculo de diametro externo para expansion\nmodulo: InsertSegmentsValues\nvarible: NPS o OD"
                raise Exception, msg
        else:
            #si no se especifica la cedula, el usuario tiene que especificar
            #directamente un diametro de salida minimo para la expansion
            #en ese caso el valor de "minimum_diameter" y "minimum_diameter_unit" debe ser especificado obligatoriamente
            segment["minimum_diameter_metric"] = DistanceConvert(x=segment["minimum_diameter"], unitin=segment["minimum_diameter_unit"],
                                                                 unitout="m")
        segment["k_factor"] = KSuddenExpansion(D1=diameter_in_metric, D2=segment["minimum_diameter_metric"])
        segment["minimum_velocity_metric"] = VelocityFlow(D=segment["minimum_diameter_metric"], Q=system_flow)
        segment["losses_metric"] = AccesoriesLosses(K=segment["k_factor"], V=segment["minimum_velocity_metric"])
        segment["pressure_drop_metric"] = PressureDrop(ht=segment["losses_metric"], ro=system_density)


    elif segment["type"] == "globe_valve_type_A":
        #si el segmento es una valvula de globo tipo A
        #para este accesorio es obligatorio especificar lo siguiente
        # connected_from
        #print segment["connected_from"]
        command = "SELECT type, OD, NPS, WT, ID, schedule, minimum_diameter_metric FROM segments WHERE name=%r" % segment["connected_from"]
        cursor.execute(command)
        properties = cursor.fetchall()
        type_from = properties[0][0]
        segment["OD"] = properties[0][1]
        segment["NPS"] = properties[0][2]
        segment["WT"] = properties[0][3]
        segment["ID"] = properties[0][4]
        segment["schedule"] = str(properties[0][5])
        segment["minimum_diameter_metric"] = properties[0][6]
#        print properties
        minimum_diameter_milimiter = DistanceConvert(x=segment["minimum_diameter_metric"], unitin="m", unitout="mm")
#        print minimum_diameter_metric_milimiter, type(minimum_diameter_metric_milimiter)
        if segment["NPS"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(NPS=segment["NPS"])
        elif segment["OD"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(OD=segment["OD"])
        else:
#            print "here"
            segment["turbulent_friccion_factor"] = FtAccesories(ID=minimum_diameter_milimiter)
#            print segment["turbulent_friccion_factor"]

        segment["k_factor"] = KGlobeValveTypeA(ft=segment["turbulent_friccion_factor"])
        segment["minimum_velocity_metric"] = VelocityFlow(D=segment["minimum_diameter_metric"], Q=system_flow)
        segment["losses_metric"] = AccesoriesLosses(K=segment["k_factor"], V=segment["minimum_velocity_metric"])
        segment["pressure_drop_metric"] = PressureDrop(ht=segment["losses_metric"], ro=system_density)

    elif segment["type"] == "globe_valve_type_B":
        #si el segmento es una valvula de globo tipo B
        #para este accesorio es obligatorio especificar lo siguiente
        # connected_from
        #print segment["connected_from"]
        command = "SELECT type, OD, NPS, WT, ID, schedule, minimum_diameter_metric FROM segments WHERE name=%r" % segment["connected_from"]
        cursor.execute(command)
        properties = cursor.fetchall()
        type_from = properties[0][0]
        segment["OD"] = properties[0][1]
        segment["NPS"] = properties[0][2]
        segment["WT"] = properties[0][3]
        segment["ID"] = properties[0][4]
        segment["schedule"] = str(properties[0][5])
        segment["minimum_diameter_metric"] = properties[0][6]
#        print properties
        minimum_diameter_milimiter = DistanceConvert(x=segment["minimum_diameter_metric"], unitin="m", unitout="mm")
#        print minimum_diameter_metric_milimiter, type(minimum_diameter_metric_milimiter)
        if segment["NPS"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(NPS=segment["NPS"])
        elif segment["OD"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(OD=segment["OD"])
        else:
#            print "here"
            segment["turbulent_friccion_factor"] = FtAccesories(ID=minimum_diameter_milimiter)
#            print segment["turbulent_friccion_factor"]

        segment["k_factor"] = KGlobeValveTypeB(ft=segment["turbulent_friccion_factor"])
        segment["minimum_velocity_metric"] = VelocityFlow(D=segment["minimum_diameter_metric"], Q=system_flow)
        segment["losses_metric"] = AccesoriesLosses(K=segment["k_factor"], V=segment["minimum_velocity_metric"])
        segment["pressure_drop_metric"] = PressureDrop(ht=segment["losses_metric"], ro=system_density)

    elif segment["type"] == "lift_check_valve_type_A":
        #si el segmento es una valvula de retencion de obturador ascendente tipo A
        #para este accesorio es obligatorio especificar lo siguiente
        # connected_from
        #print segment["connected_from"]
        command = "SELECT type, OD, NPS, WT, ID, schedule, minimum_diameter_metric FROM segments WHERE name=%r" % segment["connected_from"]
        cursor.execute(command)
        properties = cursor.fetchall()
        type_from = properties[0][0]
        segment["OD"] = properties[0][1]
        segment["NPS"] = properties[0][2]
        segment["WT"] = properties[0][3]
        segment["ID"] = properties[0][4]
        segment["schedule"] = str(properties[0][5])
        segment["minimum_diameter_metric"] = properties[0][6]
#        print properties
        minimum_diameter_milimiter = DistanceConvert(x=segment["minimum_diameter_metric"], unitin="m", unitout="mm")
#        print minimum_diameter_metric_milimiter, type(minimum_diameter_metric_milimiter)
        if segment["NPS"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(NPS=segment["NPS"])
        elif segment["OD"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(OD=segment["OD"])
        else:
#            print "here"
            segment["turbulent_friccion_factor"] = FtAccesories(ID=minimum_diameter_milimiter)
#            print segment["turbulent_friccion_factor"]

        segment["k_factor"] = KLiftCheckValveTypeA(ft=segment["turbulent_friccion_factor"])
        segment["minimum_velocity_metric"] = VelocityFlow(D=segment["minimum_diameter_metric"], Q=system_flow)
        segment["losses_metric"] = AccesoriesLosses(K=segment["k_factor"], V=segment["minimum_velocity_metric"])
        segment["pressure_drop_metric"] = PressureDrop(ht=segment["losses_metric"], ro=system_density)

    elif segment["type"] == "lift_check_valve_type_B":
        #si el segmento es una valvula de retencion de obturador ascendente tipo B
        #para este accesorio es obligatorio especificar lo siguiente
        # connected_from
        #print segment["connected_from"]
        command = "SELECT type, OD, NPS, WT, ID, schedule, minimum_diameter_metric FROM segments WHERE name=%r" % segment["connected_from"]
        cursor.execute(command)
        properties = cursor.fetchall()
        type_from = properties[0][0]
        segment["OD"] = properties[0][1]
        segment["NPS"] = properties[0][2]
        segment["WT"] = properties[0][3]
        segment["ID"] = properties[0][4]
        segment["schedule"] = str(properties[0][5])
        segment["minimum_diameter_metric"] = properties[0][6]
#        print properties
        minimum_diameter_milimiter = DistanceConvert(x=segment["minimum_diameter_metric"], unitin="m", unitout="mm")
#        print minimum_diameter_metric_milimiter, type(minimum_diameter_metric_milimiter)
        if segment["NPS"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(NPS=segment["NPS"])
        elif segment["OD"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(OD=segment["OD"])
        else:
#            print "here"
            segment["turbulent_friccion_factor"] = FtAccesories(ID=minimum_diameter_milimiter)
#            print segment["turbulent_friccion_factor"]

        segment["k_factor"] = KLiftCheckValveTypeB(ft=segment["turbulent_friccion_factor"])
        segment["minimum_velocity_metric"] = VelocityFlow(D=segment["minimum_diameter_metric"], Q=system_flow)
        segment["losses_metric"] = AccesoriesLosses(K=segment["k_factor"], V=segment["minimum_velocity_metric"])
        segment["pressure_drop_metric"] = PressureDrop(ht=segment["losses_metric"], ro=system_density)

    elif segment["type"] == "gate_valve":
        #si el segmento es una valvula de compuerta
        #para este accesorio es obligatorio especificar lo siguiente
        # connected_from
        #print segment["connected_from"]
        command = "SELECT type, OD, NPS, WT, ID, schedule, minimum_diameter_metric FROM segments WHERE name=%r" % segment["connected_from"]
        cursor.execute(command)
        properties = cursor.fetchall()
        type_from = properties[0][0]
        segment["OD"] = properties[0][1]
        segment["NPS"] = properties[0][2]
        segment["WT"] = properties[0][3]
        segment["ID"] = properties[0][4]
        segment["schedule"] = str(properties[0][5])
        segment["minimum_diameter_metric"] = properties[0][6]
#        print properties
        minimum_diameter_milimiter = DistanceConvert(x=segment["minimum_diameter_metric"], unitin="m", unitout="mm")
#        print minimum_diameter_metric_milimiter, type(minimum_diameter_metric_milimiter)
        if segment["NPS"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(NPS=segment["NPS"])
        elif segment["OD"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(OD=segment["OD"])
        else:
#            print "here"
            segment["turbulent_friccion_factor"] = FtAccesories(ID=minimum_diameter_milimiter)
#            print segment["turbulent_friccion_factor"]

        segment["k_factor"] = KGateValve(ft=segment["turbulent_friccion_factor"])
        segment["minimum_velocity_metric"] = VelocityFlow(D=segment["minimum_diameter_metric"], Q=system_flow)
        segment["losses_metric"] = AccesoriesLosses(K=segment["k_factor"], V=segment["minimum_velocity_metric"])
        segment["pressure_drop_metric"] = PressureDrop(ht=segment["losses_metric"], ro=system_density)

    elif segment["type"] == "stop_check_valve_type_A":
        #si el segmento es una valvula de retencion y cierre tipo A
        #para este accesorio es obligatorio especificar lo siguiente
        # connected_from
        #print segment["connected_from"]
        command = "SELECT type, OD, NPS, WT, ID, schedule, minimum_diameter_metric FROM segments WHERE name=%r" % segment["connected_from"]
        cursor.execute(command)
        properties = cursor.fetchall()
        type_from = properties[0][0]
        segment["OD"] = properties[0][1]
        segment["NPS"] = properties[0][2]
        segment["WT"] = properties[0][3]
        segment["ID"] = properties[0][4]
        segment["schedule"] = str(properties[0][5])
        segment["minimum_diameter_metric"] = properties[0][6]
#        print properties
        minimum_diameter_milimiter = DistanceConvert(x=segment["minimum_diameter_metric"], unitin="m", unitout="mm")
#        print minimum_diameter_metric_milimiter, type(minimum_diameter_metric_milimiter)
        if segment["NPS"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(NPS=segment["NPS"])
        elif segment["OD"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(OD=segment["OD"])
        else:
#            print "here"
            segment["turbulent_friccion_factor"] = FtAccesories(ID=minimum_diameter_milimiter)
#            print segment["turbulent_friccion_factor"]

        segment["k_factor"] = KStopCheckValveTypeA(ft=segment["turbulent_friccion_factor"])
        segment["minimum_velocity_metric"] = VelocityFlow(D=segment["minimum_diameter_metric"], Q=system_flow)
        segment["losses_metric"] = AccesoriesLosses(K=segment["k_factor"], V=segment["minimum_velocity_metric"])
        segment["pressure_drop_metric"] = PressureDrop(ht=segment["losses_metric"], ro=system_density)

    elif segment["type"] == "stop_check_valve_type_B":
        #si el segmento es una valvula de retencion y cierre tipo B
        #para este accesorio es obligatorio especificar lo siguiente
        # connected_from
        #print segment["connected_from"]
        command = "SELECT type, OD, NPS, WT, ID, schedule, minimum_diameter_metric FROM segments WHERE name=%r" % segment["connected_from"]
        cursor.execute(command)
        properties = cursor.fetchall()
        type_from = properties[0][0]
        segment["OD"] = properties[0][1]
        segment["NPS"] = properties[0][2]
        segment["WT"] = properties[0][3]
        segment["ID"] = properties[0][4]
        segment["schedule"] = str(properties[0][5])
        segment["minimum_diameter_metric"] = properties[0][6]
#        print properties
        minimum_diameter_milimiter = DistanceConvert(x=segment["minimum_diameter_metric"], unitin="m", unitout="mm")
#        print minimum_diameter_metric_milimiter, type(minimum_diameter_metric_milimiter)
        if segment["NPS"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(NPS=segment["NPS"])
        elif segment["OD"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(OD=segment["OD"])
        else:
#            print "here"
            segment["turbulent_friccion_factor"] = FtAccesories(ID=minimum_diameter_milimiter)
#            print segment["turbulent_friccion_factor"]

        segment["k_factor"] = KStopCheckValveTypeB(ft=segment["turbulent_friccion_factor"])
        segment["minimum_velocity_metric"] = VelocityFlow(D=segment["minimum_diameter_metric"], Q=system_flow)
        segment["losses_metric"] = AccesoriesLosses(K=segment["k_factor"], V=segment["minimum_velocity_metric"])
        segment["pressure_drop_metric"] = PressureDrop(ht=segment["losses_metric"], ro=system_density)

    elif segment["type"] == "stop_check_valve_type_C":
        #si el segmento es una valvula de retencion y cierre tipo C
        #para este accesorio es obligatorio especificar lo siguiente
        # connected_from
        #print segment["connected_from"]
        command = "SELECT type, OD, NPS, WT, ID, schedule, minimum_diameter_metric FROM segments WHERE name=%r" % segment["connected_from"]
        cursor.execute(command)
        properties = cursor.fetchall()
        type_from = properties[0][0]
        segment["OD"] = properties[0][1]
        segment["NPS"] = properties[0][2]
        segment["WT"] = properties[0][3]
        segment["ID"] = properties[0][4]
        segment["schedule"] = str(properties[0][5])
        segment["minimum_diameter_metric"] = properties[0][6]
#        print properties
        minimum_diameter_milimiter = DistanceConvert(x=segment["minimum_diameter_metric"], unitin="m", unitout="mm")
#        print minimum_diameter_metric_milimiter, type(minimum_diameter_metric_milimiter)
        if segment["NPS"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(NPS=segment["NPS"])
        elif segment["OD"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(OD=segment["OD"])
        else:
#            print "here"
            segment["turbulent_friccion_factor"] = FtAccesories(ID=minimum_diameter_milimiter)
#            print segment["turbulent_friccion_factor"]

        segment["k_factor"] = KStopCheckValveTypeC(ft=segment["turbulent_friccion_factor"])
        segment["minimum_velocity_metric"] = VelocityFlow(D=segment["minimum_diameter_metric"], Q=system_flow)
        segment["losses_metric"] = AccesoriesLosses(K=segment["k_factor"], V=segment["minimum_velocity_metric"])
        segment["pressure_drop_metric"] = PressureDrop(ht=segment["losses_metric"], ro=system_density)

    elif segment["type"] == "ball_valve":
        #si el segmento es una valvula de bola
        #para este accesorio es obligatorio especificar lo siguiente
        # connected_from
        #print segment["connected_from"]
        command = "SELECT type, OD, NPS, WT, ID, schedule, minimum_diameter_metric FROM segments WHERE name=%r" % segment["connected_from"]
        cursor.execute(command)
        properties = cursor.fetchall()
        type_from = properties[0][0]
        segment["OD"] = properties[0][1]
        segment["NPS"] = properties[0][2]
        segment["WT"] = properties[0][3]
        segment["ID"] = properties[0][4]
        segment["schedule"] = str(properties[0][5])
        segment["minimum_diameter_metric"] = properties[0][6]
#        print properties
        minimum_diameter_milimiter = DistanceConvert(x=segment["minimum_diameter_metric"], unitin="m", unitout="mm")
#        print minimum_diameter_metric_milimiter, type(minimum_diameter_metric_milimiter)
        if segment["NPS"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(NPS=segment["NPS"])
        elif segment["OD"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(OD=segment["OD"])
        else:
#            print "here"
            segment["turbulent_friccion_factor"] = FtAccesories(ID=minimum_diameter_milimiter)
#            print segment["turbulent_friccion_factor"]

        segment["k_factor"] = KBallValve(ft=segment["turbulent_friccion_factor"])
        segment["minimum_velocity_metric"] = VelocityFlow(D=segment["minimum_diameter_metric"], Q=system_flow)
        segment["losses_metric"] = AccesoriesLosses(K=segment["k_factor"], V=segment["minimum_velocity_metric"])
        segment["pressure_drop_metric"] = PressureDrop(ht=segment["losses_metric"], ro=system_density)

    elif segment["type"] == "90_standard_elbow":
        #si el segmento es un codo soldado de 90 grados
        #para este accesorio es obligatorio especificar lo siguiente
        # connected_from
        #print segment["connected_from"]
        command = "SELECT type, OD, NPS, WT, ID, schedule, minimum_diameter_metric FROM segments WHERE name=%r" % segment["connected_from"]
        cursor.execute(command)
        properties = cursor.fetchall()
        type_from = properties[0][0]
        segment["OD"] = properties[0][1]
        segment["NPS"] = properties[0][2]
        segment["WT"] = properties[0][3]
        segment["ID"] = properties[0][4]
        segment["schedule"] = str(properties[0][5])
        segment["minimum_diameter_metric"] = properties[0][6]
#        print properties
        minimum_diameter_milimiter = DistanceConvert(x=segment["minimum_diameter_metric"], unitin="m", unitout="mm")
#        print minimum_diameter_metric_milimiter, type(minimum_diameter_metric_milimiter)
        if segment["NPS"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(NPS=segment["NPS"])
        elif segment["OD"] != "None":
            segment["turbulent_friccion_factor"] = FtAccesories(OD=segment["OD"])
        else:
#            print "here"
            segment["turbulent_friccion_factor"] = FtAccesories(ID=minimum_diameter_milimiter)
#            print segment["turbulent_friccion_factor"]

        segment["k_factor"] = K90StandardElbow(ft=segment["turbulent_friccion_factor"])
        segment["minimum_velocity_metric"] = VelocityFlow(D=segment["minimum_diameter_metric"], Q=system_flow)
        segment["losses_metric"] = AccesoriesLosses(K=segment["k_factor"], V=segment["minimum_velocity_metric"])
        segment["pressure_drop_metric"] = PressureDrop(ht=segment["losses_metric"], ro=system_density)

    elif segment["type"] == "45_standard_elbow":
        msg = "Todavia no se ha creado el bloque para calculo de angulos de 45"
        raise Exception, msg

    columns = []
    values = []
    for value in segment:
        columns.append(value)
        if segment[value] == "None":
            values.append("None")
        else:
            values.append(segment[value])
#    print columns
#    print values

#    print str(tuple(columns))
#    print str(tuple(values))
#    print tuple(columns)
#    print tuple(values)
#    cont = 1
#    for x in range(len(values)):
#        print columns[x], type(columns[x])
#        print values[x], type(values[x])
#        print cont
#        a=(unicode(columns[x]))
#        b=(values[x])
#        a.append(columns[x])
#        b.append(values[x])
        
#        command = "INSERT INTO segments %s VALUES %r" % (a, b)
    command = """INSERT INTO segments %s VALUES %r""" % (tuple(columns), tuple(values))
    cursor.execute(command)
    connection.commit()
#    cont+=1
    connection.close()

def TemperatureConvert(temp, unitin, unitout):
    """"Funcion para convertir la temperatura en las siguientes unidades
    grados celsius
    grados farenheit
    """
    if unitin == "F":
        temp_c = (temp-32.0)/1.8
    elif unitin == "C":
        temp_c = temp
    else:
        msg = "se cumplio condicion para primer bloque if\nmodulo: TemperatureConvert\nvarible: unitin"
        raise Exception, msg


    if unitout == "C":
        return temp_c
    if unitout == "F":
        temp_f = (temp_c*(1.8))+32.0
        return temp_f
    else:
        msg = "se cumplio condicion para segundo bloque if\nmodulo: TemperatureConvert\nvarible: unitout"
        raise Exception, msg

def WaterProperties(temp):
    """Funcion para obtener las propiedades del agua a partir de la temperatura
    en grados centigrados accediendo a la base de datos del agua.
    Las propiedades se devuelven en un diccionario con el siguiente formato:

    data = {"Temperature" : (valor, unidad),
            "Pressure" : (valor, unidad),
            "Density" : (valor, unidad),
            "Especific_Volume": (valor, unidad),
            "InternalEnergy" : (valor, unidad),
            "Enthalpy" : (valor, unidad),
            "Entropy" : (valor, unidad),
            "Cv" : (valor, unidad),
            "Cp" : (valor, unidad),
            "Sound_Speed" : (valor, unidad),
            "Joule_Thompson" : (valor, unidad),
            "Viscosity" : (valor, unidad),
            "ThermCond" : (valor, unidad),
            "SurfTension" : (valor, unidad)}
    """
    def Interpolation(temp, data1, data2):
        """Funcion para interpolar los valores de las propiedades del agua
        """
        dataint = []
        dataintlist = []
        X0 = temp         #valor de temperatura
        X1 = data1[0]     #valor de temperatura anterior en la base de datos
        X2 = data2[0]     #valor de temperatura siguiente en la base de datos
        dataint.append(X0)
        values = map(None, data1[1:], data2[1:])  #lista relacional entre los valores anteriores y siguientes en la BD sin contar la temperatura
        for items in values:
            Y1 = items[0]
            Y2 = items[1]
            try:
                Y = Y1+((X0-X1)*(Y2-Y1)/(X2-X1))
            except:
                dataint.append(Y2)
            else:
                dataint.append(Y)
        dataintlist.append(dataint)
        return dataintlist

    connection = sqlite3.connect(databaseName)
    cursor = connection.cursor()

    if temp < 0.01 or temp > 373.94:
        connection.close()
        msg = "valor menor a 0.01 y mayor a 373.94\nmodulo: WaterProperties\nvarible: temp"
        raise Exception, msg

    elif temp == 0.01:
        sqlcommand = "SELECT * FROM water WHERE Temperature=0.01"
        cursor.execute(sqlcommand)
        finaldatalist = cursor.fetchall()

    elif temp == 373.94:
        sqlcommand = "SELECT * FROM water WHERE Temperature=373.94"
        cursor.execute(sqlcommand)
        finaldatalist = cursor.fetchall()

    elif temp < 2 and temp > 0.01:
        sqlcommand = "SELECT * FROM water WHERE Temperature=0.01"
        cursor.execute(sqlcommand)
        pre_datalist =cursor.fetchall()
        pre_data = pre_datalist[0]
        sqlcommand = "SELECT * FROM water WHERE Temperature=2"
        cursor.execute(sqlcommand)
        next_datalist = cursor.fetchall()
        next_data = next_datalist[0]
        finaldatalist = Interpolation(temp, pre_data, next_data)

    elif temp < 373.94 and temp > 372:
        sqlcommand = "SELECT * FROM water WHERE Temperature=372"
        cursor.execute(sqlcommand)
        pre_datalist =cursor.fetchall()
        pre_data = pre_datalist[0]
        sqlcommand = "SELECT * FROM water WHERE Temperature=373.94"
        cursor.execute(sqlcommand)
        next_datalist = cursor.fetchall()
        next_data = next_datalist[0]
        finaldatalist = Interpolation(temp, pre_data, next_data)

    elif temp%2 != 0:
        next_temp = int(temp) + (int(temp)%2)
        sqlcommand = "SELECT rowid FROM water WHERE Temperature=%s" % str(next_temp)
        cursor.execute(sqlcommand)
        next_id_list = cursor.fetchall()
        next_id = next_id_list[0][0]
        pre_id = next_id - 1
        sqlcommand = "SELECT * FROM water WHERE rowid=%s" % str(pre_id)
        cursor.execute(sqlcommand)
        pre_datalist = cursor.fetchall()
        pre_data = pre_datalist[0]
        sqlcommand = "SELECT * FROM water WHERE rowid=%s" % str(next_id)
        cursor.execute(sqlcommand)
        next_datalist = cursor.fetchall()
        next_data = next_datalist[0]
        finaldatalist = Interpolation(temp, pre_data, next_data)

    elif temp%2 == 0:
        sqlcommand = "SELECT * FROM water WHERE Temperature=%s" % temp
        cursor.execute(sqlcommand)
        finaldatalist = cursor.fetchall()
    else:
        msg = "valor no es un numero\nmodulo: WaterProperties\nvarible: temp"
        raise Exception, msg


    connection.close()
    finaldata = {"Temperature" : (finaldatalist[0][0], "C"), "Pressure" : (finaldatalist[0][1], "MPa"),
            "Density" : (finaldatalist[0][2], "kg/m3"), "Especific_Volume": (finaldatalist[0][3], "m3/kg"),
            "Internal_Energy" : (finaldatalist[0][4], "kJ/mol"), "Enthalpy" : (finaldatalist[0][5], "kJ/mol"),
            "Entropy" : (finaldatalist[0][6], "J/mol*K"), "Cv" : (finaldatalist[0][7], "J/mol*K"),
            "Cp" : (finaldatalist[0][8], "J/mol*K"), "Sound_Speed" : (finaldatalist[0][9], "m/seg"),
            "Joule_Thompson" : (finaldatalist[0][10], "K/MPa"), "Viscosity" : (finaldatalist[0][11], "Pa*seg"),
            "Therm_Cond" : (finaldatalist[0][12], "W/m*K"), "Surf_Tension" : (finaldatalist[0][13], "N/m")}
    return finaldata

def Churchill(Re, e, D):
    """Funcion para calcular el factor de friccion mediante la ecuacion de churchill

            fc = 8.0*(((8/Re)**12.0)+(1/((A+B)**(3.0/2.0))))**(1/12.0)
            A = (2.457*log((1.0/(((7.0/Re)**0.9)+(0.27*e/D)))))**16
            B = (37530/Re)**16

        e = rugosidad absoluta (m)
        D = diametro (m)
        """

    A = (2.457*log((1.0/(((7.0/Re)**0.9)+(0.27*e/D)))))**16.0
    B = (37530.0/Re)**16.0
    fc = 8.0*(((8.0/Re)**12.0)+(1.0/((A+B)**(3.0/2.0))))**(1.0/12.0)
    return fc

def Reynolds(ro, mu, D, Q=None, v=None):
    """Funcion para calcular el numero de Reynolds
        Re = (4*Q*ro)/(pi*mu*D)
        Re = (ro*v*D)/mu

        Re = numero de reynolds
        Q = caudal (m3/seg)
        ro = densidad (kg/m3)
        mu = viscosidad (kg/(m*seg))
        D = diametro (m)"""
    if v == None:
        Re = (4.0*Q*ro)/(pi*mu*D)
        return Re
    elif Q == None:
        Re = (ro*v*D)/mu
        return Re
    else:
        msg = "se cumplio condicion else\nmodulo: Reynolds"
        raise Exception, msg


def VelocityFlow(D=None, Q=None, A=None, V=None):
    """Funcion para calcular la velocidad o caudal a partir del diametro
        o del area.
        V = (4.0*Q)/(pi*(D**2))
        V = Q/A

        Q = V*A
        Q = (pi*(D**2)*V)/4.0

        Q = caudal (m3/seg)
        D = diametro (m)
        V = velocidad (m/seg)
        A = area (m2)
    """
    if A == None and V == None:
        V = (4.0*Q)/(pi*(D**2))
        return V
    elif D == None and V == None:
        V = Q/A
        return V
    elif A == None and Q == None:
        Q = (pi*(D**2)*V)/4.0
        return Q
    elif D == None and Q == None:
        Q = V*A
        return Q
    else:
        msg = "se cumplio condicion else\nmodulo: VelocityFlow"
        raise Exception, msg

def FlowConvert(Q, unitin, unitout):
    """Funcion para convertir el caudal a cualquiera
    de las siguientes unidades
    galones/seg
    galones/min
    galones/hora
    litros/minuto
    litros/seg
    litros/hora
    barriles/hora
    """
    if unitin == "gal/seg":
        Qm = Q*0.0037854
    elif unitin == "gal/min":
        Qm = Q*0.0037854*60.0
    elif unitin == "gal/h":
        Qm = Q*0.0037854*3600.0
    elif unitin == "l/min":
        Qm = Q*0.000016667
    elif unitin == "l/seg":
        Qm = Q*0.000016667/60.0
    elif unitin == "l/h":
        Qm = Q*0.000016667*60.0
    elif unitin == "barriles/h":
        Qm = Q*0.117347765/3600.0
    elif unitin == "m3/seg":
        Qm = Q
    else:
        msg = "se cumplio condicion else en primer bloque de if\nmodulo: FlowConvert\nvariable: unitin"
        raise Exception, msg

    if unitout == "m3/seg":
        return Qm
    elif unitout == "l/min":
        Ql = Qm/0.000016667
        return Ql
    else:
        msg = "se cumplio condicion else en segundo bloque de if\nmodulo: FlowConvert\nvariable: unitout"
        raise Exception, msg

def TotalLosses(V1, Vn, hft=0, dZ=0, g=gravity):
    """Funcion para calcular las perdidas totales
    ht = (((V1**2)-(Vn**2))/2*g)+htsum+hmsum+dZ

    ht = perdidas totales
    V1 = Velocidad inicial
    V2 = Velocidad final
    g = aceleracion de la gravedad
    hft = sumatoria de las perdidas individuales en todos los accesorios y tuberias
    dZ = diferencia de altura
    """

    ht = (((Vn**2)-(V1**2))/(2.0*g))+hft+dZ
    return ht

def PressureDrop(ht, ro, g=gravity):
    """Funcion para calcular la caida de presion a partir de las perdidas totales
    dP = ht*ro*g

    ht = perdidas totales (m)
    ro = densidad (kg/m3)
    g = aceleracion de la gravedad (m/seg2)
    dP = caida de presion (N/m2)
    """
    dP = ht*ro*g
    return dP

def PressureLossesConvert(ro, g=gravity, ht=None, dP=None):
    """Funcion para calcular las perdidas a partir de la caida de presion y viceversa
    dP = ht*ro*g
    ht = dP/(ro*g)

    ht = perdidas totales (m)
    ro = densidad (kg/m3)
    g = aceleracion de la gravedad (m/seg2)
    dP = caida de presion (N/m2)
    """
    if ht == None:
        ht = dP/(ro*g)
        return ht
    elif dP == None:
        dP = ht*ro*g
        return dP
    else:
        msg = "se cumplio condicion else\nmodulo: PressureLossesConvert"
        raise Exception, msg

def PressureConvert(x, unitin, unitout):
    """Funcion para convertir la caida de presion en las siguientes unidades:
    Pascal (N/m2)
    bar
    atm
    psi
    torr
    """
    if unitin == "Pa":
        x_bar = x*0.00001
    elif unitin == "atm":
        x_bar = x/0.986923267
    elif unitin == "psi":
        x_bar = x/14.5037738
    elif unitin == "torr":
        x_bar = x/750.061683
    elif unitin == "bar":
        x_bar = x
    else:
        msg = "se cumplio condicion else en primer bloque de if\nmodulo: PressureConvert\nvariable: unitin"
        raise Exception, msg

    if unitout == "bar":
        return x_bar
    elif unitout == "Pa":
        x_pa = x_bar/0.00001
        return x_pa
    elif unitout == "atm":
        x_atm = x_bar*0.986923267
        return x_atm
    elif unitout == "psi":
        x_psi = x_bar*14.5037738
        return x_psi
    elif unitout == "torr":
        x_torr = x_bar*750.061683
        return x_torr
    else:
        msg = "se cumplio condicion else en segundo bloque de if\nmodulo: PressureConvert\nvariable: unitout"
        raise Exception, msg

def KinematicViscosityConvert(nu):
    """Funcion para convertir la viscosidad cinematica de unidades cStoke
    a unidades de m2/seg
    """
    nu_m = nu*0.000001
    return nu_m

def DistanceConvert(x, unitin, unitout):
    """Funcion para convertir distancia (longitud, diametro,etc) en las
    siguientes unidades

    metro
    milimetro
    pulgadas
    pies
    """
    if unitin == "mm":
        x_m = x/1000.0
    elif unitin == "inch":
        x_m = x*0.0254
    elif unitin == "ft":
        x_m = x*0.3048
    elif unitin == "m":
        x_m = x
    else:
        msg = "se cumplio condicion else en primer bloque de if\nmodulo: DistanceConvert\nvariable: unitin"
        raise Exception, msg

    if unitout == "m":
        return x_m
    elif unitout == "mm":
        x_mm = x_m*1000.0
        return x_mm
    elif unitout == "inch":
        x_inch = x_m/0.0254
        return x_inch
    elif unitout == "ft":
        x_ft = x_m/0.3048
        return x_ft
    else:
        msg = "se cumplio condicion else en segundo bloque de if\nmodulo: DistanceConvert\nvariable: unitout"
        raise Exception, msg

def DensityConvert(x, unitin, unitout):
    """Funcion para convertir la densidad en las siguientes unidades
    lb/ft3
    kg/m3
    """
    if unitin == "lb/ft3":
        x_m = x*16.0184634
    elif unitin == "kg/m3":
        x_m = x
    else:
        msg = "se cumplio condicion else en primer bloque de if\nmodulo: DensityConvert\nvariable: unitin"
        raise Exception, msg

    if unitout == "kg/m3":
        return x
    elif unitout == "lb/ft3":
        x_ft = x_m/16.0184634
        return x_ft
    else:
        msg = "se cumplio condicion else en segundo bloque de if\nmodulo: DensityConvert\nvariable: unitout"
        raise Exception, msg

def ViscosityConv(x, unitin, unitout):
    """Funcion para convertir la viscosidad en las siguientes unidades
    cP
    Pa*seg
    """
    if unitin == "cP":
        x_m = x*0.001
    elif unitin == "Pa*seg":
        x_m = x
    else:
        msg = "se cumplio condicion else en primer bloque de if\nmodulo: ViscosityConvert\nvariable: unitin"
        raise Exception, msg

    if unitout == "Pa*seg":
        return x_m
    elif unitout == "cP":
        x_cP = x_m/0.001
        return x_cP
    else:
        msg = "se cumplio condicion else en segundo bloque de if\nmodulo: ViscosityConvert\nvariable: unitout"
        raise Exception, msg

def KarmanL(Re):
    """Funcion para calcular el factor de friccion para tuberias lisas
        usando la ecuacion de Von Karman.

                fc = (1.0/((2.0*log10(Re*sqrt(fa)))-0.8))**2.0

        fc = factor de friccion
        Re = numero de Reynolds

        esta funcion devuelve 2 valores de manera simultanea los cuales son
        fc (factor de friccion) y cont (numero de iteraciones).
        Esta funcion debe llamarse en el siguiente formato:

        f, cont = KarmanL(Re)
    """
    fa = 0.05
    fc = 0
    cont = 0
    while True:
        fc = (1.0/((2.0*log10(Re*sqrt(fa)))-0.8))**2.0
        cont += 1
        cond = abs(fa - fc)
        if cond <= 0.00000001:
            break
        else:
            fa = fc
    return fc, cont

def AreaDiameter(A=None, D=None):
    """Funcion para conseguir el area a partir del diametro y viceversa

        A = (pi*(D**2))/4.0
        D = sqrt((A*4.0)/pi)

        A = Area (m2)
        D = diametro (m)
        """
    if A == None:
        A = (pi*(D**2))/4.0
        return A
    elif D == None:
        D = sqrt((A*4.0)/pi)
        return D
    else:
        msg = "se cumplio condicion else\nmodulo: AreaDiameter"
        raise Exception, msg

def VelocityFt(v):
    """funcion para convertir la velocidad de m/seg a ft/seg
    """
    v_ft = v*3.2808399
    return v_ft


###############################################################################################
###Funciones para calculos relacionados con tuberias

def DarcyWeisbach(f, L, Q, D, g=gravity):
    """Funcion para calcular la perdida por friccion en una tuberia, con la
    ecuacion de Darcy Weisbach:

    hf = (8.0*f*L*(Q**2))/((pi**2)*g*(D**5))

    hf = perdida por friccion en la tuberia (m)
    f = factor de friccion
    Q = Caudal (m3/seg)
    L = longitud de la tuberia (m)
    g = Aceleracion de la gravedad
    D = Diametro (m)
    """
    hf = (8.0*f*L*(Q**2))/((pi**2)*g*(D**5))
    return hf


def PipeProperties(ced, OD=None, NPS=None, pipe="CSP"):
    """Funcion para obtener el diametro interno a partir del diametro nominal o el diametro externo
    la cedula y el tipo de tuberia (comercial o acero inoxidable).

        pipe = tipo de tuberia (comercial o acero inoxidable)
        ced = cedula
        NPS = diametro nominal (inch)
        OD = diametro externo (mm)
    """
    type_of_pipe = {"CSP" : {"10" : "Commercial_Steel_Pipe_c10",
                             "20" : "Commercial_Steel_Pipe_c20",
                             "30" : "Commercial_Steel_Pipe_c30",
                             "40" : "Commercial_Steel_Pipe_c40",
                             "60" : "Commercial_Steel_Pipe_c60",
                             "80" : "Commercial_Steel_Pipe_c80",
                             "100" : "Commercial_Steel_Pipe_c100",
                             "140" : "Commercial_Steel_Pipe_c140",
                             "160" : "Commercial_Steel_Pipe_c160",
                             "STD" : "Commercial_Steel_Pipe_STD",
                             "XS" : "Commercial_Steel_Pipe_XS",
                             "DXS" : "Commercial_Steel_Pipe_DXS"
                             },
                    "SSP" : {"05" : "Stainless_Steel_Pipe_c05",
                             "10" : "Stainless_Steel_Pipe_c10",
                             "40" : "Stainless_Steel_Pipe_c40",
                             "80" : "Stainless_Steel_Pipe_c80"
                            },
                    "PVC" : {"40" : "PVC_Pipe_c40",
                             "80" : "PVC_Pipe_c80",
                             "120" : "PVC_Pipe_c120"
                             }
                    }
    connection = sqlite3.connect(databaseName)
    cursor = connection.cursor()

    if OD == None:
            sqlcommand = "SELECT * FROM %s WHERE Nominal_Pipe_size=%s" % (type_of_pipe[pipe][ced], NPS)
            cursor.execute(sqlcommand)
            data = cursor.fetchall()
    elif NPS == None:
            sqlcommand = "SELECT * FROM %s WHERE Outside_Diameter=%s" % (type_of_pipe[pipe][ced], OD)
            cursor.execute(sqlcommand)
            data = cursor.fetchall()
    else:
        connection.close()
        msg = "se cumplio condicion else\nmodulo: PipeProperties"
        raise Exception, msg
    connection.close()
    return data[0]

###############################################################################################
###Funciones para calculos relacionados con accesorios

def K90WeldingElbow(r, D, ft):
    """Funcion para calcular la K para angulos de 90 grados (codos soldados) los cuales
    dependen de el valor r_d

    r_d = r/d
    """
    ###Ecuaciones de K para angulos de 90 grados
    k_90_grados = ((1, 20),
                   (2, 12),
                   (3, 12),
                   (4, 14),
                   (6, 17),
                   (8, 24),
                   (10, 30),
                   (12, 34),
                   (14, 38),
                   (16, 42),
                   (20, 50))
    def Aprox(x):
        if (abs(x - 1.5) <= 0.25):
            x_aprox = 1.5
            return x_aprox
        else:
            if int(x+0.5) == int(x):
                x_aprox = int(x)
                return x_aprox
            else:
                x_aprox = int(x+0.5)
                return x_aprox

    r_d = r/D
    r_d_aprox = Aprox(r_d)

    if r_d_aprox == 1.5:
        k = 14*ft
        return k
    else:
        for x in k_90_grados:
#            print x[0], type(x[0])
#            print r_d_aprox, type(r_d_aprox)
            if (x[0] == r_d_aprox):
                k = x[1]*ft
                return k
            elif (x[0] > r_d_aprox):
#                print x[1], ft
                k = x[1]*ft
                return k
            else:
                pass
#                msg = "se cumplio condicion else\nmodulo: K90WeldingElbow"
#                raise Exception, msg

def K180WeldingElbow(ft, r, D, k90):
    """Funcion para calcular la K para angulos de 180 grados (codo soldado)
    K = ((0.25*pi*ft*(r/D))+(0.5*k90))+k90
    k90 = k para un angulo de 90 grados
    """
    k = ((2.0*(0.25*pi*ft*(r/D))+(0.5*k90)))+k90
    return k

def K180Bend(ft):
    """Funcion para calcular la K para codos de 180 grados especificados como
    "Close pattern return bend" en la pagina A-30 del Crane tp-410
    K = 50*ft
    """

    k = 50.0*ft
    return k

def K90StandardElbow(ft):
    """Funcion para calcular el valor de K para codos de 90 grados
        K = 30.0*ft

        ft = factor de friccion en turbulencia total
    """
    k = 30.0*ft
    return k

def K45StandardElbow(ft):
    """Funcion para calcular el valor de K para codos de 45 grados
        K = 16.0*ft

        ft = factor de friccion en turbulencia total
    """
    k = 16.0*ft
    return k

def KCheckValve(d1, d2, ft):
    """Funcion para calcular el valor de K para la valvula de retencion check
    con obturador ascendente
    """
    beta = float(d1)/float(d2)
    k1 = 600.0*ft
    k2 = (k1+(beta*((0.5*(1-(beta**2)))+((1-(beta**2))**2))))/(beta**4)
    return k2

def KGlobeValve(ft, d1, d2, x1, x2):
    """ Funcion para calcular la K de la valvula de globo cuando los diametros
        de entrada y salida son distintos (beta < 1)

        k2 = (k1+(0.8*sin((radians(x1)/2.0))*(1-(beta**2.0)))+ (2.6*sin((radians(x2)/2.0))*((1-(beta**2.0))**2.0)))/(beta**4.0)

        ft = valor del factor de friccion
        beta = d1/d2
        d1 = diametro entrada (m)
        diametro salida (m)
        x1 = angulo de entrada (grados)
        x2 = angulo de salida (grados)
    """

    k1 = 3.0*ft
    beta = float(d1)/float(d2)
    k2 = (k1+(0.8*sin((radians(x1)/2.0))*(1-(beta**2.0)))+ (2.6*sin((radians(x2)/2.0))*((1-(beta**2.0))**2.0)))/(beta**4.0)
    return k2

def KGlobeValveTypeA(ft, d1=None, d2=None):
    """Funcion para calcular la K para valvulas de globo (tipo A)
    """
    K = 340.0*ft
    return K

def KGlobeValveTypeB(ft, d1=None, d2=None):
    """Funcion para calcular la K para valvulas de globo (tipo B)
    """
    K = 55*ft
    return K

def KLiftCheckValveTypeA(ft, d1=None, d2=None):
    """Funcion para calcular la K para valvulas de retencion de obturador ascendente (tipo A)
    """
    K = 600*ft

def KLiftCheckValveTypeB(ft, d1=None, d2=None):
    """Funcion para calcular la K para valvulas de retencion de obturador ascendente (tipo B)
    """
    K = 55*ft
    return K

def KStopCheckValveTypeA(ft, d1=None, d2=None):
    """Funcion para calcular la K para valvulas de retencion y cierre (tipo A)
    """
    K = 400*ft
    return K

def KStopCheckValveTypeB(ft, d1=None, d2=None):
    """Funcion para calcular la K para valvulas de retencion y cierre (tipo B)
    """
    K = 300*ft
    return K

def KStopCheckValveTypeC(ft, d1=None, d2=None):
    """Funcion para calcular la K para valvulas de retencion y cierre (tipo C)
    """
    K = 55*ft
    return K

def KGateValve(ft, d1=None, d2=None):
    """Funcion para calcular la K para valvulas de compuerta
    """
    K = 8*ft
    return K

def KBallValve(ft, d1=None, d2=None):
    """Funcion para calcular la K para valvulas de bola
    """
    K = 3*ft
    return K

def KTotal(ht, v, f, L, D, g=gravity):
    """Funcion para calcular el valor de K total a partir de las perdidas totales
    kt = ((ht*2*g)/(v**2))-((f*L)/D)

    ht = perdidas totales (m)
    g = aceleracion de la gravedad (m/seg2)
    L = longitud de tuberia (m)
    D = Diametro de tuberia (D)
    v = velocidad del fluido (m/seg)
    """
    kt = ((ht*2.0*g)/(v**2))-(f*L/D)
    return kt

def KPlacaOrificio(d1, d2, Q, dP, ro):
    """Funcion para conseguir la K de la placa orificio
        Ks = ((1-(beta**4))/((C**2)*(beta**4))
        Ks = (1.0-(beta**4))/(((Q/(A*sqrt(2.0dP/ro)))**2)*(beta**4))

        beta = d1/d2
        Q = caudal (m3/seg)
        ro = densidad (kg/m3)
        dP = caida de presion (N/m2)
        """

    beta = float(d1)/float(d2)
    Ks = (1.0-(beta**4))/(((Q/(A*sqrt(2.0*dP/ro)))**2)*(beta**4))
    return Ks

def KLongitudEq(K=None, f=None, Leq=None, L=None, D=None):
    """Funcion para calcular K, L/D, L o D a partir de las variables restantes
        K = f *(Leq)

        K = coeficiente de accesorio
        f = factor de friccion
        Leq = L/D = coeficiente de longitud equivalente
        L = longitud (m)
        D = diametro (m)
        """
    if Leq == None and L == None and D == None:
        Leqi = K/f
        return Leqi
    elif K == None and L == None and D == None:
        Ki = f*Leq
        return Ki
    elif K == None and Leq == None:
        Ki = f*(L/D)
        return Ki
    elif L == None and Leq == None:
        Li =(K*D)/f
        return Li
    elif D == None and Leq == None:
        Di = (L*f)/K
        return Di
    else:
        msg = "se cumplio condicion else\nmodulo: KLongitudEq"
        raise Exception, msg



def KSuddenExpansion(D1, D2):
    """Funcion para calcular la K para una contraccion brusca

    K1 = (1-((D1/D2)**2))**2
    K2 = K1/((D1/D2)**4)

    D1 = diametro de entrada
    D2 = diametro de salida
    """
    K1 = (1.0-((float(D1)/float(D2))**2))**2
    K2 = K1/((D1/D2)**4)
    return K2

def FtAccesories(OD=None, NPS=None, ID=None):
    """Funcion para obtener el valor del factorde friccion en turbulencia total a partir
        de cualquiera de los siguientes valores

        OD = Diametro externo en milimetros
        NPS = Diametro nominal en pulgadas
        ID = Diametro interno en milimetros

        El ID teoricamente no debe ser utilizado, pero en caso de que el usuario desconosca
        tanto el diametro interno como la cedula de la tuberia, al ingresar el ID esta funcion
        asume este valor como un OD para una tuberia generica, y realiza el calculo de esa manera.
        el error promedio usando ID es de 10%
        """
    connection = sqlite3.connect("custom.pype")
    cursor = connection.cursor()
    command = "SELECT roughness_metric FROM system WHERE rowid=1"
    cursor.execute(command)
    data = cursor.fetchall()
    connection.close()
    absolute_roughness = data[0][0]
#    print absolute_roughness, type(absolute_roughness)
    if OD:
        diameter_metric = DistanceConvert(OD, "mm", "m")
    elif NPS:
        diameter_metric = DistanceConvert(NPS, "inch", "m")
    elif ID:
        diameter_metric = DistanceConvert(ID, "mm", "m")

    ft = 0.25/((log10((absolute_roughness/diameter_metric)/3.7))**2)

    return ft
###este era el procedimento anterior, pero solo servia para tuberias comerciales,
###cedula 40
#    ###Factores de friccion en turbulencia total para los distintos diametros
#    ###nominales de los accesorios
#    #Variable = ((mm),(inch),(ft))
#    ft_tabla = ((15.0, 0.5, 0.027),
#                (20.0, 0.75, 0.025),
#                (25.0, 1.0, 0.023),
#                (32.0, 1.25, 0.022),
#                (40.0, 1.5, 0.021),
#                (50.0, 2.0, 0.019),
#                (65.0, 2.5, 0.018),
#                (80.0, 3.0, 0.018),
#                (100.0, 4.0, 0.017),
#                (125.0, 5.0, 0.016),
#                (150.0, 6.0, 0.015),
#                (200.0, 8.0, 0.014),
#                (250.0, 10.0, 0.014),
#                (300.0, 12.0, 0.013),
#                (400.0, 16.0, 0.013),
#                (450.0, 18.0, 0.012),
#                (600.0, 24.0, 0.012))
#
#    if OD:
#        for x in ft_tabla:
#            if x[0] >= OD:
#                fti = x[-1]
#                return fti
#            else:
#                fti = None
#        return fti
#    elif NPS:
#        for x in ft_tabla:
#            if x[1] >= NPS:
#                fti = x[-1]
#                return fti
#            else:
#                fti = None
#        return fti
#    elif ID:
#        for x in ft_tabla:
#            if x[0] >= ID:
#                fti = x[-1]
#                return fti
#            else:
#                fti = None
#        return fti
#
#    else:
#        msg = "se cumplio condicion else\nmodulo: FtAccesories"
#        raise Exception, msg

def ScheduleFromClass(clase, NPS=None):
    """Funcion para determinar la cedula a usar a partir de la Clase del
        accesorio

        NPS = nominal pipe size inches (medida nominal de la tuberia en pulgadas)
        """
    if clase <= "300":
        cedi = "40"
    elif clase == "400" or clase == "600":
        cedi = "80"
    elif clase == "900":
        cedi = "120"
    elif clase == "1500":
        cedi = "160"
    elif clase == "2500":
        if NPS >= 0.5 and NPS <= 6:
            cedi = "DXS"
        elif NPS >= 8:
            cedi = "160"
        else:
            msg = "se cumplio condicion else en bloque anidado de if\nmodulo: ScheduleFromClass\nvariable: NPS"
            raise Exception, msg
    else:
        msg = "se cumplio condicion else bloque de if externo\nmodulo: ScheduleFromClass\nvariable: clase"
        raise Exception, msg
    return cedi
    #en caso de darse "else" completar codigo para dar un mensaje de emergencia

def MinimumVelocity(volumen_esp, d1, d2):
    """Funcion para calcular la velocidad minima para abrir completamente
    el obturador de la valvula
    vmin = 40*(beta**2)*(sqrt(volumen_esp))

    volumen_esp = volumen especifico (ft/seg)
    vmin = velocidad minima (ft/seg)
    """
    beta = float(d1)/float(d2)
    vmin = 40.0*(beta**2)*(sqrt(volumen_esp))
    return vmin

##Por los momentos no es factible el uso del coeficiente de flujo en el programa
##No hay una manera de conectar esta propiedad con la logica gral del programa sin romper el resto del codigo
#def FlowCoefficient(cv=None, D=None, K=None):
#    """Funcion para calcular Cv o K en la ecuacion de coeficiente de
#        flujo dadas las variables restantes
#
#        cv = coeficiente de flujo (GalonesUSA/min)
#        D = diametro (pulgadas)
#        K = coeficiente de accesorio
#        """
#    if cv == None:
#        cvi = (29.9*(D**2))/(sqrt(K))
#        return cvi
#    elif K == None:
#        Ki = (894.01*(D**4))/(cv**2)
#        return Ki
#    else:
#        return None
#    #en caso de darse "else" completar codigo para dar un mensaje de emergencia

def AccesoriesLosses(K, V, g=gravity):
    """Funcion para calcular la perdida por friccion en un accesorio

    hm = K*((V**2)/(2*g))

    K = factor K del accesorio
    V = velocidad (m/seg)
    g = Aceleracion de la gravedad (m/seg2)
    """
    hm = K*((V**2)/(2.0*g))
    return hm
