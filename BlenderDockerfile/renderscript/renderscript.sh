#!/bin/bash
# test stuff
echo "start script"
#taskqueueresult=$(/usr/bin/amqp-consume --url=$BROKER_URL -q $QUEUE -c 1 cat && echo)

#echo "found taskqueue result"
/usr/bin/amqp-declare-queue --url=$BROKER_URL -q $QUEUE"FrameList" -d

framenumber=$(/usr/bin/amqp-get --url=$BROKER_URL -q $QUEUE)
status=$?
echo "initial status: $status"
while [ $status -eq 0 ]
do
/usr/local/blender/blender -b -noaudio /home/shared/$QUEUE.blend -o /home/shared/$QUEUE/frame_### -f ${framenumber}

/usr/bin/amqp-publish --url=$BROKER_URL -r $QUEUE"FrameList" -p -b $framenumber

framenumber=$(/usr/bin/amqp-get --url=$BROKER_URL -q $QUEUE)
status=$?
echo "status: $status"
hello=1
#  status=$(( $x + 2 ))
done

if [[ ${hello} == 1 ]]
then
	exit 0
	else
	exit 1
fi

