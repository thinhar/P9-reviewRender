#!/bin/bash
# test stuff



framenumber=0
#encode command
$(ffmpeg -framerate ${FRAMERATE} -start_number ${framenumber} -i /home/shared/${FOLDERNAME}/frame_%03d.png -r 30 -g 90 -s ${RESOLUTION} -quality realtime -speed 5 -threads 2 -row-mt 1 -tile-columns 3 -frame-parallel 0 -b:v 2000k -c:v vp9 -b:a 128k -c:a libopus -f webm "/home/shared/"${FOLDERNAME}"/output.webm")

exit 0