#!/usr/bin/env python
import pika
import os
import sys

queueName = os.getenv('MY_POD_NAME')
#queueName = sys.argv[1];
rabbit = os.getenv('RABBITMQ_SERVICE_PORT_5672_TCP_ADDR')

numberOfFrames=50

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit))
channel = connection.channel()


args = {"x-max-priority": 3}


channel.queue_declare(queue=queueName, durable=True, passive=False, auto_delete=False,  arguments=args);

i=0
while i <= numberOfFrames:
	channel.basic_publish(
		exchange='',
		routing_key=queueName,
		body=str(i),
		properties=pika.BasicProperties(
			delivery_mode=2,  # make message persistent
			priority=1 #1 is lowers priority
		)
	)
	i += 1;
	

connection.close()