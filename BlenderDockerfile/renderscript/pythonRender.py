#!/usr/bin/env python3                                                                                                  
import sys
sys.path.append("/usr/local/lib/python3.6/dist-packages")
import pika
import os
import bpy
import math

parameters = pika.URLParameters(os.environ['BROKER_URL'])
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
Queue=os.environ['QUEUE']
message = channel.basic_get(Queue, True)
digits = 0

# Blender Settings Setup
#scene.render.use_overwrite = True
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.render.threads_mode = 'AUTO'
bpy.context.scene.cycles.tile_order = 'HILBERT_SPIRAL'
bpy.context.scene.render.tile_x = 64
bpy.context.scene.render.tile_y = 64

def CalulateDigits(n):
    global digits
    if n > 0:
        digits = int(math.log10(n))+1
    elif n == 0:
        digits = 1
    else:
        digits = int(math.log10(-n))+2 


while str(message[0]) != "None":
    bpy.context.scene.frame_current = int(str(message[2]).split('\'')[1])
    CalulateDigits(bpy.context.scene.frame_current)
    digits_str = ''
    i = 0

    while i < (5 - digits):
        digits_str += '0'
        i += 1

    digits_str += str(bpy.context.scene.frame_current)
    bpy.context.scene.render.filepath = "//" + Queue + "/frame_" + digits_str
    bpy.ops.render.render(write_still = 1, animation = False)

    channel.basic_publish(
		exchange='',
		routing_key=Queue+""+FrameList,
		body=bpy.context.scene.frame_current,
		properties=pika.BasicProperties(
			delivery_mode=2,  # make message persistent
			priority=1 #1 is lowers priority
		)
	)


    message = channel.basic_get(Queue, True)

