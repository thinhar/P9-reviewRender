#!/bin/bash
echo "start script"
x2=$(/usr/bin/amqp-get --url=amqp://guest:guest@rabbitmq-service:5672 -q workqueue2)
status=$?
echo "status: $status"
while [ $status -eq 0 ]
do
/usr/local/blender/blender -b -noaudio /home/shared/$x2 -o /home/shared/frame_### -f 1

x2=$(/usr/bin/amqp-get --url=amqp://guest:guest@rabbitmq-service:5672 -q foo2)
status=$?
echo "status: $status"
#  status=$(( $x + 2 ))
done