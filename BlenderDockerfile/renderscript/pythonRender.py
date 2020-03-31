#!/usr/bin/env python                                                                                                  
 
import pika
import os

def callback(ch, method, properties, body):
    # do some rendering here i think
    print(" [x] Received %r" % body)
    print(" [x] Received %r" % body)
    

parameters = pika.URLParameters(os.environ['BROKER_URL'])
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
Queue=os.environ['QUEUE']
print(Queue)
channel.basic_publish(
        exchange='',
        routing_key=Queue,
        body=' something',
        properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
                priority=1 #1 is lowers priority
        )
)
channel.basic_publish(
        exchange='',
        routing_key=Queue,
        body=' something',
        properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
                priority=1 #1 is lowers priority
        )
)
channel.basic_publish(
        exchange='',
        routing_key=Queue,
        body=' something',
        properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
                priority=1 #1 is lowers priority
        )
)
#channel.basic_consume(
#    queue=Queue, on_message_callback=callback, auto_ack=True)
#channel.start_consuming()
message = channel.basic_get(Queue, True)
print(message)
message = channel.basic_get(Queue, True)
print(message)
message = channel.basic_get(Queue, True)                                                                                
print(message)                                                                                                          
message = channel.basic_get(Queue, True)
print(message)
message = channel.basic_get(Queue, True)
print(message)