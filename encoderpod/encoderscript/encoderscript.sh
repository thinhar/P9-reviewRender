#!/bin/bash
# test stuff
echo "start script"
#taskqueueresult=$(/usr/bin/amqp-consume --url=$BROKER_URL -q $QUEUE -c 1 cat && echo)
queuename=${FOLDERNAME}"FrameList"

#echo "found taskqueue result"
/usr/bin/amqp-declare-queue --url=$BROKER_URL -q ${FOLDERNAME}"FrameList" -d
#RESOLUTION=1920x1080
#FRAMERATE=24
#STARTFRAME=0

endframe=$(($FRAMES_IN_SCENE + $STARTFRAME))

while true
do

framenumber=$(/usr/bin/amqp-consume --url=$BROKER_URL -q $queuename -c 1 cat && echo)





#encode command
$(ffmpeg -framerate ${FRAMERATE} -start_number ${framenumber} -i /home/shared/${FOLDERNAME}/frame_%04d.png -r 30 -g 90 -s ${RESOLUTION} -quality realtime -speed 5 -threads 2 -row-mt 1 -tile-columns 3 -frame-parallel 0 -b:v 2000k -c:v vp9 -b:a 128k -c:a libopus -f webm "/home/shared/"${FOLDERNAME}"/output"${framenumber}".webm")



$(echo "file 'output${framenumber}.webm'">>/home/shared/${FOLDERNAME}/outputfiles.txt)


$(ffmpeg -f concat -i "/home/shared/${FOLDERNAME}/outputfiles.txt" -c copy "/home/shared/${FOLDERNAME}/finaloutput${framenumber}.webm")

$(printf "finaloutput${framenumber}.webm">/home/shared/${FOLDERNAME}/currentFinalfile)

$(echo ${framenumber} " " $(date --utc +%FT%T.%3NZ) >> /home/shared/${FOLDERNAME}/timestamps)

if [ framenumber -eq $endframe ]
then
    break
fi

done
exit 0