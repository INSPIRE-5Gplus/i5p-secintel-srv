#!/usr/bin/python
import logging
import os
import random
import time
import traceback
import json


logging.basicConfig()
logger = logging.getLogger('logger')
logger.setLevel('DEBUG')

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def index():
    return "Hello, World!"    

monitoring_action_db = {}

@app.route('/monitoring_action/<uuid>', methods=['POST'])
def create_monitoring_action(uuid):
    data=request.json
    logger.info("configure_monitoring_action : " + str(data) )
    monitoring_action_db[uuid]=data
    logger.info("configure_monitoring_action : " + str(data) + " done!" )    
    return data,201

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


if __name__ == "__main__":
    logger.info("initializing secintel")
    
    #flask
    logger.info("initializing flask")
    port = os.environ.get('PORT_HTTP', "8181")
    app.run(debug=False,host='0.0.0.0', port=port)
