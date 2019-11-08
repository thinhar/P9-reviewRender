#!/bin/bash
# test stuff
echo "start script"
taskqueueresult=$(/usr/bin/amqp-consume --url=$BROKER_URL -q $QUEUE -c 1 cat && echo)

echo "found taskqueue result"

x2=$(/usr/bin/amqp-get --url=$BROKER_URL -q $taskqueueresult)
status=$?
echo "status: $status"
while [ $status -eq 0 ]
do
/usr/local/blender/blender -b -noaudio /home/shared/$x2 -o /home/shared/frame_###

x2=$(/usr/bin/amqp-get --url=$BROKER_URL -q $taskqueueresult)
status=$?
echo "status: $status"
#  status=$(( $x + 2 ))
done
exit 0