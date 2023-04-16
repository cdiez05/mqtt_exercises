#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 13:25:12 2023

@author: carlosdm
"""

'''
Ejercicio 1 

En el topic numbers se están publicando constantemente números, 
los hay enteros y los hay reales. 

Escribe el código de un cliente mqtt que lea este topic 
y que realice tareas con los números leídos,por ejemplo, separar los enteros y reales,
calcular la frecuencia de cada uno de ellos, 
estudiar propiedades (como ser o no primo) en los enteros, etc.


'''
from paho.mqtt.client import Client
import traceback
import sys
from sympy import isprime


def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)
    try:
        n =  float(msg.payload)
        if n%1 == 0.0:
            client.publish('/clients/Real_numbers', msg.payload)
            userdata['frequence']['Real_number'] += 1
            client.publish('/clients/Frec_Reals', f'{userdata["frequence"]["Real_number"]}')
        else: 
            n = int(msg.payload)
            client.publish('/clients/Int_numbers', msg.payload)
            userdata['frequence']['Int_number'] += 1
            client.publish('/clients/Frec_Ints', f'{userdata["frequence"]["Int_number"]}')
            userdata['sum']['sum'] += n
            client.publish('/clients/sum', f'{userdata["sum"][sum]}')
            if n % 2 == 0:
                client.publish('/clients/even', msg.payload)
            else:
                client.publish('/clients/odd', msg.payload)
            if isprime(n):
                client.publish('/clients/prime', msg.payload)
    except ValueError:
        pass
    except Exception as e:
        raise e


def main(broker):
    userdata = { 'sum' : {'sum' : 0}, 'frequence' : {'Real_number' : 0, 'Int_number': 0}}
    
    
    userdata = {'suma':0}
    client = Client(userdata=userdata)
    client.on_message = on_message

    print(f'Connecting on channels numbers on {broker}')
    client.connect(broker)

    client.subscribe('numbers')

    client.loop_forever()


if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
    broker = sys.argv[1]
    main(broker)
