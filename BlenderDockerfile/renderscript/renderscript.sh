#!/bin/bash
# test stuff
echo "start script"
#taskqueueresult=$(/usr/bin/amqp-consume --url=$BROKER_URL -q $QUEUE -c 1 cat && echo)

#echo "found taskqueue result"

framenumber=$(/usr/bin/amqp-get --url=$BROKER_URL -q $QUEUE)
status=$?
echo "initial status: $status"
while [ $status -eq 0 ]
do
/usr/local/blender/blender -b -noaudio /home/shared/$QUEUE.blend -o /home/shared/$QUEUE/frame_### -f ${framenumber}

framenumber=$(/usr/bin/amqp-get --url=$BROKER_URL -q $QUEUE)
status=$?
echo "status: $status"
#  status=$(( $x + 2 ))
done
exit 0
