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

import funct as f
import sqlite3

class DataManager():
    def __init__(self, systemData=None, accessoryData=None, pipeData=None, sysCalculation=None):
        self.systemData = self.manageSystemData(systemData)
        self.accessoryData = self.manageAccessoryData(accessoryData)
        self.pipeData = self.managePipeData(pipeData)
        self.sysCalculation = sysCalculation
        self.dPOutOFBounds = False
        self.minPressureDrop = None
        self.maxPressureDrop = None

        if self.systemData:
            f.CreateCustomDB()
            f.InsertSystemValues(self.systemData)
        elif self.accessoryData:
            f.InsertSegmentsValues(self.accessoryData)
        elif self.pipeData:
            f.InsertSegmentsValues(self.pipeData)
        elif self.sysCalculation:
            sysDataDict = self.fetchSystemValues()
            self.minDiamCalculation(sysDataDict["total_losses_metric"], sysDataDict)

    def manageSystemData(self, systemData):
        blueprint = {"flow": "None", "flow_unit" : "None", "flow_metric" : "None",
                     "fluid_name" : "None", "water" : "None", "temperature" : "None",
                     "temperature_unit" : "None", "viscosity" : "None", "viscosity_unit" : "None",
                     "viscosity_metric" : "None", "density" : "None", "density_unit" : "None",
                     "density_metric" : "None", "total_losses" : "None", "total_losses_unit" : "None",
                     "total_losses_metric" : "None", "pressure_drop" : "None", "pressure_drop_unit" : "None",
                     "pressure_drop_metric" : "None", "pipe_type" : "None", "roughness_metric" : "None",
                     "roughness" : "None", "roughness_unit" : "None"
                     }
        data = blueprint
        if systemData:
            for value in systemData:
                if type(systemData[value]) == unicode:
                    data[value] = str(systemData[value])

                else:
                    data[value] = systemData[value]

            return data

    def managePipeData(self, pipeData, flag=None):
        blueprint = {"name" : "None", "type" : "None", "pipe_type" : "None", "NPS" : "None",
                     "OD" : "None", "ID" : "None", "WT" : "None", "minimum_diameter" : "None",
                     "minimum_diameter_unit" : "None", "losses" : "None", "losses_unit" : "None",
                     "losses_metric" : "None", "pressure_drop" : "None", "pressure_drop_unit" : "None",
                     "pressure_drop_metric" : "None", "schedule" : "None",
                     "minimum_velocity" : "None", "minimum_velocity_unit" : "None",
                     "minimum_velocity_metric" : "None", "friction_factor" : "None",
                     "reynolds" : "None", "orientation" : "None", "connected_from" : "None",
                     "connected_to" : "None", "roughness" : "None", "roughness_unit" : "None",
                     "roughness_metric" : "None", "length" : "None", "length_unit" : "None",
                     "length_metric" : "None"
                     }
        data = blueprint
        if pipeData:
            for value in pipeData:
                if type(pipeData[value]) == unicode:
                    data[value] = str(pipeData[value])

                else:
                    data[value] = pipeData[value]
            if not flag:
                data["name"] = self.setName("pipe")
                data["connected_from"] = self.setConnections()
            return data

    def manageAccessoryData(self, accessoryData, flag=None):
        blueprint = {"name" : "None", "type" : "None", "NPS" : "None", "OD" : "None",
             "ID" : "None", "WT" : "None", "minimum_diameter" : "None",
             "schedule" : "None", "connected_from" : "None", "connected_to" : "None",
             "class" : "None", "D_2" : "None", "D_2_type" : "None", "k_factor" : "None", "cv" : "None",
             "radius" : "None", "turbulent_friccion_factor" : "None",
             "minimum_velocity_metric" : "None", "losses_metric" : "None",
             "pressure_drop_metric" : "None"
             }

        data = blueprint

        if accessoryData:
            for value in accessoryData:
                if type(accessoryData[value]) == unicode:
                    data[value] = str(accessoryData[value])

                else:
                    data[value] = accessoryData[value]
            if not flag:
                data["name"] = self.setName(data["type"])
                data["connected_from"] = self.setConnections()
            return data

    def getDiameter(self):
        connection = sqlite3.connect("custom.pype")
        cursor = connection.cursor()
        command = "SELECT minimum_diameter_metric FROM segments WHERE rowid=1"
        cursor.execute(command)
        data = cursor.fetchall()
        connection.close()
        return data[0][0]

    def calculateTotalLosses(self, dP_metric):
        connection = sqlite3.connect("custom.pype")
        cursor = connection.cursor()
        command = "SELECT density_metric FROM system WHERE rowid=1"
        cursor.execute(command)
        data = cursor.fetchall()
        connection.close()
        density = data[0][0]
        total_losses = f.PressureLossesConvert(ro=density, dP=dP_metric)
        return total_losses
#    def updateSystem(self, values):
#        connection = sqlite3.connect("custom.pype")
#        cursor = connection.cursor()
#
#        #begin segmento para obtener los nombres de las columnas de la base de datos
#        cursor.execute("PRAGMA table_info(system)")
#        data2 = cursor.fetchall()
#        data_col = []
#
#        for values in data2:
##            print values[1], type(values[1])
#            data_col.append(str(values[1]))
#        #end segmento para obtener los nombres de las columnas de la base de datos
#
#        command = "SELECT * FROM segments WHERE rowid=1"
#        cursor.execute(command)
#        data = cursor.fetchall()
#        systemValues = data[0]
#
#        connection.close()

    def setConnections(self):
        connection = sqlite3.connect("custom.pype")
        cursor = connection.cursor()
        command = "SELECT name FROM segments"
        cursor.execute(command)
        data = cursor.fetchall()
        numberOfRows = len(data)
        if numberOfRows:
            command = "SELECT name FROM segments WHERE rowid=%s" % numberOfRows
            cursor.execute(command)
            data = cursor.fetchall()
            connectedFrom = str(data[0][0])
        else:
            connectedFrom = "None"

        connection.close()
        return connectedFrom


    def setName(self, type):
        connection = sqlite3.connect("custom.pype")
        cursor = connection.cursor()
#        command = """UPDATE system SET schedule="%s" WHERE rowid=1""" % "STD"
#        cursor.execute(command)

        if type == "pipe":
            command = """SELECT name FROM segments WHERE type='pipe'"""
            cursor.execute(command)
            data = cursor.fetchall()
            if  not len(data):
                name = "pipe_1"
            else:
                data2 = data[-1][0]
                dataList = data2.split("_")
                pipeNum = int(dataList[-1])
#                print pipeNum
                name = "pipe_" + str(pipeNum+1)
#                print Name

        elif type != "pipe":
            command = """SELECT name FROM segments WHERE type=%r""" % type
            cursor.execute(command)
            data = cursor.fetchall()
            if  not len(data):
                name = type+"_1"
            else:
                data2 = data[-1][0]
                dataList = data2.split("_")
                accessoryNum = int(dataList[-1])
                name = type + "_" + str(accessoryNum+1)
        else:
            msg = "se cumplio condicion else \nmodulo: setConnections\nvarible: type"
            raise Exception, msg

        connection.close()
        return name

    def fetchSystemValues(self):
        connection = sqlite3.connect("custom.pype")
        cursor = connection.cursor()
        command = "SELECT * FROM system WHERE rowid=1"
        cursor.execute(command)
        sysdata = cursor.fetchall()
        sysDataCol = []
        for values in sysdata[0]:
            if not values:
                sysDataCol.append("None")
            else:
                if type(values) == unicode:
                    sysDataCol.append(str(values))

                else:
                    sysDataCol.append(values)

        cursor.execute("PRAGMA table_info(system)")
        data2 = cursor.fetchall()
        data_col = []
        connection.close()
        for values in data2:
        #            print values[1], type(values[1])
            data_col.append(str(values[1]))

        #print len(data_col)
        #print len(sysDataCol)
        sysDataDict = {}
        for value in range(len(sysDataCol)):
        #    print value
        #    print data_col[value]
        #    print sysDataCol[value]
            sysDataDict[data_col[value]] = sysDataCol[value]
            if not sysDataDict[data_col[value]]:
                sysDataDict[data_col[value]] = "None"
        return sysDataDict

    def fetchSegmentsColNames():
        connection = sqlite3.connect("custom.pype")
        cursor = connection.cursor()
        #begin segmento para obtener los nombres de las columnas de la base de datos
        cursor.execute("PRAGMA table_info(segments)")
        data2 = cursor.fetchall()
        data_col = []
        connection.close()
        for values in data2:
#            print values[1], type(values[1])
            data_col.append(str(values[1]))
        connection.close()
        return data_col
    
    def minDiamCalculation(self, setpoint, sistema,  flag=None):

        minDiam = 15  #para minimum_diameter
        maxDiam = 600 #para minimum_diameter

        if not flag:
            database = "custom.pype"
        else:
            database = flag

        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        #begin segmento para obtener los nombres de las columnas de la base de datos
        cursor.execute("PRAGMA table_info(segments)")
        data2 = cursor.fetchall()
        data_col = []
        connection.close()
        for values in data2:
#            print values[1], type(values[1])
            data_col.append(str(values[1]))
        #end segmento para obtener los nombres de las columnas de la base de datos

#        midDiamLosses, midDiamPressureDrop = self.lossesCalculation()

        minDiamSegments = self.changeDBValues(data_col, minDiam)
#        for x in minDiamSegments:
#            print x
#        raise Exception, "blaaaaa"
        minDiamlosses, minDiamPressureDrop = self.lossesCalculation(orden_de_segmentos=minDiamSegments, sistema=sistema, doPrint="No")
        print "minimun losses = %s m" % minDiamlosses
        self.maxPressureDrop = minDiamPressureDrop

        maxDiamSegments = self.changeDBValues(data_col, maxDiam)
        maxDiamlosses, maxDiamPressureDrop = self.lossesCalculation(orden_de_segmentos=maxDiamSegments, sistema=sistema, doPrint="No")
        print "maximun losses = %s m" % maxDiamlosses
        self.minPressureDrop = maxDiamPressureDrop
        print "setpoint = %s m" % setpoint
        print "*"*20

        if (setpoint > maxDiamlosses and
            setpoint < minDiamlosses):
                cont = 1
                while True:

        #            if cont == 20:
        #                break
        #            else:
        #                pass
                    diameter = (maxDiam+minDiam)/2.0
                    diameterSegments = self.changeDBValues(data_col, diameter)
                    losses, pressureDrop = self.lossesCalculation(orden_de_segmentos=diameterSegments, sistema=sistema)
        #            diameter = (2.0*maxDiam*minDiam)/(maxDiam+minDiam)
#                    tuberia1["minimum_diameter"] = diameter
#                    losses = lossesCalculation(sistema, orden_de_segmentos, "foo.pype")
                    print "min diameter %s mm" % minDiam
                    print "max diameter %s mm" % maxDiam
                    print "diameter %s mm" % diameter
                    print "losses %s m" % losses
                    print "error %s " % (setpoint - losses)
                    print "iteracion numero %s" %cont
                    print "*"*10

                    if abs(setpoint - losses) > 0.001:
        #                print "foo"
                        if setpoint > losses:
                            maxDiam = diameter
                        else:
                            minDiam = diameter

                    else:
                        print "end"
                        print"*"*20
                        self.dPOutOFBounds = False
                        break
                    cont += 1

        else:
            self.dPOutOFBounds = True
#            print "value out of range"

    def changeDBValues(self, colNames, newDiameter):
        data_col = colNames
        orden_de_segmentos = []
        connection = sqlite3.connect("custom.pype")
        cursor = connection.cursor()
        command = "SELECT * FROM segments"
        cursor.execute(command)
        data = cursor.fetchall()
#        print data
#        msg = "sss"

        connection.close()
        for segment in range(len(data)):
            segmentDict = {}
            for value in range(len(data[segment])):
                segmentDict[data_col[value]] = data[segment][value]
                if not segmentDict[data_col[value]]:
                    segmentDict[data_col[value]] = "None"
            if segmentDict["type"] == "pipe":
                segmentDict2 = self.managePipeData(segmentDict, flag="foo")
            else:
                segmentDict2 = self.manageAccessoryData(segmentDict, flag="foo")
#            print segmentDict2["type"], type(segmentDict2["type"])
            segmentDict2["minimum_diameter"] = newDiameter
            segmentDict2["minimum_diameter_unit"] = "mm"
            orden_de_segmentos.append(segmentDict2)
        return orden_de_segmentos

    def lossesCalculation(self, flag=None, orden_de_segmentos=None, sistema=None, doPrint=None):
	if not flag:
		database = "custom.pype"
	else:
		database = flag

	if orden_de_segmentos:
		f.CreateCustomDB(flag=flag)
		f.InsertSystemValues(sistema, flag=flag)
		for segmentos in orden_de_segmentos:
#                    for x in segmentos:
#                        print x, type(x), " == ", segmentos[x], type(segmentos[x])
#
#                    raise Exception, "msg"
                    f.InsertSegmentsValues(segmentos, flag=flag)
	connection = sqlite3.connect(database)
	cursor = connection.cursor()
	command = "SELECT losses_metric, height, reynolds FROM segments"
	cursor.execute(command)
	data = cursor.fetchall()
#        print data
	total_losses2 = 0
	d_height = 0
	print "reynolds %s " % data[0][2]
	for x in data:
#	    print x[0], type(x[0])
            total_losses2 += x[0]
            try:
                    d_height += x[1]
            except:
                    pass
            else:
                    pass

	command = "SELECT minimum_velocity_metric FROM segments WHERE type='pipe'"
	cursor.execute(command)
	data = cursor.fetchall()
	initial_velocity = data[0][0]
	final_velocity = data[-1][0]
	total_losses = f.TotalLosses(V1=initial_velocity, Vn=final_velocity, hft=total_losses2, dZ=d_height)
	command = "SELECT density_metric, viscosity_metric FROM system"
	cursor.execute(command)
	data = cursor.fetchall()
	system_density = data[0][0]
	viscosity_metric = data[0][1]
	total_pressure_drop = f.PressureDrop(ht=total_losses, ro=system_density)
        total_pressure_drop_bar = f.PressureConvert(x=total_pressure_drop, unitin="Pa", unitout="bar")
	if not doPrint:
		print total_pressure_drop, " Pascal"
		print total_pressure_drop_bar, " bar"
		print system_density, viscosity_metric

	#command = "SELECT connected_to FROM segments"
	#cursor.execute(command)
	#print cursor.fetchall()
	connection.close()
	try:
		os.remove(flag)
	except:
		pass
#        print "bad"
	else:
		pass
#        print "good"


	return total_losses, total_pressure_drop

if __name__ == "__main__":
    """foo"""
#    value = DataManager()
#    value.setConnections()

#    systemValues = {'flow_unit': u'gal/min', 'pipe_type': 'CSP', 'flow': 0.01, 'temperature': 100, 'temperature_unit': u'C',
#                    "water" : "yes"}
#    managedata = DataManager(systemValues)
#    print managedata.systemData



