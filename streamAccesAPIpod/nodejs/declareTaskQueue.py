#!/usr/bin/env python
import pika
import os


rabbit = os.getenv('RABBITMQ_SERVICE_PORT_5672_TCP_ADDR')



connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit))
channel = connection.channel()


args = {"x-max-priority": 3}
queueName= 'taskQueue'


channel.queue_declare(queue=queueName, durable=True, passive=False, auto_delete=False,  arguments=args);


connection.close()