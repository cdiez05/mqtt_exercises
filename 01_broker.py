"""
Created on Sun Apr 16 13:12:35 2023

@author: carlosdm
"""



"""
Ejercicio 1


Un componente esencial del sistema es un broker que se encarga de gestionar 
las publicaciones y subscripciones de los distintos elementos que se conectan.
Para los ejercicios posteriores utilizaremos el broker en simba.fdi.ucm.es.


Los usuarios que se conectan, pueden enviar y recibir mensajes en el topic clients. 
También podréis crear vuestros propios canales de forma jerárquica a partir de esta raíz. 
Es decir, podéis publicar y leer en topics del estilo clients/mi_tema/mi_subtema.
Comprueba, en primer lugar, que puedes conectarte al broker y enviar y recibir mensaje
"""

from paho.mqtt.client import Client

def on_message(client, userdata, msg):
    print("MESSAGE:", userdata, msg.topic, msg.qos, msg.payload, msg.retain) 
    
def on_publish(mqtcc,userdata,mid):
    print("Message with topic clients published")

def main(broker, topic): 
    client = Client()
    
    print(f'connecting {broker}')
    client.connect(broker)
    client.subscribe(topic)
    client.on_publish = on_publish
    client.on_message = on_message
    
    client.loop_start()
    while True:
        mensaje=input("Write your message")
        client.publish(topic, mensaje)
    client.loop_stop()


if __name__ == "__main__":
    import sys
    if len(sys.argv)<3:
        print(f"Usage: {sys.argv[0]} broker topic") 
        sys.exit(1)
    broker = sys.argv[1]
    topic = sys.argv[2]
    main(broker, topic)