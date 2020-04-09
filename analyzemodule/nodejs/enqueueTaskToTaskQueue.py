#!/usr/bin/env python3
import pika
import os
import sys

nameOfTask = sys.argv[1]
numberOfpodsRequired = int(sys.argv[2])
resourceRequirements = sys.argv[3]

print (nameOfTask) 
print (numberOfpodsRequired) 
print (resourceRequirements)

rabbit = os.getenv('RABBITMQ_SERVICE_PORT_5672_TCP_ADDR')


connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit))
channel = connection.channel()


queueName= 'taskQueue'
i = 1
while i <= numberOfpodsRequired:
	i += 1
	channel.basic_publish(
		exchange='',
		routing_key=queueName,
		body=nameOfTask+' '+ resourceRequirements,
		properties=pika.BasicProperties(
			delivery_mode=2,  # make message persistent
			priority=1 #1 is lowers priority
		)
	)
	

connection.close()