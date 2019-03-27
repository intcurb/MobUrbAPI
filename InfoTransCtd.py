# -*- coding: utf-8 -*-
from flask import Flask, request, Response
from flask_restful import Resource, Api
from flask import send_file
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
import os, sys, pyproj
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
import lxml.etree as et
import json
from pprint import pprint
from lxml import objectify
import shutil
from shutil import copyfile
from shutil import make_archive
import datetime
import zipfile

cwd = os.getcwd()

begin = """<?xml version="1.0" encoding="UTF-8"?>
<!-- generated on Thu Mar 14 11:12:35 2019 by SUMO duarouter Version 0.32.0
<?xml version="1.0" encoding="UTF-8"?>

<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/duarouterConfiguration.xsd">

    <input>
        <net-file value="map.net.xml"/>
        <route-files value="trips.trips.xml"/>
    </input>

    <output>
        <output-file value="map.rou.xml"/>
        <alternatives-output value="map.rou.alt.xml"/>
    </output>

    <processing>
        <ignore-errors value="true"/>
    </processing>

    <time>
        <begin value="0"/>
        <end value="3600"/>
    </time>

    <report>
        <no-step-log value="true"/>
    </report>

</configuration>
-->
<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">
    <vType id="car" vClass="passenger"/>
    <vType id="motorcicle" vClass="motorcycle"/>
    <vType id="bike" vClass="bicycle"/>
    <vType id="bus" vClass="bus"/>
    <vType id="truck" vClass="truck"/>"""
end = "</routes>"

#Load SUMO libs
tools = os.path.join(cwd, 'tools')
sys.path.append(tools)

# import the library
import sumolib
import traci
import traci.constants as tc

app = Flask(__name__)
api = Api(app)

class Simulation(Resource):
    def post(self):
        # parse the net
        now = datetime.datetime.now()
        net = sumolib.net.readNet('map.net.xml')
        path = "sumoFiles/simulation-" + str(now)
        fileName = "simulation-" + str(now)
        os.mkdir(path)

        copyfile("map.net.xml",  path + "/map.net.xml")
        copyfile("map.poly.xml", path + "/map.poly.xml")

        radius = 10

        data = request.json["jsonList"]
        date_first = datetime.datetime.strptime(data[0]["initDate"].replace('/', '-'), '%d-%m-%Y %H:%M:%S')
        i = 1
        vehicles = ""
        for route in data:
            date_init = datetime.datetime.strptime(route["initDate"].replace('/', '-'), '%d-%m-%Y %H:%M:%S')
            date_diff = date_init - date_first
            
            timeToInsertVehicle = str(int(date_diff.total_seconds()))

            if (route["meansOfTransport"] == "Bicicleta"):
                vehicleType = "bike"
            if (route["meansOfTransport"] == "Ônibus"):
                vehicleType = "bus"
            if (route["meansOfTransport"] == "Moto"):
                vehicleType = "motorcicle"
            if (route["meansOfTransport"] == "Caminhão"):
                vehicleType = "truck"
            else:
                vehicleType = "car"
                

            if ("listOfLocation" in route):
                verifyEdge = []
                j = 0
                listOfEdges = ""
                for coordinates in route["listOfLocation"]:
                    x, y = net.convertLonLat2XY(coordinates["lng"], coordinates["lat"])
                    edges = net.getNeighboringEdges(x, y, radius)
                    i = i+1
                    if len(edges) > 0:
                        distancesAndEdges = sorted([(dist, edge) for edge, dist in edges])
                        dist, closestEdge = distancesAndEdges[0]
                        xml=et.fromstring(str(closestEdge))
                        id = xml.attrib['id']
                        if id not in verifyEdge and ("-" + id) not in verifyEdge:
                            verifyEdge.append(id)
                            j = j+1
                            listOfEdges += " " + id
                if (j >= 2):
                    vehicles += '\n<vehicle id="' + str(i) + '" depart="' + timeToInsertVehicle + '" departSpeed="' + str(route["averageOfSpeed"]) + '" vClass="' + vehicleType + '"><route edges="'
                    vehicles += listOfEdges
                    vehicles += '"/></vehicle>\n'

        file = open(path + "/map.rou.xml","w")

        xmltext = ""
        file.write(xmltext + begin + vehicles + end) 
        
        file.close()

        make_archive(path, 'zip', path)

        return json.dumps({'file': "fileName=" + fileName + ".zip"}), 200, {'ContentType':'application/json'}
    
    def get(self):
        try:
            fileName = request.args.get("fileName")
            return send_file('sumoFiles/' + fileName, attachment_filename='teste.zip')
        except Exception as e:
            return str(e)
        

api.add_resource(Simulation, '/simulation') # Route


if __name__ == '__main__':
     app.run(port='5002')
     