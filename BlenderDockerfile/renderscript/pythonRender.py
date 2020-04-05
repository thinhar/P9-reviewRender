#!/usr/bin/env python                                                                                                  
 
import pika
import os

parameters = pika.URLParameters(os.environ['BROKER_URL'])
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
Queue=os.environ['QUEUE']
#----------------------------------------------------------testing stuff----------------------------------------------------------

# def callback(ch, method, properties, body):
#     # do some rendering here i think
#     print(" [x] Received %r" % body)
#     print(" [x] Received %r" % body)

# print(message)
# message = channel.basic_get(Queue, True)
# print(message)
# message = channel.basic_get(Queue, True)                                                                                
# print(message)                                                                                                          
# message = channel.basic_get(Queue, True)
# print(message)
# message = channel.basic_get(Queue, True)
# print(message)

# print(message.body)

# channel.basic_publish(
#         exchange='',
#         routing_key=Queue,
#         body='1something',
#         properties=pika.BasicProperties(
#                 delivery_mode=2,  # make message persistent
#                 priority=1 #1 is lowers priority
#         )
# )
# channel.basic_publish(
#         exchange='',
#         routing_key=Queue,
#         body='2something',
#         properties=pika.BasicProperties(
#                 delivery_mode=2,  # make message persistent
#                 priority=1 #1 is lowers priority
#         )
# )
# channel.basic_publish(
#         exchange='',
#         routing_key=Queue,
#         body='3something',
#         properties=pika.BasicProperties(
#                 delivery_mode=2,  # make message persistent
#                 priority=1 #1 is lowers priority
#         )
# )
#channel.basic_consume(
#    queue=Queue, on_message_callback=callback, auto_ack=True)
#channel.start_consuming()
#channel.start_consuming()
#--------------------------------------------------------------testing stuff---------------------------------------------------------
#scene.render.use_overwrite = True
scene.render.filepath = '//frame_#####'
message = channel.basic_get(Queue, True)

while str(message[0]) != "none":
    #render
    print(str(message[2]).split('\'')[1])
    bpy.context.scene.frame_current = int(str(message[2]).split('\'')[1])
    bpy.ops.render.render(animation = False)
    message = channel.basic_get(Queue, True)


message = channel.basic_get(Queue, True)

