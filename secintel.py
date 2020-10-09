#!/usr/bin/python
import logging
import os
import random
import time
import traceback
import json
import requests

logging.basicConfig()
logger = logging.getLogger('logger')
logger.setLevel('DEBUG')

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

IP_SECINTEL="10.55.0.13"
PORT_SECINTEL="4455"

@app.route('/')
@cross_origin()
def index():
    return "Hello, World!"    

monitoring_action_db = {}

### /MONITORING_ACTION ###
@app.route('/monitoring_action', methods=['GET'])
def get_monitoring_action_dict():
    logger.info("get_monitoring_action" )
    cs_json = monitoring_action_db
    return cs_json,200

@app.route('/monitoring_action/<uuid>', methods=['POST'])
def create_monitoring_action(uuid):
    data=request.json
    logger.info("configure_monitoring_action : " + str(data) )
    monitoring_action_db[uuid]=data
    if monitoring_action_db[uuid]['action_type'] == "MONITOR_IDS":
        #CREATE MONITORING CALLBACK_URL
        CALLBACK_URL = "http://" + IP_SECINTEL + ":" + PORT_SECINTEL + "/telemetry/" + uuid
        json_data = { "callback_url" : CALLBACK_URL, "enable" : 1 }
        #SUBSCRIBE TO ELEMENT WITH MONITORING URL
        URL = "http://" + monitoring_action_db[uuid]["element_ip"] + "/subscribe/"
        if data["debug"] == "False":
            logger.info("sending request to : " + str(URL) + " " + str(json_data) )      
            r = requests.post(URL,json =json_data)
        monitoring_action_db[uuid]['data'] = {} 
        logger.info("configure_monitoring_action : " + str(data) + " done!" )   
        return data,201
    return "Unknown monitoring action type", 400

@app.route('/monitoring_action/<uuid>', methods=['GET'])
def get_monitoring_action(uuid):
    logger.info("get_monitoring_action" )
    cs_json = monitoring_action_db[uuid]
    return cs_json,200

@app.route('/monitoring_action/<uuid>', methods=['DELETE'])
def delete_monitoring_action(uuid):
    logger.info("delete_monitoring_action: " +str(uuid) )
    del monitoring_action_db[uuid]
    logger.info("delete_connectivity_service: " +str(uuid) + " done!" )
    return "",204

### /TELEMETRY ###
@app.route('/telemetry/<uuid>', methods=['POST'])
def create_telemetry_element(uuid):
    data=request.json
    logger.info("create_telemetry_element : " + str(data) )
    monitoring_action_db[uuid]['data'][data['id']]=data
    return data,201

### MAIN ###
if __name__ == "__main__":
    logger.info("initializing secintel")
    
    #flask
    logger.info("initializing flask")
    port = os.environ.get('PORT_HTTP', PORT_SECINTEL)
    app.run(debug=False,host='0.0.0.0', port=port)
