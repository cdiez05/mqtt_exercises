"""
Created on Sun Apr 16 13:34:19 2023

@author: carlosdm
"""


"""
Ejercicio número 4: 
   

Elige un termómetro concreto al que escuchar,es decir, 
uno de los sensores que publican en temperature. 

Escribe ahora el código para un cliente mqtt cuya misión es escuchar un termómetro y, 
si su valor supera una determinada temperatura,K0, 
entonces pase a escuchar también en el topic humidity.

Si la temperatura baja de K0 o el valor de humidity sube de
K1 entonces el cliente dejará de escuchar en el topic humidity.
    
"""
from paho.mqtt.client import Client
import traceback
import sys

#Fijamos los siguientes valores de temperatura y humedad respectivamente:
K0 = 25 #si se supera esta temperatura se pasa a escuchar también en el topic humidity
K1 = 40 #si la temperatura baja de K0 o el valor de humidity sube de K1 entonces
#el cliente dejará de escuchar en el topic humidity

def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)
    n = float (msg.payload)
    if msg.topic == 'temperature/t1':
        if n > K0 and userdata['humidity'] == False:
            client.subscribe('humidity')
            userdata['humidity'] = True #suscrito a humidity
        elif n < K0 and userdata['humidity'] == True:
            client.unsubscribe('humidity') #deja de estar suscrito a humidity
            userdata['humidity'] = False
    elif msg.topic == 'humidity':
        if n > K1:
            client.unsubscribe('humidity')
            userdata['humidity'] = False
            
def main(hostname):
    userdata = {
        'humidity':False
    }
    client = Client(userdata= userdata)
    client.on_message = on_message

    print(f'Connecting on channels numbers on {hostname}')
    client.connect(hostname)

    client.subscribe('temperature/t1')

    client.loop_forever()

if __name__ == "__main__":
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
    broker = sys.argv[1]
    main(broker)