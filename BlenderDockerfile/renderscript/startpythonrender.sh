#!/bin/bash

/usr/local/blender/blender -b -noaudio /home/shared/$QUEUE.blend --python /home/nodejs/pythonRender.py
status=$?
while [ $status -gt 0 ]
do
/usr/local/blender/blender -b -noaudio /home/shared/$QUEUE.blend --python /home/nodejs/pythonRender.py
status=$?
done

exit $status