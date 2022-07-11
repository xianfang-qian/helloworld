#!/usr/bin/env python
import time
import sys
import os
import json
import logging
from argparse import ArgumentParser
#from flask import Flask, Response, jsonify, render_template, make_response
import influxdb
import numpy as np
import cv2
#from scipy import signal
from threading import Thread, Lock


#app = Flask(__name__)
log = logging.getLogger(__name__)


SERVER_HOST = os.getenv('LOCAL_HOST')
NAMESPACE = os.getenv('NAMESPACE')
INFLUXDB_HOST = "influxdb.{}.svc".format(NAMESPACE)
INFLUXDB_PORT = "8086"

DATABASE_NAME = "HelloWorld"


#parser = ArgumentParser()
#parser.add_argument("-infuxdb_h", "--influxdb_host",
#                    help="Host IP of influxdb",
#                    required=False, default=INFLUXDB_HOST, type=str)
#parser.add_argument("-infuxdb_p", "--influxdb_port",
#                    help="Port of influxdb",
#                    required=False, default="8086", type=int)
#parser.add_argument("-influxdb_user", "--influxdb_username",
#                    help="Username for of influxdb",
#                    required=False, default="admin", type=str)
#parser.add_argument("-influxdb_pass", "--influxdb_password",
#                    help="Password for of influxdb",
#                   required=False, default="admin", type=str)
#parser.add_argument("-database", "--influxdb_database",
#                    help="Database name for of influxdb",
#                    required=False, default=DATABASE_NAME, type=str)
#args = parser.parse_args()

mutex = Lock()

print("Start to connect to influxdb...")
try:
    client = influxdb.InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT,
                                        username="admin",
                                        password="admin",
                                        database=DATABASE_NAME)
    client.create_database(DATABASE_NAME)
    #client.swithc_database(DATABASE_NAME)
    print("Connect sucess...")
except Exception :
    pass


def add_data_to_influxdb(var1,var2):
    mutex.acquire()
    json_body = []
    #fields={var1:var2}
    json_body.append({"measurement": "OutPut",
                          "fields": {
                          "Test"+str(var1):var2}})
    print ("Start update InfluxDB.....:",var1)
#    client.write_points(content)
    client.write_points(json_body)
    time.sleep(1)
    print ("Update finished.....:",var1)
    time.sleep(0.5)
    mutex.release()

def main():
    n=1
    while n<20:
        add_data_to_influxdb(n,n*0.01)
        time.sleep(5)
        n=n + 1
        print("hello world....:",n)

    try:
        result = client.query('select * from students;') 
        print("Result: {}".format(result))
    except Exception:
        pass
if __name__=='__main__':
    main()




