#!/bin/bash

/usr/local/blender/blender -b -noaudio /home/shared/$incomingname --python /home/nodejs/analyser.py
status=$?
while [ $status -gt 0 ]
do
    /usr/local/blender/blender -b -noaudio /home/shared/$incomingname --python /home/nodejs/analyser.py
    status=$?
done

exit $status