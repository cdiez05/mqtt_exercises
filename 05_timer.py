#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 23:51:50 2023

@author: carlosdm
"""

'''
Ejercicio 5

Escribe el código de un cliente mqtt que podamos utilizar como temporizador. 
El cliente leerá mensajes (elige tú mismo el topic) en los que se indicarán: 
    - tiempo de espera
    - topic 
    - mensaje a publicar una vez pasado el tiempo de espera

El cliente tendrá que encargarse de esperar el tiempo adecuado y luego
publicar el mensaje en el topic correspondiente.
'''

from paho.mqtt.client import Client
from multiprocessing import Process
from time import sleep
import paho.mqtt.publish as publish

def task_with_message(message,broker):
	print('message in process ', message)
	topic, timeout, text = message[2:-1].split(',')
	print('reading message', timeout, topic, text)
	sleep(int(timeout))
	publish.single(topic, payload=text, hostname=broker)
	print('end message in process ',message)
	
def on_message(mqttc, userdata, msg):
	print('on_message inicio', msg.topic, msg.payload)
	task = Process(target=task_with_message, args=(str(msg.payload), userdata['broker']))
	task.start()
	print('on_message final', msg.payload)
	
def on_log(mqttc, userdata, level, string):
	print("LOG", userdata, level, string)

def on_connect(mqttc, userdata, flags, rc):
	print("CONNECT:", userdata, flags, rc)
	
def main(broker):
	userdata = {'broker': broker}
	mqttc = Client(userdata=userdata)
	mqttc.enable_logger()
	mqttc.on_message = on_message
	mqttc.on_connect = on_connect
	mqttc.connect(broker)
	topic = 'clients/timeout'
	mqttc.subscribe(topic)
	mqttc.loop_forever()

if __name__ == "__main__":
	import sys
	if len(sys.argv)<2:
		print(f"Usage: {sys.argv[0]} broker")
		sys.exit(1)
	broker = sys.argv[1]
	main(broker)