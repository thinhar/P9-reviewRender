#!/usr/bin/env python3                                                                                                  
import sys
sys.path.append("/usr/local/lib/python3.6/dist-packages")
import pika
import os
import bpy

parameters = pika.URLParameters(os.environ['BROKER_URL'])
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
Queue=os.environ['QUEUE']

#scene.render.use_overwrite = True
bpy.context.scene.render.filepath = '//frame_#####'
message = channel.basic_get(Queue, True)

while str(message[0]) != "None":
    #render
    bpy.context.scene.frame_current = int(str(message[2]).split('\'')[1])
    bpy.ops.render.render(animation = False)
    message = channel.basic_get(Queue, True)


