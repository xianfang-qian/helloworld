"""
Copyright 2021 Intel Corporation

This software and the related documents are Intel copyrighted materials,
and your use of them is governed by the express license under which they
were provided to you ("License"). Unless the License provides otherwise,
you may not use, modify, copy, publish, distribute, disclose or transmit
this software or the related documents without Intel's prior written permission.

This software and the related documents are provided as is, with no express or
implied warranties, other than those that are expressly stated in the License
"""

import os
import math
import sys
import time
import json
import influxdb
import logging
from argparse import ArgumentParser
import multiprocessing as mp
from flask import Flask, Response, jsonify, render_template, make_response
import requests
from threading import Thread, Lock


app = Flask(__name__)
log = logging.getLogger(__name__)

SERVER_HOST = os.getenv('LOCAL_HOST')
NAMESPACE = os.getenv('NAMESPACE')
INFLUXDB_HOST = "influxdb.{}.svc".format(NAMESPACE)
INFLUXDB_PORT = "8086"

DATABASE_NAME = "HelloWorld"
NETWORK_FPS = 20
NUM_CH = 1
RUNNING = []
MUTEX = None
CONFIG_PATH = None
CONF_DATA, URL_DATA = {}, {}
Q_DATA = {}
CURRENT_FRAMES = []
FPS = []



#@app.route('/get_all_streams')
#def get_all_streams("Text"):
#   """
#    Route to show all running video streams
#    """
#    return "HelloWorld,Please try again!"

@app.route("/")
def index():
    """Function to test the functionality of the API"""
    return "HelloWorld, Nice to see you!"

mutex = Lock()

print("Start to connect to influxdb...")
try:
    client = influxdb.InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT,
                                        username="admin",
                                        password="admin",
                                        database=DATABASE_NAME)
    i = -1
    while i<=20:
        i += 1
        try:
            client.drop_database(DATABASE_NAME)
            break
        except:
            log.info('Retrying...')
            time.sleep(1)
    client.drop_database(DATABASE_NAME)
    client.create_database(DATABASE_NAME)
    print("Connect sucess...")
except Exception:
    print("Connect failed...")
    sys.exit(-1)

#    client.create_database(DATABASE_NAME)
#    print("Connect sucess...")
#except Exception :
#    print("Connect failed...")
#    pass


def add_data_to_influxdb(var1,var2):
    mutex.acquire()
    json_body = []
    #fields={var1:var2}
    json_body.append({"measurement": "OutPut",
                      #"tags": {"test":"helloword"},
                      "fields": {
                          "Test":var2}})

    print ("Start update InfluxDB.....:",var1)
#    client.write_points(content)
    client.write_points(json_body)
    #time.sleep(10)
    print ("Update finished.....:",var1)
    #time.sleep(0.5)
    mutex.release()


def main():
    server_port = 8000
    print("Hello")
    n=1
    while n<=100:
        add_data_to_influxdb(n,n*0.01)
        print(n)
        #time.sleep(5)
        n=n + 1
        print("hello world....:",n)
    app.run(host=SERVER_HOST, port=server_port, threaded=True)


if __name__=='__main__':
    main()
