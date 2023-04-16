#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 18:25:42 2023

@author: carlosdm
"""


"""
Ejercicio número 3
"""
from paho.mqtt.client import Client
from time import sleep
import sys

temp_t1 = [] 
temp_t2 = []

def calculo_estadisticas():
    t1_max = max(temp_t1)
    t1_min = min(temp_t1)
    t1_avg = sum(temp_t1) / len(temp_t1)
    t2_avg = max(temp_t2)
    t2_min = min(temp_t2)
    t2_media = sum(temp_t2) / len(temp_t2)
    print(f'SENSOR 1 - Max: {t1_max}, Min: {t1_min}, Average: {t1_avg}')
    print(f'SENSOR 2 - Max: {t2_avg}, Min: {t2_min}, Average: {t2_media}')
    # Vaciamos las listas
    temp_t1.clear()
    temp_t2.clear()


def on_message(client, userdata, msg):
    data = msg.payload.decode()
    topic = msg.topic
    if topic == 'temperature/t1':
        temp_t1.append(float(data))
    elif topic == 'temperature/t2':
        temp_t2.append(float(data))

def main(hostname):
    client = Client()
    client.on_message = on_message
    print(f'Connecting on channels numbers on {hostname}')
    client.connect(hostname)
    client.subscribe('temperature/#')
    client.loop_start()

    while True:
        sleep(5) #Esperamos 5 segundos
        calculo_estadisticas()


if __name__ == '__main__':
    hostname = 'simba.fdi.ucm.es'
    if len(sys.argv)>1:
        hostname = sys.argv[1]
    main(hostname)